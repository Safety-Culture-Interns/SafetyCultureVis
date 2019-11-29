import csv
import random
import datetime
from audits.Audits import Audit

LONG_MONTHS = [1, 3, 5, 7, 8, 10, 12]


def write_to_csv(audits):
    csv_data = [["audit_id", "template_id", "audit_created_at_date", "audit_created_at_time",
                 "audit_modified_at_date", "audit_modified_at_time", "score", "total_score", "score_percentage",
                 "audit_name", "duration", "date_completed_date", "date_completed_time", "owner_name", "owner_id",
                 "longitude", "latitude", "template_owner", "template_author", "template_description", "template_name",
                 "template_owner_id", "template_author_id"]]

    # first line of the csv is titles

    for i, audit in enumerate(audits):
        audit_created_at = generate_date("2000-01-01T00:00:00.000Z")
        audit_modified_at = generate_date(audit_created_at)
        date_completed = generate_completed_datetime(audit_modified_at, audits[i].get_duration())

        csv_data.append([audits[i].get_audit_id(), audits[i].get_template_id(),
                         audit_created_at[:10], audit_created_at[11:-5], audit_modified_at[:10],
                         audit_modified_at[11:-5],
                         audits[i].get_score(), audits[i].get_total_score(), audits[i].get_score_percentage(),
                         audits[i].get_audit_name(), audits[i].get_duration(), date_completed[:10],
                         date_completed[11:-5],
                         audits[i].get_owner_name(), audits[i].get_owner_id(), audits[i].get_longitude(),
                         audits[i].get_latitude(), audits[i].get_template_owner(), audits[i].get_template_author(),
                         audits[i].get_template_description(), audits[i].get_template_name(),
                         audits[i].get_template_owner_id(), audits[i].get_template_author_id()])

    with open('data.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_data)
    csvFile.close()


def generate_date(earlier_string):
    correct_datetime = False
    early_values = [int(earlier_string[:4]), int(earlier_string[5:7]), int(earlier_string[8:10]),
                    int(earlier_string[11:13]), int(earlier_string[14:16]), int(earlier_string[17:19])]
    early_datetime = datetime.datetime(early_values[0], early_values[1], early_values[2], early_values[3],
                                       early_values[4], early_values[5])

    while not correct_datetime:
        seconds = random.randrange(0, 59)
        minuets = random.randrange(0, 59)
        hour = random.randrange(0, 24)
        year = random.randrange(2010, 2019)
        month = random.randrange(1, 12)
        if month in LONG_MONTHS:
            max_days = 31
        elif month == 2:
            max_days = 28
        else:
            max_days = 30
        day = random.randrange(1, max_days)
        current_datetime = datetime.datetime(year, month, day, hour, minuets, seconds)
        if current_datetime > early_datetime:
            correct_datetime = True
            date_time = "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z".format(year, month, day, hour, minuets, seconds)
    return date_time


def generate_completed_datetime(date_string, duration):
    early_values = [int(date_string[:4]), int(date_string[5:7]), int(date_string[8:10]),
                    int(date_string[11:13]), int(date_string[14:16]), int(date_string[17:19])]
    early_datetime = datetime.datetime(early_values[0], early_values[1], early_values[2], early_values[3],
                                       early_values[4], early_values[5])
    completed_datetime = early_datetime + datetime.timedelta(seconds=duration)
    date_time = "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z".format(completed_datetime.year, completed_datetime.month,
                                                                    completed_datetime.day, completed_datetime.hour,
                                                                    completed_datetime.minute,
                                                                    completed_datetime.second)

    return date_time
