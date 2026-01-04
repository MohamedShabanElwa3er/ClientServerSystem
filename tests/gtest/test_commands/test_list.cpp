#include <gtest/gtest.h>
#include "../../../server/commands/ListCommand.hpp"
#include "CommandTestBase.hpp"

TEST(ListCommandTest, ListFiles) {
    CommandTestBase base;
    Command cmd = base.makeCmd("LIST");

    ListCommand l(cmd);
    QString res = l.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
}
