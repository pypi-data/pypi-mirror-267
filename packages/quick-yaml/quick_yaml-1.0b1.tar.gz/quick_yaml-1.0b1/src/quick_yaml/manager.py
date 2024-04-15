import jmespath

from .data_structures import BYAML, NestedDict
from .parser import QueryProcessor
import pandas as pd
import copy


class MetaData:
    def __init__(self):
        """
        Initialize the object with an empty dictionary for storing tables.
        """
        self.tables = {}  # A dictionary to hold table-specific metadata

    def add_table(self, table_name, unique_columns=None, indexes=None):
        """
        Add a new table to the metadata.
        Parameters:
            table_name (str): The name of the table.
            unique_columns (list): A list of unique columns for the table.
            indexes (list): A list of indexes for the table.
        Returns:
            None
        """
        self.tables[table_name] = {
            'version': 1.0,
            'unique_columns': unique_columns or [],
            'indexes': indexes or []
        }

    def to_dict(self):
        """
        Return a dictionary representation of the object.
        """
        return self.tables

    def get_unique_columns(self, table_name):
        """Returns the unique columns for the given table."""
        return self.tables[table_name]['unique_columns']

    def get_indexes(self, table_name):
        """Returns the indexes for the given table."""
        return self.tables[table_name]['indexes']


class QYAMLDB:
    """
    quick_yaml class represents a simple in-memory database system.

    Methods:
        - __init__: Initialize the database.
        - add_table: Add a table to the database.
        - insert_data: Insert data into a specified table.
        - query_data: Query data from a specified table.
        - delete_data: Delete data from a specified table.
    """
    def __init__(self, path, key_file='key.file', encrypted=False,byaml=None):
        """
          Initializes the quick_yaml instance.
          Parameters:
              path (str): The file path for the database.
              key_file (str): The file path for the encryption key. Defaults to 'key.file'.
              encrypted (bool): Flag indicating whether encryption is enabled. Defaults to False.
              byaml (BYAML): An existing BYAML instance. If not provided, a new BYAML instance is created.
          Raises:
              ValueError: If the file format is invalid.
          Returns:
              None
          """
        if not path.endswith('.ezdb'):
            raise ValueError('Invalid file format. Must use ".ezdb" extension.')
        self.path = path
        self.key_file = key_file
        self.encrypted = encrypted
        self.transaction_mode = False
        self._backup_table = None
        self.byaml = byaml or BYAML(self.path, encryption_enabled=self.encrypted, key_file=self.key_file)
        self.tables: dict = {}  # Use a dict to manage multiple tables, each with its data and metadata

    def save_db(self):
        """Saves the current state of the database to a file."""

        to_save = {table_name: {'metadata': table_info['metadata'].to_dict(),
                                'data': table_info['data'].to_dict()} for table_name, table_info in
                   self.tables.items()}
        self.byaml.encode_to_binary_yaml(to_save)

    def create_table(self, table_name, unique_columns=None, indexes=None):
        """
        Creates a new table in the database.

        Parameters:
            table_name (str): The name of the table to create.
            unique_columns (list, optional): List of column names that should be unique. Defaults to None.
            indexes (list, optional): List of column names to index. Defaults to None.
        Returns:
            str: "done." if the table is created successfully.
        Raises:
            ValueError: If the table already exists.
        """
        if table_name in self.tables:
            raise ValueError(f"Table '{table_name}' already exists.")
        metadata = MetaData()
        metadata.add_table(table_name, unique_columns, indexes)  # MetaData is adjusted to handle this
        self.tables[table_name] = {
            'metadata': metadata,
            'data': NestedDict()
        }
        self.save_db()
        return "done."

    def load_db(self):
        """
        Load the database by decoding the contents from binary YAML and populating the tables dictionary with metadata
         and data.

        Returns:
            None
        """
        contents = self.byaml.decode_from_binary_yaml(type_dict='dict')

        try:
            for table_name, table_info in contents.items():
                metadata = MetaData()
                metadata.tables[table_name] = table_info['metadata']  # Properly load metadata
                self.tables[table_name] = {
                    'metadata': metadata,
                    'data': NestedDict(table_info['data'])
                }
        except Exception:
            print("WARNING CANNOT LOAD META DATA")

    def insert_new_data(self, table_name, data):
        """
        Insert new data into the specified table.

        Parameters:
            table_name (str): Name of the table to insert data into.
            data (dict): Data to be inserted into the table.

        Returns:
            str: A message indicating the insertion operation is done.

        Raises:
            ValueError: If the table does not exist or if a unique constraint is violated.
        """

        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Check for unique constraints
        unique_columns = self.tables[table_name]['metadata'].get_unique_columns(table_name)
        for column in unique_columns:
            if column in data and any(
                    data[column] == row.get(column) for row in self.tables[table_name]['data'].get_dict().values()):
                raise ValueError(f"Unique constraint violated for column: {column}")

        # Get existing IDs as integers
        existing_ids = [int(key) for key in self.tables[table_name]['data'].get_dict().keys()]

        # Find missing IDs if there are any gaps
        missing_ids = [i for i in range(1, max(existing_ids) + 1) if i not in existing_ids] if existing_ids else []

        # Use the first missing ID if available; otherwise, use the next highest ID
        entry_id = str(missing_ids[0]) if missing_ids else str(max(existing_ids) + 1 if existing_ids else 1)

        # Insert the data with the new entry_id
        self.tables[table_name]['data'][entry_id] = data
        self.save_db()
        return 'done'

    def insert_many(self, table_name, list_of_values):
        """
        Insert multiple values into the specified table.
        Parameters:
            table_name (str): Name of the table to insert data into.
            list_of_values (list): List of values to be inserted into the table.
        Returns:
            str: A message indicating the insertion operation is done.
        """
        try:
            for i in list_of_values:
                if type(i) is dict or isinstance(i, NestedDict):
                    self.insert_new_data(table_name, i)
                    return 'done'
        except Exception:
            print("Error inserting values")

    def get_data_by_id(self, table_name, entry_id):
        """
        A function that retrieves data by ID from a specific table.

        Parameters:
            table_name (str): The name of the table to retrieve data from.
            entry_id (int): The ID of the entry to retrieve.

        Returns:
            contents: The data associated with the provided entry ID in the specified table.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table Not found.")
        contents = self.tables[table_name]['data'].get(str(entry_id), None)
        return contents

    def update_entry(self, table_name, entry_id, updated_data):
        """Updates the data by given ID.
        Parameters:
            table_name (str): Name of the table
            entry_id (str): ID of the entry
            updated_data (NestedDict/Dict): Data to be updated.
        """
        if table_name not in self.tables or entry_id not in self.tables[table_name]['data'].get_dict():
            raise ValueError("Table or entry does not exist.")
        print(
            f"DEBUG Table {self.tables[table_name]['data'][entry_id]} type{type(self.tables[table_name]['data'][entry_id])}")
        if entry_id not in self.tables[table_name]['data']:
            return KeyError("Entry does not exist.")
        self.tables[table_name]['data'][entry_id].update(updated_data)
        self.save_db()
        return 'done'

    def update_many(self, table_name, condition, update_data, flags=None):
        """ Updates data based on given condition
        Parameters:
            condition (dict): Filtering Conditions.
            update_data (dict): Data to be updated
            flags: Additional flags (Supported: { add_missing_values : 'True'/False})
            table_name: name of table """
        if flags is None:
            flags = {'add_missing_values': True}
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Retrieve the metadata to check for unique constraints
        unique_columns = self.tables[table_name]['metadata'].get_unique_columns(table_name)
        qp = QueryProcessor(self.tables[table_name])
        qp.filter_id(condition)
        matching_ids = qp.results

        if not matching_ids:
            return None  # No data matching the condition

        for entry_id in matching_ids:
            current_entry = self.tables[table_name]['data'].get(entry_id)

            for key, value in update_data.items():
                # Check if the key exists in the entry or if missing keys should be added
                if key in current_entry or flags.get('add_missing_keys', False):
                    # Check for unique constraints
                    if key in unique_columns and any(
                            value == row.get(key) for row in self.tables[table_name]['data'].get_dict().values()
                            if row.get(key) is not None and str(row.get('id')) != entry_id):
                        raise ValueError(f"Unique constraint violated for column: {key}")

                    # Update or add the key-value pair
                    if isinstance(value, dict) and isinstance(current_entry.get(key, None), dict):
                        # For nested dicts, update sub-keys
                        current_entry[key].update(value)
                    else:
                        current_entry[key] = value

            # Update the entry in the dataset
            self.tables[table_name]['data'][entry_id] = current_entry

        self.save_db()
        return 'done'

    def delete_entry(self, table_name, entry_id):
        """
        Delete an entry from a specified table.
        Parameters:
            table_name (str): The name of the table to delete the entry from.
            entry_id (str): The unique identifier of the entry to be deleted.

        Raises:
            ValueError: If the table or entry does not exist.
            KeyError: If the entry does not exist.

        Returns:
            str: "done" if the deletion is successful.
        """
        if table_name not in self.tables or entry_id not in self.tables[table_name]['data'].get_dict().keys():
            raise ValueError("Table or entry does not exist.")
        if entry_id not in self.tables[table_name]['data']:
            return KeyError("Entry does not exist.")
        del self.tables[table_name]['data'][entry_id]
        self.save_db()
        return "done"

    def delete_many(self, table_name, condition):
        """
           Delete multiple records from a table based on a given condition.
           Parameters:
               table_name (str): The name of the table to delete records from.
               condition (dict): The condition to filter the records to be deleted.
           Raises:
               ValueError: If the table does not exist in the database.
           Returns:
               str: A message confirming the deletion process is done.
           """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Retrieve the metadata to check for unique constraints
        qp = QueryProcessor(self.tables[table_name])
        qp.filter_id(condition)
        matching_ids = qp.results
        # for each matching records, delete the record
        for entry_id in matching_ids:
            del self.tables[table_name]['data'][entry_id]
        self.save_db()
        return "done"

    def find_jmes(self, table_name, query):
        """
        Finds data in the specified table based on a query.
        This uses Jmespath query to find the data in the dictionary
        Parameters:
            table_name (str): The name of the table to search in.
            query (dict): The query to filter the data.
        Returns:
            list: The results of the query execution.
        Raises:
            ValueError: If the table does not exist in the database.
        """
        # Placeholder for query processing logic
        if table_name not in self.tables:
            raise ValueError("Table or entry does not exist.")

        data_list = list(self.tables[table_name]['data'].get_dict().values())

        return jmespath.search(query, data_list)

    def execute_query(self, table_name, query):
        """
           Executes a query on a specific table and returns the results.

           Parameters:
               table_name (str): The name of the table to execute the query on.
               query (dict): The query to be executed.

           Returns:
               dict: The results of the query execution.
           """
        # check if table exists
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        data = self.tables[table_name]['data'].to_dict()
        executor = QueryProcessor(data)
        executor.process_query(query)
        return executor.results

    def find(self, table_name, query):
        """
           Finds and filters data in the specified table based on a query.
           Parameters:
               table_name (str): The name of the table to search in.
               query (dict): The query to filter the data.
           Returns:
               dict: The filtered results based on the query.
           """
        data = self.tables[table_name].to_dict()
        executor = QueryProcessor(data)
        executor.filter(query)
        return executor.results

    def find_all(self, table_name):
        """
        Returns all the data in the specified table.
        Parameters:
            table_name (str): The name of the table to search in.
        Returns:
            list: The results of the query execution.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        return self.tables[table_name]['data'].values()

    def to_pandas(self, table_name):
        """
        Converts the specified table data into a pandas DataFrame.

        Parameters:
            table_name (str): The name of the table to convert.

        Returns:
            pandas.DataFrame: The converted DataFrame.

        Raises:
            ValueError: If the table does not exist in the database.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Extract data from the specified table
        data = self.tables[table_name]['data'].to_dict()

        # Flatten the data and convert it into a format suitable for DataFrame creation
        flattened_data = []
        for entry_id, entry_data in data.items():
            entry_data_flat = {'obj_id': entry_id}
            for key, value in entry_data.items():
                if isinstance(value, list):
                    entry_data_flat[key] = ', '.join(map(str, value))  # Convert lists to comma-separated strings
                else:
                    entry_data_flat[key] = value
            flattened_data.append(entry_data_flat)

        # Create and return the DataFrame
        df = pd.DataFrame(flattened_data)
        return df

    def begin_transaction(self, data, break_on_invalid_command=True):
        """
        Emulates a transaction processing system.

        Parameters:
            data (dict): Dictionary data to be processed
            break_on_invalid_command (bool): Flag that is used to indicate whether to break on invalid translations.

        Returns:
            dict: A dictionary containing the status, error message, and transaction details.
        """

        # Create a backup copy of the tables
        self._backup_table = copy.deepcopy(self.tables)

        # Initialize transaction report
        transaction_report = {
            'successful_operations': 0,
            'failed_operation': 0,
            'list_of_failed_operations': []
        }

        # Get the transactional data and error strategy from input data
        transactional_data = data.get('$operations', [])
        error_strategy = data.get('$error_strategy', 'rollback')

        # Ensure error_strategy is valid
        if error_strategy not in ('rollback', 'continue', 'break'):
            error_strategy = 'rollback'

        for i in transactional_data:
            try:
                status = self.execute_command(i)
                if status == 'Invalid command' and break_on_invalid_command:
                    break
                transaction_report['successful_operations'] += 1
            except Exception as e:
                if error_strategy == 'rollback':
                    self.tables = self._backup_table
                    transaction_report['failed_operation'] += len(transactional_data) - transaction_report[
                        'successful_operations']
                    return {'status': 'Failure', 'error_message': str(e), 'details': transaction_report}
                elif error_strategy == 'break':
                    transaction_report['failed_operation'] += len(transactional_data) - transaction_report[
                        'successful_operations']
                    return {'status': 'Failure', 'error_message': str(e), 'details': transaction_report}
                elif error_strategy == 'continue':
                    transaction_report['list_of_failed_operations'].append(i)
                    continue

        # Determine final status based on failed operations
        stat = "Success" if len(transaction_report['list_of_failed_operations']) == 0 else "Finished with errors"
        return {'status': stat, 'error_message': None, 'details': transaction_report}

    def execute_command(self, i):
        """
        Execute a command based on the given input type.
        Parameters:
            i (dict): The input command to be executed.
        Returns:
            str: The result of the executed command.
        """
        translation_operations = ['$insert', '$insert_many', '$update', '$update_many', '$delete'
            , '$delete_many', '$del_many', '$del']
        if i['type'] not in translation_operations:
            return "Invalid operation detected."
        if i['type'] == '$insert':
            return self.insert_new_data(i['$table_name'], i['$data'])
        elif i['type'] == '$insert_many':
            return self.insert_many(i['$table_name'], i['data'])
        elif i['type'] == '$update':
            return self.update_entry(i['$table_name'], i['$obj_id'], i['$data'])
        elif i['type'] == '$update':
            return self.update_many(i['$table_name'], i['$obj_id'], i['$data'])
        elif i['type'] == '$update_many':
            return self.update_many(i['$table_name'], i['$condition'], i['$data'], i.get('$flags',
                                                                                         {'add_missing_values': True}))
        elif i['type'] == '$delete' or '$del':
            return self.delete_entry(i['$table_name'], i['$obj_id'])
        elif i['type'] == '$delete_many' or '$del_many':
            return self.delete_many(i['$table_name'], i['$condition'])
        elif i['type'] == '$create_table':

            return self.create_table(i['$table_name'], i['$unique_columns'], None)
        elif i['type'] == '$query':
            return self.execute_query(i['$table_name'], i['$query_data'])
