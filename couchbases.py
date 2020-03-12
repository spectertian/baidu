from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.exceptions import NotFoundError

# import couchbase.bucket
cluster = Cluster('couchbase://127.0.0.1')
# cluster = Cluster('couchbase://127.0.0.1,192.168.1.1')
authenticator = PasswordAuthenticator('admin', 'admin123')
# exit()
cluster.authenticate(authenticator)
cb = cluster.open_bucket('beer-sample')


def getKey(key):
    try:
        result = cb.get(key)
        return result.value
    except NotFoundError as e:
        # print(e)
        return ''
    # ss = cb.get(key).value
    # if ss.success:
    #     return  ss
    # else:
    #     return ''


def setInfo(key, value):
    return cb.upsert(key, value)

# cb.upsert('u:king_arthur', {'name': 'Arthur', 'email': 'kingarthur@couchbase.com', 'interests': ['Holy Grail', 'African Swallows']})
# OperationResult<RC=0x0, Key=u'u:king_arthur', CAS=0xb1da029b0000>

# ss = cb.get('u:king_arthur').value
# ss = cb.get('abbaye_notre_dame_du_st_remy-rochefort_8').value

# print(ss)
# {u'interests': [u'Holy Grail', u'African Swallows'], u'name': u'Arthur', u'email': u'kingarthur@couchbase.com'}

## The CREATE PRIMARY INDEX step is only needed the first time you run this script
# cb.n1ql_query('CREATE PRIMARY INDEX ON beer-sample').execute()
# from couchbase.n1ql import N1QLQuery
# #
# row_iter = cb.n1ql_query(N1QLQuery('SELECT name FROM beer-sample WHERE ' +\
# '$1 IN interests', 'African Swallows'))
# for row in row_iter: print(row)
# {u'name': u'Arthur'}
