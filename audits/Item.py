class Item:
    def __init__(self, item_id, label, item_type, scoring=[], children=[], parent_id="", options=[], responses=[]):
        self.item_id = item_id
        self.label = label
        self.item_type = item_type
        self.scoring = scoring
        self.children = children
        self.parent_id = parent_id
        self.options = options
        self.responses = responses

    def get_item_id(self):
        return self.item_id

    def get_label(self):
        return self.label

    def get_item_type(self):
        return self.item_type

    def get_scoring(self):
        return self.scoring

    def get_children(self):
        return self.children

    def get_parent_id(self):
        return self.parent_id

    def get_options(self):
        return self.options

    def get_responses(self):
        return self.responses

    def set_item_id(self, item_id):
        self.item_id = item_id

    def set_label(self, label):
        self.label = label

    def set_item_type(self, item_type):
        self.item_type = item_type

    def set_scoring(self, scoring):
        self.scoring = scoring

    def set_children(self, children):
        self.children = children

    def set_parent_id(self, parent_id):
        self.parent_id = parent_id

    def set_options(self, options):
        self.options = options

    def set_responses(self, responses):
        self.responses = responses
