class Audit:
    template_id = ''
    archived = ''
    created_on = ''
    modified_on = ''
    owner = ''

    def __init__(self, id, archived, created, modififed, owner):
        self.template_id = id
        self.archived = archived
        self.created_on = created
        self.modified_on = modififed
        self.owner = owner

    def get_owner(self):
        return self.owner
