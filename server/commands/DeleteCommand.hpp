#ifndef __DELETE__COMMAND__HPP__
#define __DELETE__COMMAND__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

class DeleteCommand : public ICommand {
public:
    explicit DeleteCommand(const Command& command);
    QString execute(bool& authenticated) override;

private:
    Command m_command;
};

#endif