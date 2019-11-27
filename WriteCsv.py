import csv
from audits.Audits import Audit


def write_to_csv(audits):
    csv_data = []

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
