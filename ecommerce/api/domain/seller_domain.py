from api.domain.domain_base import DomainServiceBase
from api.data_access.seller_repository import SellerRepository

class SellerDomainService(DomainServiceBase):
    def __init__(self):
        super().__init__(SellerRepository())
