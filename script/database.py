import models


class Database:
    def __init__(self, db_path):
        """
        Object that initiates database connection

        :param db_path: <string>, database path
        """
        self.db_path = db_path
        self.db = models.db
        self.models = models.MODELS
        self.initialize()

    def __del__(self):
        self.close_connection()

    def initialize(self):
        """
        Creates the database and the table if they don't exist
        """
        self.db.init(self.db_path)
        self.open_connection()
        self.create_tables()

    def open_connection(self):
        self.db.connect()

    def close_connection(self):
        self.db.close()

    def create_tables(self):
        self.db.create_tables(self.models)
