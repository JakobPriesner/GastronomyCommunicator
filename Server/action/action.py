import logging


class ActionList:
    def __init__(self):
        logging.debug('Init ActionList')
        self.actions = []
        self.completed_actions = []
        self.anz_actions = 0

    def add_action(self, action_description, table):
        temp_action = Action(self.anz_actions+1, action_description, table)
        self.actions.append(temp_action)
        self.anz_actions += 1
        logging.info(f'Add action with ID: {self.anz_actions}, description: {action_description} and table (ID: {table.id}, number: {table.number})')
        return temp_action

    def complete_action(self, action_id):
        temp_action = self.get_action_by_id(action_id)
        self.actions.remove(temp_action)
        self.completed_actions.append(temp_action)

    def get_action_by_id(self, action_id):
        for action in self.actions:
            if action.id == action_id:
                return action
        return False


class Action:
    def __init__(self, action_id, action_description, table):
        self.id = action_id
        self.action = action_description
        self.table = table
        self.priority = 0
        self.is_done = False
        self.number_of_requests = 1

    def get_action_in_json(self):
        return {"id": self.id, "action": self.action, "table": self.table, "is_done": self.is_done,
                "number_of_requests": self.number_of_requests}

    def to_string(self):
        return f'{self.id}: Action: {self.action} on Tablenumber {self.table.number} with priority {self.priority}. Requested {self.number_of_requests} Time(s). [{self.is_done}]'