from flaskr import db
import pandas as pd
import pandas.io.json
import datetime

db_collection = db.Audits().db_collection


def get_stats_by_day():
    pipeline = [
        {
            '$project': {
                '_id': 0,
                'score': '$audit_data.score',
                'total_score': '$audit_data.total_score',
                'score_percentage': '$audit_data.score_percentage',
                'duration': '$audit_data.duration',
                'date': {'$substr': ["$modified_at", 0, 10]},
                'failed': {'$cond': [{'$eq': ['$audit_data.date_completed', None]}, 1, 0]},
                'completed': {'$cond': [{'$eq': ['$audit_data.date_completed', None]}, 0, 1]}
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
        }
    ]
    # use the pipeline to make a list from the aggregate cursor, then convert to a dataframe
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))


def get_last_30_days_dataframe():
    now = datetime.datetime.utcnow()
    last_30d = now - datetime.timedelta(days=30)
    print(last_30d)
    pipeline = [
        {
            '$project': {'_id': 0, 'created_at': 1, 'array_values': {
                '$gte': [{'$dateFromString': {'dateString': '$created_at'}}, last_30d]}
                         }
        },
        {
            '$match': {'array_values': True}
        }

    ]

    # use the pipeline to make a list from the aggregate cursor, then convert to a dataframe
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))


def get_failed_report_dataframe():
    pipeline = [
        {
            '$project': {'_id': 0,
                         'array_values': {
                             '$cond': [{'$eq': ['$audit_data.date_completed', None]}, 'failed', 'completed']}
                         }
        },

        {
            '$group': {
                '_id': '$array_values',
                'count': {'$sum': 1}
            }

        }
    ]

    # use the pipeline to make a list from the aggregate cursor, then convert to a dataframe
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))


def get_map_dataframe():
    pipeline = [
        {
            '$project': {'_id': 0, 'Created_at': "$created_at", 'Modified_at': "$modified_at",
                         'completed_at': '$audit_data.date_completed', 'Score_percent': '$audit_data.score_percentage',
                         'header_items': {'$arrayElemAt': ['$header_items', 3]}}
        },
        {
            '$project': {'Created_at': "$Created_at", 'Modified_at': "$Modified_at",
                         'completed_at': '$completed_at', 'Score': '$Score_percent',
                         'X': {'$arrayElemAt': ['$header_items.responses.location.geometry.coordinates', 0]},
                         'Y': {'$arrayElemAt': ['$header_items.responses.location.geometry.coordinates', 1]}}
        }
    ]

    # use the pipeline to make a list from the aggregate cursor, then convert to a dataframe
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline)))


# test print results
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(get_stats_by_day())
