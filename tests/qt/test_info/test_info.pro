QT += core testlib
CONFIG += console c++17

INCLUDEPATH += ../../../common ../../../server
include(../../../common/common.pri)

LIBS += -L../../../common -lcommon

SOURCES += \
    test_info.cpp \
    ../../../server/commands/InfoCommand.cpp
