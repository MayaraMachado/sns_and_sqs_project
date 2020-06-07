class DomainServiceBase:
    def __init__(self, repository):
        self.repository = repository

    def update(self, obj, updated_data={}):
        self.repository.update(obj, updated_data)

    def delete(self, obj):
        self.repository.delete(obj)

    def create(self, obj):
        obj = self.repository.inserir(obj)
        return obj

    def get_all(self, query_params={}, orderby=[], select_related=[]):
        return self.repository.get_all(query_params, orderby, select_related)

    def get(self, query_params={}, select_related=[]):
        return self.repository.get(query_params, select_related)
