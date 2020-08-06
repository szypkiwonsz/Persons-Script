from playhouse.migrate import SqliteMigrator, migrate

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
        self.migrator = SqliteMigrator(self.db)
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

    def add_database_field(self, database_model, table_name, column_name, field):
        # Handling peewee.OperationalError: duplicate column name
        if not self.check_if_column_exist(table_name, column_name):
            migrate(self.migrator.add_column(table_name, column_name, field))
            database_model._meta.add_field(column_name, field)

    def check_if_column_exist(self, table_name, column_name):
        columns_meta_data = self.db.get_columns(table_name)
        for i, data in enumerate(columns_meta_data):
            retrieved_column_name = columns_meta_data[i][0]
            if column_name == retrieved_column_name:
                return True
        return False
