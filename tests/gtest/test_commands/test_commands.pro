QT -= gui
CONFIG += console c++17
TEMPLATE = app

INCLUDEPATH += \
    ../../../common \
    ../../../server \
    /usr/include

LIBS += \
    -L/usr/lib -lgtest -lgtest_main -lpthread \
    -L../../../common -lcommon

SOURCES += \
    test_auth.cpp \
    test_create.cpp \
    test_write.cpp \
    test_append.cpp \
    test_read.cpp \
    test_list.cpp \
    test_info.cpp \
    test_delete.cpp \
    test_rename.cpp \
    test_cpu.cpp \
    ../../../server/commands/AuthCommand.cpp \
    ../../../server/commands/CreateCommand.cpp \
    ../../../server/commands/WriteCommand.cpp \
    ../../../server/commands/AppendCommand.cpp \
    ../../../server/commands/ReadCommand.cpp \
    ../../../server/commands/ListCommand.cpp \
    ../../../server/commands/InfoCommand.cpp \
    ../../../server/commands/DeleteCommand.cpp \
    ../../../server/commands/RenameCommand.cpp \
    ../../../server/commands/CpuLoadCommand.cpp \
    ../../../server/filesystem/FileService.cpp   # ✅ ADD THIS