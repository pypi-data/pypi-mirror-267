from recflows.resources.base import BaseResource

class BaseApp(BaseResource):
    def __init__(self, id, name, description):
        super().__init__("apps", id)
        self.name = name
        self.description = description

        self.mount_resource()

    def __doc__(self):
        return f"""
        # {self.name} (id={self.id}) 
        {self.description}
        """
