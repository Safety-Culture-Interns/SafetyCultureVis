class Template:
    name = ''
    id = ''
    created = ''
    modified = ''

    def __init__(self, name, id, created, modified):
        self.name = name
        self.id = id
        self.created = created
        self.modified = modified

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_modified(self):
        return self.modified

    def get_created(self):
        return self.created
