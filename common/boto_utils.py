import json

import boto3
from botocore.config import Config
from common.logger import get_logger

logger = get_logger(__name__)


class LambdaInvocationType:
    Event = "Event"
    RequestResponse = "RequestResponse"


class BotoUtils:
    def __init__(self, region_name):
        self.region_name = region_name

    def get_ssm_parameter(self, parameter, config=Config(retries={'max_attempts': 1})):
        """ Format config=Config(connect_timeout=1, read_timeout=0.1, retries={'max_attempts': 1}) """
        ssm = boto3.client('ssm', region_name=self.region_name, config=config)
        parameter = ssm.get_parameter(Name=parameter, WithDecryption=True)
        return parameter["Parameter"]["Value"]

    def invoke_lambda(self, lambda_function_arn, invocation_type, payload, config=Config(retries={'max_attempts': 1})):
        """ Format config=Config(connect_timeout=1, read_timeout=0.1, retries={'max_attempts': 1}) """
        lambda_client = boto3.client('lambda', region_name=self.region_name, config=config)
        lambda_response = lambda_client.invoke(FunctionName=lambda_function_arn, InvocationType=invocation_type,
                                               Payload=payload)
        if invocation_type == "Event":
            return lambda_response
        return json.loads(lambda_response.get('Payload').read())

    def publish_to_sns_topic(self, arn, payload, message_group_id, message_deduplication_id):
        client = boto3.client('sns', region_name=self.region_name)
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(payload)}),
            MessageStructure='json',
            MessageGroupId=message_group_id,
            MessageDeduplicationId=message_deduplication_id
        )
        return response
