from api.domain.domain_base import DomainServiceBase
from api.data_access.product_repository import ProductRepository

class ProductDomainService(DomainServiceBase):
    def __init__(self):
        super().__init__(ProductRepository())
