import requests
from audits import Template, Audits

# URL = "https://api.safetyculture.io"
URL = "https://sandpit-api.safetyculture.io"
# HEADER = {'Authorization': 'Bearer 9defde6335dd17c61959ae46a7d73a307c0945fbcd435dc649d1d341235e5105'}
HEADER = {'Authorization': 'Bearer c9b02a45268c522719c457f46bec3a1f6142f1513191fee0204d5603689b80da'}


def main():
    templates = create_templates()
    audit_ids = create_audit_ids()
    audits = create_audits(audit_ids)


def get_json(value):
    if value == "audits" or value == "templates":
        r = requests.get(url="{}/{}/search".format(URL, value), headers=HEADER)
    else:
        r = requests.get(url="{}/{}/{}".format(URL, "audits", value), headers=HEADER)
    data = r.json()
    return data


def create_templates():
    data = get_json('templates')
    templates = []
    for number, list in enumerate(data['templates']):
        template_id = list['template_id']
        try:
            template_name = list['name']
        except KeyError:
            template_name = "No Name"
        template_created_at = list['created_at']
        template_modified_on = list['modified_at']
        template = Template.Template(template_name, template_id, template_created_at, template_modified_on)
        templates.append(template)
    return templates


def create_audit_ids():
    data = get_json('audits')
    audits = []
    for number, list in enumerate(data['audits']):
        audit_id = data['audits'][number]['audit_id']
        audits.append(audit_id)
    return audits


def create_audits(audit_ids):
    audits = []
    # for audit in audit_ids:
    for i in range(0, 5):
        data = get_json(audit_ids[i])
        template_id = data['template_id']
        archived = data['archived']
        created_on = data['audit_data']['date_started']
        modified_on = data['audit_data']['date_modified']
        owner = data['audit_data']['authorship']['owner']
        aud = Audits.Audit(template_id, archived, created_on, modified_on, owner)
        audits.append(aud)
    return audits


main()
