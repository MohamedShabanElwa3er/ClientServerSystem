#ifndef __INFO__COMMAND__HPP__
#define __INFO__COMMAND__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

class InfoCommand : public ICommand {
public:
    explicit InfoCommand(const Command& cmd);
    QString execute(bool& authenticated) override;

private:
    Command m_command;
};
#endif