import json
from datetime import datetime
from api.domain.domain_base import DomainServiceBase
from api.data_access.billing_repository import BillingRepository
from api.models import Billing

class BillingDomainService(DomainServiceBase):
    def __init__(self):
        super().__init__(BillingRepository())

    def process_purchase(self, message):
        
        message = json.loads(message)
        message = json.loads(message['Message'])
        message['seller_id'] = message.pop('seller')
        message['total_received'] = message.pop('total_price')
        message['purchase_date'] = datetime.strptime(message['purchase_date'], "%Y-%m-%d %H:%M:%S %Z")
    
        billing = Billing(**message)
        self.repository.create(billing)

        return True

    def get(self, seller_id):
        response = {'seller_id' : seller_id,}
        total_received = self.repository.sum_earned_value(seller_id)
        total_received['total_received'] = total_received.pop('total_received__sum')
        response.update(total_received)

        return response
        