from flaskr import db
import pandas as pd
import pandas.io.json
import datetime


def get_stats_by_x_days(username, start_date, end_date):
    """ Returns a dataframe with the date, total audits, total uncompleted audits, total completed audits,
    average score, average total score, average score percentage, average duration and percent of audits completed
    in a given date range
    """
    db_collection = db.Audits().get_collection(username)
    start_datetime = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    end_datetime = datetime.datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
    pipeline = [
        {
            '$project': {
                '_id': 0,
                'created_at': 1,
                'score': '$audit_data.score',
                'total_score': '$audit_data.total_score',
                'score_percentage': '$audit_data.score_percentage',
                'duration': '$audit_data.duration',
                'failed': {'$cond': [{'$eq': ['$audit_data.date_completed', None]}, 1, 0]},
                'completed': {'$cond': [{'$eq': ['$audit_data.date_completed', None]}, 0, 1]},
                'date': {'$substr': ["$modified_at", 0, 10]},
                'within_start_date': {'$gte': [{'$dateFromString': {'dateString': '$modified_at'}}, start_datetime]},
                'within_end_date': {'$lte': [{'$dateFromString': {'dateString': '$modified_at'}}, end_datetime]}

            }
        },
        {
            '$match': {
                'within_start_date': True,
                'within_end_date': True
            }
        },
        {
            '$group': {
                '_id': '$date',
                'audits': {'$sum': 1},
                'failed_audits': {'$sum': '$failed'},
                'completed_audits': {'$sum': '$completed'},
                'avg_score': {'$avg': '$score'},
                'avg_total_score': {'$avg': '$total_score'},
                'avg_score_percentage': {'$avg': '$score_percentage'},
                'avg_duration': {'$avg': '$duration'},
            }
        },
        {
            '$project': {
                '_id': 0,
                'date': '$_id',
                'audits': 1,
                'failed_audits': 1,
                'completed_audits': 1,
                'avg_score': 1,
                'avg_total_score': 1,
                'avg_score_percentage': 1,
                'avg_duration': 1,
                'percent_completed': {'$multiply': [{'$divide': ['$completed_audits', '$audits']}, 100]}

            }
        },
        {
            '$sort': {
                'date': 1
            }
        }

    ]

    # use the pipeline to make a list from the aggregate cursor, then convert to a dataframe
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))


def get_average_score_percentage(username, start_date, end_date):
    """ Returns a number of the average score percentage of the audits in a date range
    """
    db_collection = db.Audits().get_collection(username)
    start_datetime = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    end_datetime = datetime.datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
    pipeline = [
        {
            '$project': {
                'score_percentage': "$audit_data.score_percentage",
                'within_start_date': {'$gte': [{'$dateFromString': {'dateString': '$modified_at'}}, start_datetime]},
                'within_end_date': {'$lte': [{'$dateFromString': {'dateString': '$modified_at'}}, end_datetime]}
            }

        },
        {
            '$match': {
                'within_start_date': True,
                'within_end_date': True
            }
        },
        {
            "$group": {
                '_id': None,
                'avg_score_percentage': {
                    '$avg': "$score_percentage"
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'avg_score_percentage': 1
            }

        }
    ]
    if pd.io.json.json_normalize(list(db_collection.aggregate(pipeline))).get('avg_score_percentage') is None:
        return 0

    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline))).get('avg_score_percentage').iloc[0]


# Returns
def get_failed_report_dataframe(username, start_date, end_date):
    """ Returns a dataframe with the count of the uncompleted audits within a date range
    """
    db_collection = db.Audits().get_collection(username)
    start_datetime = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    end_datetime = datetime.datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
    pipeline = [
        {
            '$project': {'_id': 0,
                         'array_values': {
                             '$cond': [{'$eq': ['$audit_data.date_completed', None]}, 'failed', 'completed']},
                         'within_start_date': {
                             '$gte': [{'$dateFromString': {'dateString': '$modified_at'}}, start_datetime]},
                         'within_end_date': {
                             '$lte': [{'$dateFromString': {'dateString': '$modified_at'}}, end_datetime]}
                         }
        },
        {
            '$match': {
                'within_start_date': True,
                'within_end_date': True
            }
        },
        {
            '$group': {
                '_id': '$array_values',
                'count': {'$sum': 1}
            }

        }
    ]

    df = pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))
    if df.empty:
        data = {'_id': ['failed', 'completed'], 'count': [0, 0]}
        df = pd.DataFrame(data)
    if not (df['_id'] == 'failed').any():
        new_row = pd.DataFrame({'_id': 'failed', 'count': 0}, index=[0])
        df = pd.concat([new_row, df]).reset_index(drop=True)
    if not (df['_id'] == 'completed').any():
        df = df.append({'_id': 'completed', 'count': 0}, ignore_index=True)

    return df


def get_map_dataframe(username, start_date, end_date):
    """ Returns a dataframe with the dates created at, modified at, completed at, score percentage, x and y coordinates
    that have a point location and is within the given date range
    """

    db_collection = db.Audits().get_collection(username)
    start_datetime = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    end_datetime = datetime.datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
    pipeline = [
        {
            '$project': {
                '_id': 0,
                'Created_at': "$created_at",
                'Modified_at': "$modified_at",
                'completed_at': '$audit_data.date_completed',
                'Score_percent': '$audit_data.score_percentage',
                'location': {'$arrayElemAt': [
                    {'$filter': {'input': "$header_items", 'as': "item",
                                 'cond': {'$eq': ["$$item.label", "Location"]}}},
                    0]},
                'within_start_date': {'$gte': [{'$dateFromString': {'dateString': '$modified_at'}}, start_datetime]},
                'within_end_date': {'$lte': [{'$dateFromString': {'dateString': '$modified_at'}}, end_datetime]}
            }
        },
        {
            '$match': {
                'location.responses.location.geometry.type': 'Point',
                'within_start_date': True,
                'within_end_date': True
            }
        },
        {
            '$project': {'Created_at': "$Created_at", 'Modified_at': "$Modified_at",
                         'completed_at': '$completed_at', 'Score': '$Score_percent',
                         'X': {'$arrayElemAt': ['$location.responses.location.geometry.coordinates', 0]},
                         'Y': {'$arrayElemAt': ['$location.responses.location.geometry.coordinates', 1]}}
        }
    ]

    # use the pipeline to make a list from the aggregate cursor, then convert to a dataframe
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))

    # test print result
#
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(get_map_dataframe('matthew', '2018-08-08', '2018-08-08'))

