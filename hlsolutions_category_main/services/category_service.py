from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from ..errors.custom_exceptions import ServerError
from decouple import config

auth_provider = PlainTextAuthProvider(
    username=config('CASSANDRA_USERNAME'),
    password=config('CASSANDRA_PASSWORD')
)

cluster = Cluster(
    auth_provider=auth_provider
)

session = cluster.connect(config('CASSANDRA_KEYSPACE'))

class CategoryService:
    """
    This class provides methods to interact with the categories table in the database.
    """

    def get_all(self):
        """
        Retrieves all categories from the database.

        Returns:
            list: A list of dictionaries representing the categories.
        
        Raises:
            ServerError: If there are no categories to get.
            ServerError: If there is an error trying to get the categories.
        """
        try:
            result = session.execute("SELECT * FROM categories;")
            if len(result.current_rows) > 0:
                return [dict(row._asdict()) for row in result]
            else:
                raise ServerError("There are no categories to get.", 404)
        except Exception as error:
            if isinstance(error, ServerError):
                raise error
            raise ServerError("Error trying to get the categories.", 500)

    def get_by_id(self, id_category):
        """
        Retrieves a category by its ID.

        Args:
            id_category (str): The ID of the category to retrieve.

        Returns:
            dict: A dictionary representing the category.

        Raises:
            ServerError: If the category is not found.
            ServerError: If there is an error trying to get the category.
        """
        try:
            result = session.execute("SELECT * FROM categories WHERE id_category = %s", [id_category])
            if len(result.current_rows) > 0:
                return dict(result.one()._asdict())
            else:
                raise ServerError("Category not found.", 404)
        except Exception as error:
            if isinstance(error, ServerError):
                raise error
            raise ServerError("Error trying to get the category.", 500)

    def create_category(self, name):
        """
        Creates a new category.

        Args:
            name (str): The name of the category.

        Returns:
            result: The result of the database operation.

        Raises:
            ServerError: If there is an error trying to create the category.
        """
        try:
            result = session.execute(
                "INSERT INTO categories (id_category, name) VALUES (uuid(), %s)",
                (name,)
            )
            return result
        except Exception as error:
            if isinstance(error, ServerError):
                raise error
            raise ServerError("Error trying to create the category.", 500)

    def update_category(self, id_category, name):
        """
        Updates a category.

        Args:
            id_category (str): The ID of the category to update.
            name (str): The new name of the category.

        Raises:
            ServerError: If the category is not found.
            ServerError: If there is an error trying to update the category.
        """
        try:
            result_id = session.execute("SELECT id_category FROM categories WHERE id_category = %s", (id_category,))
            if not result_id.one():
                raise ServerError("Category not found.", 404)
            
            update_query = "UPDATE categories SET name = %s WHERE id_category = %s"
            session.execute(update_query, (name, id_category))
        except Exception as error:
            if isinstance(error, ServerError):
                raise error
            raise ServerError("Error trying to update the category.", 500)

    def delete_category(self, id_category):
        """
        Deletes a category.

        Args:
            id_category (str): The ID of the category to delete.

        Raises:
            ServerError: If the category is not found.
            ServerError: If there is an error trying to delete the category.
        """
        try:
            result_id = session.execute("SELECT id_category FROM categories WHERE id_category = %s", (id_category,))
            if not result_id.one():
                raise ServerError("Category not found.", 404)
            session.execute("DELETE FROM categories WHERE id_category = %s", (id_category,))
        except Exception as error:
            if isinstance(error, ServerError):
                raise error
            raise ServerError("Error trying to delete the category.", 500)

category_service = CategoryService()