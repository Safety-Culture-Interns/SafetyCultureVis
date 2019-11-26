class Audit:
    def __init__(self, audit_id, template_id, archived, audit_created_at, audit_modified_at, score, total_score,
                 score_percentage, audit_name, duration, date_completed, date_modified, date_started, owner_name,
                 owner_id):
        self.audit_id = audit_id
        self.template_id = template_id
        self.archived = archived
        self.audit_created_at = audit_created_at
        self.audit_modified_at = audit_modified_at
        self.score = score
        self.total_score = total_score
        self.score_percentage = score_percentage
        self.audit_name = audit_name
        self.duration = duration
        self.date_completed = date_completed
        self.date_modified = date_modified
        self.date_started = date_started
        self.owner_name = owner_name
        self.owner_id = owner_id

    # def get_attribute(self, attribute):
    #     return self.__getattribute__(attribute)

    def get_audit_id(self):
        return self.audit_id

    def get_template_id(self):
        return self.template_id

    def get_archived(self):
        return self.archived

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

    def get_date_modified(self):
        return self.date_modified

    def get_date_started(self):
        return self.date_started

    def get_owner_name(self):
        return self.owner_name

    def get_owner_id(self):
        return self.owner_id

    def get_owner(self):
        return self.owner
