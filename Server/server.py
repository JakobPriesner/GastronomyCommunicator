from pathlib import Path
from waitor.waitor import WaitorList
from table.table import TableList


class Core:
    def __init__(self, table_list, waitor_list):
        self.table_list = table_list
        self.waitor_list = waitor_list
        self.actions = []

    def assign_action(self):
        occupancy_list = []
        for waitor in self.waitor_list.get_waitor_list:
            occupancy_list.append([waitor.id, len(waitor.active_orders)])
        # sort the waiters according to their workload
        sorted(occupancy_list, key=lambda x: x[1])

        # give the action to the waiter who is least busy
        self.waitor_list.get_waitor_by_id(occupancy_list[0]).active_orders.append()

    def get_action(self):
        pass

    def add_table(self):
        pass


def test(core):
    core.table_list.register_table(1, 4)
    core.table_list.register_table(2, 7)
    core.table_list.register_table(3, 1)
    core.table_list.register_table(4, 8)
    print(core.table_list.to_string())

    core.waitor_list.register_waitor(0, "Jakob", "123456")
    core.waitor_list.register_waitor(1, "Dave", "789")
    core.waitor_list.log_in(0, "Jakob", "123456")
    # core.waitor_list.log_in(1, "Dave", "789")
    print(core.waitor_list.to_string())


if __name__ == "__main__":
    relPath = str(Path(__file__).parent) + "/"
    core = Core(TableList(), WaitorList())
    test(core)
