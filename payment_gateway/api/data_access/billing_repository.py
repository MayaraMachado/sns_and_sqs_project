from api.data_access.repository_base import RepositoryBase
from api.models import Billing

class BillingRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Billing)
