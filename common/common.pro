TEMPLATE = lib
CONFIG += staticlib
QT += core

include(common.pri)

SOURCES += \
    protocol/CommandParser.cpp \
    protocol/Response.cpp \
    security/PathValidator.cpp