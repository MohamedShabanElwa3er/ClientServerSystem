#include <gtest/gtest.h>
#include "../../../server/commands/CpuLoadCommand.hpp"
#include "CommandTestBase.hpp"

TEST(CpuLoadCommandTest, CpuLoad) {
    CommandTestBase base;
    Command cmd = base.makeCmd("CPU_LOAD");

    CpuLoadCommand c(cmd);
    QString res = c.execute(base.authenticated);

    EXPECT_TRUE(res.startsWith("OK"));
}
