from vars import HOST, PORT, USER, PASSWORD, DATABASE

class BaseApp():
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __doc__(self):
        return f"""
        # {self.name} ({self.id}) 
        {self.description}
        """
    def get_conexion_url(self):
        return f"schema://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
