#include <gtest/gtest.h>
#include "../../../server/commands/WriteCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(WriteCommandTest, WriteFile) {
    QFile("write.txt").open(QIODevice::WriteOnly);

    CommandTestBase base;
    Command cmd = base.makeCmd("WRITE", {"write.txt", "Hello"});

    WriteCommand w(cmd);
    QString res = w.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
    QFile::remove("write.txt");
}
