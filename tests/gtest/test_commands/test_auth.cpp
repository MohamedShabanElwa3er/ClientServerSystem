#include <gtest/gtest.h>
#include "../../../server/commands/AuthCommand.hpp"
#include "CommandTestBase.hpp"

TEST(AuthCommandTest, InvalidCredentials) {
    CommandTestBase base;
    Command cmd = base.makeCmd("AUTH", {"bad,bad"});

    bool auth = false;
    AuthCommand a(cmd);
    QString res = a.execute(auth);

    EXPECT_FALSE(auth);
    EXPECT_TRUE(res.startsWith("ERROR"));
}

TEST(AuthCommandTest, validCredentials) {
    CommandTestBase base;
    Command cmd = base.makeCmd("AUTH", {"bad,bad"});

    bool auth = false;
    AuthCommand a(cmd);
    QString res = a.execute(auth);

    EXPECT_FALSE(auth);
    EXPECT_TRUE(res.startsWith("ERROR"));
}

 