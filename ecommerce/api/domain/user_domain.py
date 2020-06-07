from api.domain.domain_base import DomainServiceBase
from api.data_access.user_repository import UserRepository

class UserDomainService(DomainServiceBase):
    def __init__(self):
        super().__init__(UserRepository())
