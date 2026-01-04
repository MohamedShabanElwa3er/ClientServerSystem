#ifndef __RENAME__COMMAND__HPP__
#define __RENAME__COMMAND__HPP__

#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

class RenameCommand : public ICommand {
public:
    explicit RenameCommand(const Command& command);
    QString execute(bool& authenticated) override;

private:
    Command m_command;
};
#endif