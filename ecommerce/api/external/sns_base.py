import boto3
import logging
from django.conf import settings

class SNSConnection:

    def __init__(self):
        '''
            Create instance of SNS client using boto3;
            
            
            Returns:
            ---------

            sqs : pyboto3.sns
                Instância sns.
        '''
        self.sns_client = boto3.client(
            'sns', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1')

    def create_subscription(self, topic_arn, subscription_type, endpoint):
        '''
        '''

        return self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=subscription_type,
            Endpoint=endpoint,
            Attributes={
                "FilterPolicy" : {
                            "event_type": [
                                "order_placed",
                                "order_cancelled"
                            ]
                        }
                }
        )

    def get_topic_subscriptions(self, topic_arn):
        return self.sns_client.list_subscriptions_by_topic(
            TopicArn=topic_arn
        )

    def opt_out_of_subscription(self, topic_arn, endpoint, subscription_type):
        subscriptions = get_topic_subscriptions(topic_arn)

        for subscription in subscriptions['Subscriptions']:
            if subscription['Protocol'] == subscription_type and subscription['Endpoint'] == endpoint:
    
                logging.warning(f"Unsubscribing {subscription['Endpoint']}")
                subscription_arn = subscription['SubscriptionArn']
                self.sns_client.unsubscribe(SubscriptionArn=subscription_arn)

    def publish_message_to_subscribers(self, topic_arn, message, message_attributes={}):
        publish = self.sns_client.publish(
                                            TopicArn=topic_arn,
                                            Message=message,
                                            MessageAttributes = message_attributes
                                        )
        return publish
