from recflows.services.database import read_resource_by_id, insert_resouce, update_resouce


class BaseResource:
    def __init__(self, table, id):
        self.table = table
        self.id = id

    def mount_resource(self):
        record = {
            k: v
            for k, v in self.__dict__.items()
            if k != "table"
        }

        if read_resource_by_id(self.table, self.id):
            update_resouce(self.table, record)
        else:
            insert_resouce(self.table, record)
