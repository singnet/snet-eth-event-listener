import json
from infrastructure.repositories.contract_repository import ContractRepository
from common.boto_utils import BotoUtils, LambdaInvocationType
from config import AWS_REGION, EVENT_LISTENER_ARN
from constant import Status, StatusCode

contract_repo = ContractRepository()
boto_util = BotoUtils(region_name=AWS_REGION)


class TriggerListener:
    def __init__(self):
        pass

    @staticmethod
    def trigger_listener_for_all_the_contracts():
        # Get all the contracts
        contracts = contract_repo.get_contracts()

        # Trigger event listener for all the contracts asynchronously.
        for contract in contracts:
            contract_name = contract.contract_name
            payload = json.dumps({"contract_name": contract_name})
            response = boto_util.invoke_lambda(lambda_function_arn=EVENT_LISTENER_ARN,
                                               invocation_type=LambdaInvocationType.Event,
                                               payload=payload)
            if response["StatusCode"] == StatusCode.RequestAcceptedStatusCode:
                # notify slack channel
                return Status.SUCCESS
        return Status.FAILED
