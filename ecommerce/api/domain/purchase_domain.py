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

    def __notificate_transaction_sns(self, purchase):
        products = purchase.product.all()
        seller = products[0].seller.pk
        message = {
                    "seller" : str(seller),
                    "purchase_date" :  purchase.created_at.strftime("%Y-%m-%d %H:%M:%S %Z"),
                    "purchase_id" : str(purchase.pk),
                    "total_price" : str(purchase.total_price)
        }

        message_attributes = {
            'event_type': {
                'DataType': 'String',
                'StringValue': 'order_placed'
            }
        }

        self.sns_connection.publish_message_to_subscribers(settings.TRANSACTION_TOPIC_SNS, json.dumps(message), message_attributes)


    def create(self, purchase_data):
        purchase = Purchase()
        products_pk = [product["id"] for product in purchase_data['products']]
        products_list = self.product_domain.get_all(query_params={'pk__in': products_pk})

        purchase.user = self.user_domain.get(query_params={'pk':purchase_data['user']})
        purchase.total_price = self.__calculate_total_price(products_list)
        
        purchase_dict = purchase.__dict__
        purchase_dict.pop('_state')
        purchase = self.repository.create(purchase.__dict__)
        
        purchase.product.add(*list(products_list))
        self.repository.update_m2m(purchase)
        
        self.__notificate_transaction_sns(purchase)

        return purchase

