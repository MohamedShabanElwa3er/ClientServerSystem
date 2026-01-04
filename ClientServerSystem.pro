TEMPLATE = subdirs

# Explicit .pro file mappings
common.file = common/common.pro
server.file = server/server.pro
client.file = client/client.pro
tests.file  = tests/tests.pro

SUBDIRS += common server client tests