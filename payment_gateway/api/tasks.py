from celery.decorators import task
from datetime import datetime, date, timedelta
from django.conf import settings
from api.external.sqs_base import SQSConnection
from api.domain.revenue_domain import RevenueDomainService

@task()
def verify_transaction_queue():
    revenue_domain = RevenueDomainService()
    sqs_connection = SQSConnection()

    print('aaaaa')

    queue_messages = sqs_connection.poll_queue_for_messages(settings.TRANSACTION_URL_QUEUE)
    if 'Messages' in queue_messages and len(queue_messages['Messages']) >= 1:
        print(queue_messages)
        for message in queue_messages['Messages']:
            message_body = message['Body']
            receipt_handle = message['ReceiptHandle']

            success = revenue_domain.process_purchase(message_body)
            if success:
                sqs_connection.delete_message_from_queue(settings.TRANSACTION_URL_QUEUE, receipt_handle)
    