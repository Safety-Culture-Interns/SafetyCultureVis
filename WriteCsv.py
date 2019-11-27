import csv
from audits.Audits import Audit

audits = []
csvData = []

audit1 = Audit("Audit_id", "Template_id", "archived", "audit created", "audit_modified at", "score", "total_score",
               "score_percentage", "audit_name", "duration", "date_compleated", "owner_name", "owner_id")
audit2 = Audit("Audit_id", "Template_id", "archived", "audit created", "audit_modified at", "score", "total_score",
               "score_percentage", "audit_name", "duration", "date_compleated", "owner_name", "owner_id")
audits.append(audit1)
audits.append(audit2)


for i, audit in enumerate(audits):
    csvData.append([audits[i].get_audit_id(), audits[i].get_template_id(), audits[i].get_archived(),
                    audits[i].get_audit_created_at(), audits[i].get_audit_modified_at(), audits[i].get_score(),
                    audits[i].get_total_score(), audits[i].get_score_percentage(), audits[i].get_audit_name(),
                    audits[i].get_duration(), audits[i].get_date_completed(), audits[i].get_owner_name(),
                    audits[i].get_owner_id()])


with open('data.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()
