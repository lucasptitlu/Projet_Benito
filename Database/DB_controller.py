import boto3

DEFAULT_RESSOURCE = boto3.resource("dynamodb", region_name="eu-north-1")
def get_client_by_id(id):
    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
    table = dynamodb.Table("Clients")
    response = table.get_item(
        Key={
            "id": id,
        }
    )
    item = response["Item"]
    return item


class Clients:
    """Encapsulates an Amazon DynamoDB table of movie data."""

    def __init__(self, dyn_resource: DEFAULT_RESSOURCE):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None

    def add_movie(self, title, year, plot, rating):
        """
        Adds a movie to the table.

        :param title: The title of the movie.
        :param year: The release year of the movie.
        :param plot: The plot summary of the movie.
        :param rating: The quality rating of the movie.
        """
        try:
            self.table.put_item(
                Item={
                    "year": year,
                    "title": title,
                    "info": {"plot": plot, "rating": Decimal(str(rating))},
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't add movie %s to table %s. Here's why: %s: %s",
                title,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
