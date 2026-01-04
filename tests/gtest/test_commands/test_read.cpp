#include <gtest/gtest.h>
#include "../../../server/commands/ReadCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(ReadCommandTest, ReadFile) {
    QFile f("read.txt");
    f.open(QIODevice::WriteOnly);
    f.write("data");
    f.close();

    CommandTestBase base;
    Command cmd = base.makeCmd("READ", {"read.txt"});

    ReadCommand r(cmd);
    QString res = r.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
    QFile::remove("read.txt");
}
