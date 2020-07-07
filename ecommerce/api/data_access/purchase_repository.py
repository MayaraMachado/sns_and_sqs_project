from api.data_access.repository_base import RepositoryBase
from api.models import Purchase, CreditCard
from django.db import transaction

class PurchaseRepository(RepositoryBase):
    def __init__(self):
        self.credit_card_model = CreditCard
        super().__init__(Purchase)

    def create(self, purchase_data, credit_card_data):
        with transaction.atomic():
            credit_card = self.credit_card_model.objects.create(**credit_card_data)
            purchase_data['credit_card_id'] = credit_card.card_id
            purchase = self.model.objects.create(**purchase_data)
        return purchase

    def update_m2m(self, obj):
        obj.save()
