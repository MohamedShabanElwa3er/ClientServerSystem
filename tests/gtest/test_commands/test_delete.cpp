#include <gtest/gtest.h>
#include "../../../server/commands/DeleteCommand.hpp"
#include "CommandTestBase.hpp"
#include <QFile>

TEST(DeleteCommandTest, DeleteFile) {
    QFile f("del.txt");
    f.open(QIODevice::WriteOnly);
    f.close();

    CommandTestBase base;
    Command cmd = base.makeCmd("DELETE", {"del.txt"});

    DeleteCommand d(cmd);
    QString res = d.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
}
