#include <gtest/gtest.h>
#include "../../../server/commands/RenameCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(RenameCommandTest, RenameFile) {
    QFile f("old.txt");
    f.open(QIODevice::WriteOnly);
    f.close();

    CommandTestBase base;
    Command cmd = base.makeCmd("RENAME", {"old.txt", "new.txt"});

    RenameCommand r(cmd);
    QString res = r.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
    EXPECT_TRUE(QFile::exists("new.txt"));

    QFile::remove("new.txt");
}
