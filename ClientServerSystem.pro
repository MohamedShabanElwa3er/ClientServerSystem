TEMPLATE = subdirs

common.file = common/common.pro
server.file = server/server.pro
client.file = client/client.pro
tests.file  = tests/tests.pro

# ✅ enforce correct build order
server.depends = common
client.depends = common
tests.depends  = common

SUBDIRS += common server client tests