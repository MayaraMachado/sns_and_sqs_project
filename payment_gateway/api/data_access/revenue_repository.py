from django.db.models import Sum

from api.data_access.repository_base import RepositoryBase
from api.models import Revenue

class RevenueRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Revenue)

    def sum_earned_value(self, seller_id):
        return self.model.objects.filter(seller_id=seller_id).aggregate(Sum('total_value'))
