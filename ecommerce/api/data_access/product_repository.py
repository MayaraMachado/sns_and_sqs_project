from api.data_access.repository_base import RepositoryBase
from api.models import Product

class ProductRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Product)
