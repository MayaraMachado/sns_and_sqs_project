from api.data_access.repository_base import RepositoryBase
from api.models import Purchase

class PurchaseRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Purchase)

    def create(self, dict_obj):
        return self.model.objects.create(**dict_obj)

    def update_m2m(self, obj):
        obj.save()
