#include <gtest/gtest.h>
#include "../../../server/commands/InfoCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(InfoCommandTest, FileInfo) {
    QFile f("info.txt");
    f.open(QIODevice::WriteOnly);
    f.write("data");
    f.close();

    CommandTestBase base;
    Command cmd = base.makeCmd("INFO", {"info.txt"});

    InfoCommand i(cmd);
    QString res = i.execute(base.authenticated);

    EXPECT_TRUE(res.contains("size="));
    QFile::remove("info.txt");
}
