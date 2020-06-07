from celery.decorators import task
from datetime import datetime, date, timedelta
from django.conf import settings
from api.external.sqs_base import SQSConnection
from api.domain.billing_domain import BillingDomainService

@task()
def verify_transaction_queue():
    billing_domain = BillingDomainService()
    sqs_connection = SQSConnection()

    queue_messages = sqs_connection.poll_queue_for_messages(settings.TRANSACTION_URL_QUEUE)
    print(queue_messages)
    if 'Messages' in queue_messages and len(queue_messages['Messages']) >= 1:
        for message in queue_messages['Messages']:
            message_body = message['Body']
            receipt_handle = message['ReceiptHandle']

            success = billing_domain.process_purchase(message_body)
            if success:
                sqs_connection.delete_message_from_queue(settings.TRANSACTION_URL_QUEUE, receipt_handle)
    