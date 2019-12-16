from flaskr import db
import pandas as pd
import pandas.io.json
import datetime


def get_avg_duration_dataframe(username, days_back):
    db_collection = db.Audits().get_collection(username)
    now = datetime.datetime.utcnow()
    last_xd = now - datetime.timedelta(days=days_back)
    pipeline1 = [
        {
            '$project': {

                '_id': 0,
                'duration': "$audit_data.duration",
                'within_time': {'$gte': [{'$dateFromString': {'dateString': '$created_at'}}, last_xd]}

            }
        },
        {
            '$match': {'within_time': True}
        },
        {
            '$group': {
                '_id': None,
                'duration': {
                    '$avg': "$duration"
                }

            }
        },
        {
            '$project': {'_id': 0,
                         'duration': 1}
        }
    ]

    average_duration = (pd.io.json.json_normalize(list(db_collection.aggregate(pipeline1))).get('duration').iloc[0])
    print(average_duration)
    if average_duration is not None:
        average_duration /= 100

    pipeline2 = [
        {
            '$project': {'_id': 0,
                         'date': {'$substr': ["$modified_at", 0, 10]},
                         'duration': '$audit_data.duration',
                         'within_time': {'$gte': [{'$dateFromString': {'dateString': '$created_at'}}, last_xd]}
                         }
        },
        {
            '$match': {'within_time': True}
        },
        {
            '$group': {'_id': '$date',
                       'avg_duration': {'$avg': '$duration'}
                       }
        },
        {
            '$project': {
                '_id': 0,
                'date': '$_id',
                'avg_duration_percent': {'$divide': ['$avg_duration', average_duration]}}
        }

    ]
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline2)))


def get_stats_by_x_days(username, days_back):
    db_collection = db.Audits().get_collection(username)
    now = datetime.datetime.utcnow()
    last_xd = now - datetime.timedelta(days=days_back)
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
                'array_values': {'$gte': [{'$dateFromString': {'dateString': '$created_at'}}, last_xd]}

            }
        },
        {
            '$match': {
                'array_values': True
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


def get_average_score_percentage(username):
    db_collection = db.Audits().get_collection(username)
    now = datetime.datetime.utcnow()
    last_30d = now - datetime.timedelta(days=30)
    pipeline = [
        {
            '$project': {
                'score_percentage': "$audit_data.score_percentage",
                'array_values': {'$gte': [{'$dateFromString': {'dateString': '$created_at'}}, last_30d]}
            }

        },
        {
            '$match': {
                'array_values': True
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
    return pd.io.json.json_normalize(list(db_collection.aggregate(pipeline))).get('avg_score_percentage').iloc[0]


def get_stats_by_day_dataframe(username):
    db_collection = db.Audits().get_collection(username)
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


def get_last_x_days_dataframe(username):
    db_collection = db.Audits().get_collection(username)
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


def get_failed_report_dataframe(username):
    db_collection = db.Audits().get_collection(username)
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


def get_map_dataframe(username):
    db_collection = db.Audits().get_collection(username)
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
            }
        },
        {
            '$match': {
                'location.responses.location.geometry.type': 'Point'
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
    print(get_average_score_percentage('matthew'))
