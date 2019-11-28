import csv
from audits.Audits import Audit


def write_to_csv(audits):
    csv_data = [["audit_id", "template_id", "archived", "audit_created_at_date", "audit_created_at_time",
                 "audit_modified_at_date", "audit_modified_at_time", "score", "total_score", "score_percentage",
                 "audit_name", "duration", "date_completed_date", "date_completed_time", "owner_name", "owner_id",
                 "longitude", "latitude", "template_owner", "template_author", "template_description", "template_name",
                 "template_owner_id", "template_author_id", "prepared_by", "location_country"]]

    # first line of the csv is titles

    for i, audit in enumerate(audits):
        audit_created_at = str(audits[i].get_audit_created_at())
        audit_modified_at = str(audits[i].get_audit_modified_at())
        date_completed = str(audits[i].get_date_completed())

        csv_data.append([audits[i].get_audit_id(), audits[i].get_template_id(), audits[i].get_archived(),
                         audit_created_at[:10], audit_created_at[11:-5], audit_modified_at[:10], audit_modified_at[11:-5],
                         audits[i].get_score(), audits[i].get_total_score(), audits[i].get_score_percentage(),
                         audits[i].get_audit_name(), audits[i].get_duration(), date_completed[:10], date_completed[11:-5],
                         audits[i].get_owner_name(), audits[i].get_owner_id(), audits[i].get_longitude(),
                         audits[i].get_latitude(), audits[i].get_template_owner(), audits[i].get_template_author(),
                         audits[i].get_template_description(), audits[i].get_template_name(),
                         audits[i].get_template_owner_id(), audits[i].get_template_author_id(),
                         audits[i].get_prepared_by(), audits[i].get_location_country()])

    with open('data.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_data)
    csvFile.close()
