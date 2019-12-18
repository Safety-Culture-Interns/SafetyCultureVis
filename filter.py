from collections import OrderedDict

api_zipped = [('text-1', 'xxx'), ('img-1', '122'), ('img-2', 'jjj'), ('text-3', 'xxx'), ('text-4', 'xxx'),
              ('extra-4', 'xxx')]  # list from api
mongo_zipped = [('text-1', 'x'), ('img-1', '122'), ('img-2', 'x'), ('text-3', 'xxx'),
                ('text-4', 'xxx')]  # list from mongo



def filterDuplicate(string_to_check):
    if string_to_check in ll:
        print("wow")
        return False
    else:
        return True


def audits_to_delete(audit_ids):
    return list(set([x for x in audit_ids if audit_ids.count(x) > 1]))


ll = api_zipped
out_filter = list(filter(filterDuplicate, mongo_zipped))
ll = mongo_zipped
out_filter += list(filter(filterDuplicate, api_zipped))  # returns a list of everything that is different
try:
    audit_ids, audit_dates = zip(*out_filter)  # gets just the different audit ids
    audits_to_add = list(OrderedDict.fromkeys(audit_ids))  # this is the list to be added to database
    audits_to_delete = audits_to_delete(audit_ids)
    print("delete {}".format(audits_to_delete))  # delete
    print("add {}".format(audits_to_add))  # add
except ValueError:
    print("database and Api are the same")

# audit_ids = ['dddd', 'ddss', 'ddddd', 'sdsads' 'sdasd' 'dweee333333']
# mongo_ids = ['dddd', 'ddss', 'ddss', 'ddddsd', 'sdsads', 'asdas', '3333']
#
# audit_ids_to_delete = list(filter(lambda x: x not in audit_ids, mongo_ids))
# print(audit_ids_to_delete)
