QT += core testlib
CONFIG += console c++17

INCLUDEPATH += ../../../common
include(../../../common/common.pri)

LIBS += -L../../../common -lcommon

SOURCES += test_parser.cpp
