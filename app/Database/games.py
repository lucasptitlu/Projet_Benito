from asyncio.log import logger
from botocore.exceptions import ClientError

from app.Database.base import Base


class Games(Base):
    """Encapsulates an Amazon DynamoDB table of Games."""

    def init_table(self):
        self.table = self.dynamodb.Table("Games")

    def add_game(self, name, category, min_ration, hour_ratio):
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
                    "category": category,
                    "min_ration": min_ration,
                    "hour_ratio": hour_ratio,
                }
            )
        except ClientError as err:
            logger.error(
                f"""Couldn't add {name} to games table . """
                f"""Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}"""
            )
            raise
