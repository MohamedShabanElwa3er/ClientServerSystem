QT += core testlib
CONFIG += console c++17

INCLUDEPATH += ../../../common ../../../server
include(../../../common/common.pri)

LIBS += -L../../../common -lcommon

SOURCES += \
    test_append.cpp \
    ../../../server/commands/AppendCommand.cpp
