import boto3
import logging
from django.conf import settings

class SQSConnection:

    def __init__(self):
        '''
            Instanciação do cliente SQS utilizando boto3;
            
            
            Returns:
            ---------

            sqs : pyboto3.sqs
                Instância sqs.
        '''
        self.sqs_client = boto3.client(
            'sqs', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1')

    def create_sqs_queue(self, queue_name):
        return self.sqs_client.create_queue(
            QueueName=queue_name
        )

    def find_queue(self, prefix):
        return self.sqs_client.list_queues(
            QueueNamePrefix=prefix
        )

    def list_all_queues(self):
        return self.sqs_client.list_queues()

    def poll_queue_for_messages(self, queue_url, max_messages_number=10):
        return self.sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages_number
        )

    def process_message_from_queue(self):
        queue_messages = poll_queue_for_messages()
        if 'Messages' in queue_messages and len(queue_messages['Messages']) >= 1:
            for message in queue_messages['Messages']:
                logging.warning(f"Processing message: {message['MessageId']} with text: {message['Body']}.")
                change_message_visibility_timeout(message['ReceiptHandle'])

    def delete_message_from_queue(self, queue_url, receipt_handle):
        return self.sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    def purge_queue(self, queue_url):
        return self.sqs_client.purge_queue(
            QueueUrl=queue_url
        )

