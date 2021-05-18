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