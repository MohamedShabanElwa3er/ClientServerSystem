QT += core network
CONFIG += console c++17

INCLUDEPATH += ../common
include(../common/common.pri)

LIBS += -L../common -lcommon

SOURCES += \
    main.cpp \
    core/Server.cpp \
    core/ClientSession.cpp \
    filesystem/FileService.cpp \
    commands/CommandFactory.cpp \
    commands/AuthCommand.cpp \
    commands/CreateCommand.cpp \
    commands/WriteCommand.cpp \
    commands/ReadCommand.cpp \
    commands/ListCommand.cpp \
    commands/AppendCommand.cpp \
    commands/CpuLoadCommand.cpp \
    commands/InfoCommand.cpp \
    commands/DeleteCommand.cpp \
    commands/RenameCommand.cpp 

HEADERS += \
    core/Server.hpp \
    core/ClientSession.hpp \
    filesystem/FileService.hpp \
    commands/ICommand.hpp \
    commands/CommandFactory.hpp \
    commands/AuthCommand.hpp \
    commands/CreateCommand.hpp \
    commands/WriteCommand.hpp \
    commands/ReadCommand.hpp \
    commands/ListCommand.hpp \
    commands/AppendCommand.hpp \
    commands/CpuLoadCommand.hpp \
    commands/InfoCommand.hpp \
    commands/DeleteCommand.hpp \
    commands/RenameCommand.hpp 