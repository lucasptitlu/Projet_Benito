from asyncio.log import logger
from decimal import Decimal
from botocore.exceptions import ClientError
from app.Database.base import Base


class Clients(Base):
    """Encapsulates an Amazon DynamoDB table of Clients."""

    def init_table(self):
        self.table = self.dynamodb.Table("Clients")

    def credit_by_id(self, id, bonito):
        """
        Credit specific client with bonito

        """
        try:
            user = self.get_entry_by_id(id)
            self.table.update_item(
                Key={"id": id},
                UpdateExpression="set bonito=:r",
                ExpressionAttributeValues={":r": Decimal(user.get("bonito") + bonito)},
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as err:
            logger.error(
                "Couldn't update bonito %s. Here's why: %s: %s",
                bonito,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def add_client(self, name, email, bonito, bonitard):
        """
        Adds a client to the table.

        """
        try:
            items = self.get_all_table()
            # gets highest existing id to naturaly increase by one the id for new entry
            new_id = items[-1].get("id") + 1 if items else 0
            self.table.put_item(
                Item={
                    "id": new_id,
                    "name": name,
                    "email": email,
                    "bonito": bonito,
                    "bonitard": bonitard,
                }
            )
        except ClientError as err:
            logger.error(
                f"""Couldn't add {name} to clients table . """
                f"""Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}"""
            )
            raise
