import csv
from audits.Audits import Audit
from audits.Item import Item
from audits.Template import Template

templates = []
audits = []
items = []
templateData = []
auditData = []
itemData = []

template1 = Template("name", "id", "created", "modified")
audit1 = Audit("Audit_id", "Template_id", "archived", "audit created", "audit_modified at", "score", "total_score",
               "score_percentage", "audit_name", "duration", "date_compleated", "owner_name", "owner_id")
item1 = Item("item_id", "label", "item_type")
item2 = Item("item_id2", "label2", "item_type2")
templates.append(template1)
audits.append(audit1)
items.append(item1)
items.append(item2)
total_templates = 0
total_audits = 0
total_items = 0
for i, template in enumerate(templates):
    total_templates += 1
    templateData.append([templates[i].get_name(), templates[i].get_id(), templates[i].get_created(),
                         templates[i].get_modified()])

for i, audit in enumerate(audits):
    total_audits += 1
    auditData.append([audits[i].get_audit_id(), audits[i].get_template_id(), audits[i].get_archived(),
                      audits[i].get_audit_created_at(), audits[i].get_audit_modified_at(), audits[i].get_score(),
                      audits[i].get_total_score(), audits[i].get_score_percentage(), audits[i].get_audit_name(),
                      audits[i].get_duration(), audits[i].get_date_completed(), audits[i].get_owner_name(),
                      audits[i].get_owner_id()])

for i, item in enumerate(items):
    total_items += 1
    itemData.append([items[i].get_item_id(), items[i].get_label(), items[i].get_item_type()])
csvData = []
for i in range(total_templates):
    csvData.append(templateData[i])
for i in range(total_audits):
    csvData.append(auditData[i])
for i in range(total_items):
    csvData.append(itemData[i])
with open('data.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()
