#pragma once
#include "../../../common/protocol/Command.hpp"

struct CommandTestBase {
    bool authenticated = true;

    Command makeCmd(const QString& name, const QStringList& args = {}) {
        Command c;
        c.name = name;
        c.args = args;
        return c;
    }
};
