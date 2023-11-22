from asyncio.log import logger
from botocore.exceptions import ClientError
from operator import itemgetter
import boto3

DEFAULT_RESSOURCE = boto3.resource("dynamodb", region_name="eu-north-1")


class Clients:
    """Encapsulates an Amazon DynamoDB table of Clients."""

    def __init__(self, dyn_resource=DEFAULT_RESSOURCE):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dynamodb = dyn_resource
        self.table = self.dynamodb.Table("Clients")

    def get_client_by_id(self, id):
        response = self.table.get_item(
            Key={
                "id": id,
            }
        )
        item = response["Item"]
        return item

    def get_all_clients(self):
        unordered_client_list = self.table.scan()["Items"]
        return sorted(unordered_client_list, key=itemgetter("id"))

    def add_client(self, name, email, bonito, balance):
        """
        Adds a client to the table.

        """
        try:
            items = self.get_all_clients()
            # gets highest existing id to naturaly increase by one the id for new entry
            new_id = items[-1].get("id") + 1
            self.table.put_item(
                Item={
                    "id": new_id,
                    "name": name,
                    "email": email,
                    "bonito": bonito,
                    "balance": balance,
                }
            )
        except ClientError as err:
            logger.error(
                f"""Couldn't add {name} to clients table . """
                f"""Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}"""
            )
            raise
