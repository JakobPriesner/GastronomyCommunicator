import json
import logging
from pathlib import Path


class WaitorList:
    def __init__(self):
        logging.debug('Init WaitorList')
        self.stored_waitor = {}
        self.waitor_list = []
        self.waitor_anz = 0

    def laod_stored_waitor(self):
        # load all saved (already registered) waiters
        with open(relPath + "waitor_list.json") as waitor_list_file:
            stored_waitor_list = json.load(waitor_list_file)
            for waitor in stored_waitor_list.keys():
                self.stored_waitor[waitor] = stored_waitor_list[waitor]

    def log_in(self, user_name, password):
        # already registered waiter logged in to work
        for waitor in self.stored_waitor:
            if user_name == self.stored_waitor[waitor]["user_name"] \
                    and password == self.stored_waitor[waitor]["password"]:
                # waitor entered valid access data
                temp_waitor = Waitor(waitor, user_name, password, is_working=True)
                self.waitor_list.append(temp_waitor)
                self.waitor_anz += 1
                return 'ok'
        return 'err'

    def log_out(self, waitor_id):
        # Deletes the waiter from the list of active waiters and returns his pending orders so that they can
        # be redistributed
        waitor = self.get_waitor_by_id(waitor_id)
        waitor.is_working = False
        self.waitor_list.remove(waitor)
        self.waitor_anz -= 1
        return waitor.active_orders

    def register_waitor(self, waitor_id, user_name, user_password):
        # adds a waiter who is not yet registered in the system
        self.stored_waitor[waitor_id] = {"user_name": user_name, "password": user_password}

    def store_waitor_list(self):
        # prepare waiter (deletes all data that is no longer relevant)
        for waitor in self.waitor_list:
            waitor.active_orders = []
            waitor.is_available = False
            waitor.is_working = False
            waitor.connection = None

        with open(relPath + 'waitor_list.json', 'w') as file:
            json.dump(self.get_waitor_list_in_json(), file, indent=4, sort_keys=True)

    def get_waitor_by_id(self, waitor_id):
        # returns the object of a waiter by his ID
        for waitor in self.waitor_list:
            if waitor.id == waitor_id:
                return waitor
        # otherwise the waiter does not exist in the system
        logging.warning(f'Waitor with ID {waitor_id} not found!')

    def get_waitor_by_name(self, user_name):
        # return the object of a waitor by his name
        for waitor in self.waitor_list:
            if waitor.user_name == user_name:
                return waitor
        # otherwise the waiter does not exist in the system
        logging.warning(f'Waitor with UserName {user_name} not found!')

    def get_waitor_list_in_json(self):
        # returns the data of a waiter in json format
        temp = {}
        for waitor in self.waitor_list:
            temp[waitor.id] = waitor.get_waitor_in_json()
        return temp

    def to_string(self):
        return '----WAITOR-LIST----\n' + json.dumps(self.get_waitor_list_in_json(), indent=4, sort_keys=True)


class Waitor:
    def __init__(self, waitor_id, user_name, user_password, is_working=False):
        self.id = waitor_id
        self.is_available = False  # means, if the waitor is working or in the toilet, ...
        self.is_working = is_working
        self.active_orders = []
        self.user_name = user_name
        self.password = user_password
        self.connection = None

    def absolve_action(self, waitor_id):
        for action in self.active_orders:
            if action["id"] == waitor_id:
                self.active_orders.remove(action)

    def send_action(self):
        pass

    def get_waitor_in_json(self):
        return {"id": self.id, "is_available": self.is_available, "active_orders": self.active_orders,
                "user_name": self.user_name, "password": self.password}

    def to_string(self):
        output = f'\nID {self.id}: {self.user_name}\n'
        output += 'is working\n' if self.is_working else 'doesn´t work\n'
        for order in self.active_orders:
            output += '     ' + order.to_string() + '\n'
        output += '\n-----------------'

        return output


relPath = str(Path(__file__).parent) + '/'