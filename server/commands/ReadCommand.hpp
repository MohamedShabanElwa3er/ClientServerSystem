#pragma once

#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

/*
 * READ <filename>
 *
 * Response on success:
 *   OK <length>
 *   <file content>
 */
class ReadCommand : public ICommand {
public:
    explicit ReadCommand(const Command& command);

    QString execute(bool& authenticated) override;

private:
    Command m_command;
};