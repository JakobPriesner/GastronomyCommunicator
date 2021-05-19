import logging
import sys
import time
from pathlib import Path
from waitor.waitor import WaitorList
from table.table import TableList
from action.action import ActionList


class Core:
    def __init__(self, table_list, waitor_list, action_list):
        self.table_list = table_list
        self.waitor_list = waitor_list
        self.action_list = action_list

    def assign_action(self, action_description, table_id):
        # toDo: check if the table has already sent this task and if necessary only increase the counter of the task
        occupancy_list = []
        for waitor in self.waitor_list.waitor_list:
            occupancy_list.append([waitor.id, len(waitor.active_orders)])
        # sort the waiters according to their workload
        occupancy_list = sorted(occupancy_list, key=lambda x: x[1], reverse=False)
        table = self.table_list.get_table_by_id(table_id)

        if table:
            # create Action
            action = self.action_list.add_action(action_description, table)

            # give the action to the waiter who is least busy
            self.waitor_list.get_waitor_by_id(occupancy_list[0][0]).active_orders.append(action)
        else:
            logging.critical('Action was posted from a table with an ID which is not created or not registered!')

    def get_action(self):
        pass

    def add_table(self):
        pass

    def close(self, first_complete_tasks=True):
        # save all lists in .json-Files
        logging.info('Store Waitor List...')
        self.waitor_list.store_waitor_list()
        logging.info('Store Table List...')
        self.table_list.store_table_list()

        if first_complete_tasks:
            logging.info('Waiting for completion of all tasks...')
            while not self.action_list.actions == []:
                time.sleep(1)

        logging.info('Stopping server...')


def test(core):
    core.table_list.register_table(1, 4)
    core.table_list.register_table(2, 7)
    core.table_list.register_table(3, 1)
    core.table_list.register_table(4, 8)
    print(core.table_list.to_string())

    core.waitor_list.register_waitor(0, "Jakob", "123456")
    core.waitor_list.register_waitor(1, "Dave", "789")
    core.waitor_list.log_in(0, "Jakob", "123456")
    core.waitor_list.log_in(1, "Dave", "789")

    core.assign_action("bestellen", 1)
    core.assign_action("bestellen", 1)
    core.assign_action("bezahlen", 1)
    core.assign_action("frage", 1)
    core.assign_action("bestellen", 2)
    core.assign_action("bestellen", 3)
    core.assign_action("bestellen", 4)
    core.assign_action("bestellen", 1)
    core.assign_action("frage", 5)

    for waitor in core.waitor_list.waitor_list:
        print(waitor.to_string())

    core.close()


def prepare_log():
    # init logger
    logging.basicConfig(filename='server.log', level=logging.DEBUG)
    root = logging.getLogger()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    LOG_FORMAT = '%(asctime)s,%(msecs)d --> %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    root.addHandler(ch)


if __name__ == "__main__":
    relPath = str(Path(__file__).parent) + "/"
    prepare_log()
    core = Core(TableList(), WaitorList(), ActionList())
    test(core)
