from django.db.models import Sum

from api.data_access.repository_base import RepositoryBase
from api.models import Billing

class BillingRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Billing)

    def sum_earned_value(self, seller_id):
        return self.model.objects.filter(seller_id=seller_id).aggregate(Sum('total_received'))