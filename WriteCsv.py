import csv
from audits.Audits import Audit


def write_to_csv(audits):
    csv_data = []

    #first line of the csv is titles
    csv_data.append(["audit_id", "template_id", "archived", "audit_created_at", "audit_modified_at", "score", "total_score",
                 "score_percentage", "audit_name", "duration", "date_completed", "owner_name", "owner_id", "longitude",
                 "latitude"])

    for i, audit in enumerate(audits):
        csv_data.append([audits[i].get_audit_id(), audits[i].get_template_id(), audits[i].get_archived(),
                        audits[i].get_audit_created_at(), audits[i].get_audit_modified_at(), audits[i].get_score(),
                        audits[i].get_total_score(), audits[i].get_score_percentage(), audits[i].get_audit_name(),
                        audits[i].get_duration(), audits[i].get_date_completed(), audits[i].get_owner_name(),
                        audits[i].get_owner_id(), audits[i].get_longitude(), audits[i].get_latitude()])

    with open('data.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_data)
    csvFile.close()
