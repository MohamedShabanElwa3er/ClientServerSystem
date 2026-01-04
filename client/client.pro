QT += core network
CONFIG += console c++17

INCLUDEPATH += ../common
include(../common/common.pri)

LIBS += -L../common -lcommon

SOURCES += \
    main.cpp