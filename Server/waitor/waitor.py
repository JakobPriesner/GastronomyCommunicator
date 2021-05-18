import json
import logging
from pathlib import Path


class WaitorList:
    def __init__(self):
        self.stored_waitor = {}
        self.waitor_list = []
        self.waitor_anz = 0

    def laod_stored_waitor(self):
        # load all saved (already registered) waiters
        with open(relPath + "waitor_list.json") as waitor_list_file:
            stored_waitor_list = json.load(waitor_list_file)
            for waitor in stored_waitor_list.keys():
                self.stored_waitor[waitor] = stored_waitor_list[waitor]

    def log_in(self, waitor_id, user_name, password):
        # already registered waiter logged in to work
        if self.stored_waitor.get(waitor_id):
            # waitor is registered
            if user_name == self.stored_waitor[waitor_id]["user_name"] \
                    and password == self.stored_waitor[waitor_id]["password"]:
                # waitor entered valid access data
                self.waitor_list.append(Waitor(waitor_id, user_name, password))
            self.waitor_anz += 1

    def register_waitor(self, waitor_id, user_name, user_password):
        # adds a waiter who is not yet registered in the system
        self.stored_waitor[waitor_id] = {"user_name": user_name, "password": user_password}

    def get_waitor_by_id(self, waitor_id):
        # returns the object of a waiter by its ID
        for waitor in self.waitor_list:
            if waitor.id == waitor_id:
                return waitor
        # otherwise the waiter does not exist in the system
        logging.warning(f'Waitor with ID {waitor_id} not found!')

    def get_waitor_list_in_json(self):
        # returns the data of a waiter in json format
        temp = {}
        for waitor in self.waitor_list:
            temp[waitor.id] = waitor.get_waitor_in_json()
        return temp

    def log_out(self, waitor_id):
        # Deletes the waiter from the list of active waiters and returns his pending orders so that they can
        # be redistributed
        waitor = self.get_waitor_by_id(waitor_id)
        self.waitor_list.remove(waitor)
        self.waitor_anz -= 1
        return waitor.active_orders

    def to_string(self):
        return '----WAITOR-LIST----\n' + json.dumps(self.get_waitor_list_in_json(), indent=4, sort_keys=True)


class Waitor:
    def __init__(self, waitor_id, user_name, user_password):
        self.id = waitor_id
        self.is_available = False  # means, if the waitor is working or in the toilet, ...
        self.is_working = False
        self.active_orders = []
        self.user_name = user_name
        self.password = user_password
        self.connection = None

    def absolve_action(self, waitor_id):
        for action in self.active_orders:
            if action["id"] == waitor_id:
                self.active_orders.remove(action)

    def get_action(self):
        pass

    def send_action(self):
        pass

    def get_waitor_in_json(self):
        return {"id": self.id, "is_available": self.is_available, "active_orders": self.active_orders,
                "user_name": self.user_name, "password": self.password}


relPath = str(Path(__file__).parent) + '/'