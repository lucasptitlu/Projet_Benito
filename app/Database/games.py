from asyncio.log import logger
from datetime import datetime
from botocore.exceptions import ClientError

from app.Database.base import Base


class Games(Base):
    """Encapsulates an Amazon DynamoDB table of Games."""

    def init_table(self):
        self.table = self.dynamodb.Table("Games")

    def start_game(self, id: int):
        self.table.update_item(
            Key={"id": id},
            UpdateExpression="set start_time=:r,in_use=:p ",
            ExpressionAttributeValues={
                ":r": datetime.now().strftime("%D-%H:%M:%S"),
                ":p": True,
            },
            ReturnValues="UPDATED_NEW",
        )

    def end_game(self, id: int):
        game = self.get_entry_by_id(id)
        self.table.update_item(
            Key={"id": id},
            UpdateExpression="set in_use=:p ",
            ExpressionAttributeValues={
                ":p": False,
            },
            ReturnValues="UPDATED_NEW",
        )
        breakpoint()
        # ca marche pas

        return datetime.now().strftime("%D-%H:%M:%S") - game.get("start_time")

    # datetime.strptime(
    #         game.get("start_time"), "%d/%m/%y-%H:%M:%S"
    #     )
    # return datetime.now() - game.get("start_time")

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
                    "in_use": False,
                    "start_time": None,
                }
            )
        except ClientError as err:
            logger.error(
                f"""Couldn't add {name} to games table . """
                f"""Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}"""
            )
            raise
