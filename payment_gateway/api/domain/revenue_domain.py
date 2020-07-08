import json
from datetime import datetime
from api.domain.domain_base import DomainServiceBase
from api.data_access.revenue_repository import RevenueRepository
from api.models import Revenue

class RevenueDomainService(DomainServiceBase):
    def __init__(self):
        super().__init__(RevenueRepository())

    def process_purchase(self, message):
        
        message = json.loads(message)
        message = json.loads(message['Message'])
        
        items = message.pop('items')
        purchase_id = message.pop('purchase_id')
        purchase_date = datetime.strptime(message['purchase_date'], "%Y-%m-%d %H:%M:%S %Z")

        revenues = []
        for item in items.keys():
            revenues.append(Revenue(seller_id=item, purchase_id=purchase_id, 
                                    total_value=items[item], purchase_date=purchase_date
                                    )
                            )
        self.repository.bulk_create(revenues)

        return True

    def get(self, seller_id):
        response = {'seller_id' : seller_id,}
        total_received = self.repository.sum_earned_value(seller_id)
        total_received['total_received'] = total_received.pop('total_value__sum')
        response.update(total_received)

        return response
        