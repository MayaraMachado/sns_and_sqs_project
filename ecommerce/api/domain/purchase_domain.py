import json
from django.conf import settings

from api.domain.domain_base import DomainServiceBase
from api.data_access.purchase_repository import PurchaseRepository
from api.models import Purchase

class PurchaseDomainService(DomainServiceBase):

    def __init__(self, product_domain, user_domain, sns_connection):
        self.product_domain = product_domain
        self.user_domain = user_domain
        self.sns_connection = sns_connection
        super().__init__(PurchaseRepository())

    def __calculate_total_price(self, products):
        prices = list(products.values_list('price', flat=True))
        return sum(prices)

    def __mask_card(self, card_number):
        return f"**** **** **** {card_number[-4:]}"

    def __notificate_transaction_sns(self, purchase):
        products = purchase.product.all()
        items = {}
        for product in products:
            seller = str(product.seller_id)
            if seller in items:
                items[seller] += product.price
            else:
                items[seller] = product.price


        message = {
                    "items" : items,
                    "purchase_date" :  purchase.created_at.strftime("%Y-%m-%d %H:%M:%S %Z"),
                    "purchase_id" : str(purchase.pk),
        }

        message_attributes = {
            'event_type': {
                'DataType': 'String',
                'StringValue': 'order_placed'
            }
        }

        self.sns_connection.publish_message_to_subscribers(settings.TRANSACTION_TOPIC_SNS, json.dumps(message), message_attributes)

    def create(self, purchase_data, user):
        ## Criar compra
        credit_card_data = purchase_data.pop('credit_card')
        credit_card_data['card_number'] = self.__mask_card(credit_card_data.pop('card_number'))

        products_pk = [product["product_id"] for product in purchase_data.pop('products')]
        products_list = self.product_domain.get_all(query_params={'pk__in': products_pk})

        purchase_data['user'] = self.user_domain.get(query_params={'username':user.username})
        purchase_data['total_price'] = self.__calculate_total_price(products_list)
        
        purchase = self.repository.create(purchase_data, credit_card_data)
        
        purchase.product.add(*list(products_list))
        self.repository.update_m2m(purchase)
        
        if settings.USAR_AWS:
            self.__notificate_transaction_sns(purchase)

        return purchase

