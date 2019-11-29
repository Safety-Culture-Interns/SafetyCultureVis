class Audit:
    def __init__(self, audit_id, template_id, audit_created_at, audit_modified_at, score, total_score,
                 score_percentage, audit_name, duration, date_completed, owner_name,
                 owner_id, latitude, longitude, template_owner, template_author, template_description, template_name,
                 template_owner_id, template_author_id):
        self.audit_id = audit_id
        self.template_id = template_id
        self.audit_created_at = audit_created_at
        self.audit_modified_at = audit_modified_at
        self.score = score
        self.total_score = total_score
        self.score_percentage = score_percentage
        self.audit_name = audit_name
        self.duration = duration
        self.date_completed = date_completed
        self.owner_name = owner_name
        self.owner_id = owner_id
        self.template_owner = template_owner
        self.template_author = template_author
        self.template_description = template_description
        self.template_name = template_name
        self.latitude = latitude
        self.longitude = longitude
        self.template_owner_id = template_owner_id
        self.template_author_id = template_author_id

    # def get_attribute(self, attribute):
    #     return self.__getattribute__(attribute)

    def get_audit_id(self):
        return self.audit_id

    def get_template_id(self):
        return self.template_id

    def get_audit_created_at(self):
        return self.audit_created_at

    def get_audit_modified_at(self):
        return self.audit_modified_at

    def get_score(self):
        return self.score

    def get_total_score(self):
        return self.total_score

    def get_score_percentage(self):
        return self.score_percentage

    def get_audit_name(self):
        return self.audit_name

    def get_duration(self):
        return self.duration

    def get_date_completed(self):
        return self.date_completed

    def get_owner_name(self):
        return self.owner_name

    def get_owner_id(self):
        return self.owner_id

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_template_owner(self):
        return self.template_owner

    def get_template_author(self):
        return self.template_author

    def get_template_description(self):
        return self.template_description

    def get_template_name(self):
        return self.template_name

    def get_template_owner_id(self):
        return self.template_owner_id

    def get_template_author_id(self):
        return self.template_author_id

    def __str__(self):
        return "String for audit ID {}. that is using the template {}. Created by {}".format(self.audit_id, self.template_id, self.audit_name)
