#include <gtest/gtest.h>
#include "../../../server/commands/CreateCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(CreateCommandTest, CreateFile) {
    CommandTestBase base;
    Command cmd = base.makeCmd("CREATE", {"create.txt"});

    CreateCommand c(cmd);
    QString res = c.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
    EXPECT_TRUE(QFile::exists("create.txt"));

    QFile::remove("create.txt");
}
