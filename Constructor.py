from audits import Audits
import WriteCsv
import MongoDB
import APISync
import csv

URL = "https://api.safetyculture.io"  # live site
# URL = "https://sandpit-api.safetyculture.io"  # sand box
HEADER = {'Authorization': 'Bearer 9defde6335dd17c61959ae46a7d73a307c0945fbcd435dc649d1d341235e5105'}  # live site


# HEADER = {'Authorization': 'Bearer c9b02a45268c522719c457f46bec3a1f6142f1513191fee0204d5603689b80da'}  # sandbox


def main():
    # write_audits_to_db(audit_ids)
    audit_ids = MongoDB.get_all('audit_id')
    APISync.sync_with_api()
    if MongoDB.get_database_length() > get_csv_length():
        audits = create_audits(audit_ids)
        WriteCsv.write_to_csv(audits)


def create_audits(audit_ids):
    audits = []
    for i in range(0, len(audit_ids)):
        print("{} audit added to class list".format(i))
        data = MongoDB.get_all_from_db(audit_ids[i])
        audit_id = data['audit_id']
        template_id = MongoDB.get_audit_information(audit_id, 'template_id')
        template_data = MongoDB.get_audit_information(audit_id, 'template_data')
        audit_data = MongoDB.get_audit_information(audit_id, 'audit_data')
        template_owner = remove_special_characters(template_data['authorship']['owner'])
        template_author = remove_special_characters(template_data['authorship']['author'])
        template_description = remove_special_characters(template_data['metadata']['description'])
        template_name = remove_special_characters(template_data['metadata']['name'])
        template_author_id = template_data['authorship']['author_id']
        template_owner_id = template_data['authorship']['owner_id']
        created_on = audit_data['date_started']
        modified_on = audit_data['date_modified']
        score = audit_data['score']
        total_score = audit_data['total_score']
        score_percentage = audit_data['score_percentage']
        audit_name = remove_special_characters(audit_data['name'])
        duration = audit_data['duration']
        date_completed = audit_data['date_completed']
        owner_name = remove_special_characters(audit_data['authorship']['owner'])
        owner_id = audit_data['authorship']['owner_id']
        try:
            coordinates = MongoDB.get_audit_information(audit_id, ['header_items', 'responses', 'location', 'geometry',
                                                                   'coordinates'])
            latitude = coordinates[0]
            longitude = coordinates[1]
        except IndexError:
            latitude = ''
            longitude = ''
        aud = Audits.Audit(audit_id, template_id, created_on, modified_on, score, total_score,
                           score_percentage,
                           audit_name, duration, date_completed, owner_name, owner_id, latitude, longitude,
                           template_owner, template_author, template_description, template_name, template_owner_id,
                           template_author_id)
        audits.append(aud)
    return audits


def remove_special_characters(text):
    return ''.join(e for e in text if e.isascii())


# returns the number of lines in the csv.
# used to determine if csv needs to be updates
def get_csv_length():
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader)
        return row_count


main()
