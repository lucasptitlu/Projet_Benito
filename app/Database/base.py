from abc import ABC, abstractmethod
from operator import itemgetter
import boto3

DEFAULT_RESSOURCE = boto3.resource("dynamodb", region_name="eu-north-1")


class Base(ABC):
    """Encapsulates an Amazon DynamoDB table of Clients."""

    def __init__(self, dyn_resource=DEFAULT_RESSOURCE):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dynamodb = dyn_resource
        self.init_table()

    @abstractmethod
    def init_table(self):
        pass

    def get_entry_by_id(self, id):
        response = self.table.get_item(
            Key={
                "id": id,
            }
        )
        item = response["Item"]
        return item

    def get_all_table(self):
        unordered_client_list = self.table.scan()["Items"]
        return sorted(unordered_client_list, key=itemgetter("id"))
