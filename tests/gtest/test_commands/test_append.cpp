#include <gtest/gtest.h>
#include "../../../server/commands/AppendCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(AppendCommandTest, AppendNewLine) {
    QFile f("append.txt");
    f.open(QIODevice::WriteOnly);
    f.write("Line1");
    f.close();

    CommandTestBase base;
    Command cmd = base.makeCmd("APPEND", {"append.txt", "Line2"});

    AppendCommand a(cmd);
    QString res = a.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
    QFile::remove("append.txt");
}
