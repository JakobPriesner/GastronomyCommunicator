import json
import logging
from pathlib import Path


class TableList:
    def __init__(self):
        self.table_list = []
        self.load_stored_tables()
        self.table_anz = 0

    def load_stored_tables(self):
        # load the stored table_list
        with open(relPath + "table_list.json") as table_list_file:
            stored_table_list = json.load(table_list_file)
            for table in stored_table_list.keys():
                # add the stored tables to table_list
                self.table_list[table] = Table(table, stored_table_list[table]["table_name"])
                self.table_anz += 1

    def log_in(self, table_id, connection):
        self.get_table_by_id(table_id).connection = connection

    def register_table(self, table_id, table_number):
        if self.get_table_by_id(table_id):
            logging.info(f'Table with ID {table_id} already exists.')
        else:
            self.table_list.append(Table(table_id, table_number))
            self.table_anz += 1

    def delete_table(self, table_id):
        # here is really meant the deleting of a table, not the "logging out"
        del self.table_list[table_id]

    def get_table_by_id(self, table_id):
        for table in self.table_list:
            if table.id == table_id:
                return table
        return False

    def get_table_list_in_json(self):
        # returns the data of a table in json format
        temp_table_list = {}
        for table in self.table_list:
            temp_table_list[table.id] = table.get_table_in_json()
        return temp_table_list

    def to_string(self):
        return '----TABLE-LIST----\n' + json.dumps(self.get_table_list_in_json(), indent=4, sort_keys=True)


class Table:
    def __init__(self, table_id, table_number):
        self.id = table_id
        self.table_number = table_number
        self.actions = []
        self.connection = None

    def get_table_in_json(self):
        return {"id": self.id, "table_number": self.table_number, "actions": self.actions}


relPath = str(Path(__file__).parent) + '/'