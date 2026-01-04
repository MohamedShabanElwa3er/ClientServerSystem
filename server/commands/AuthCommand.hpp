#ifndef __AUTH__COMMAND__HPP__
#define __AUTH__COMMAND__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

/*
 * AUTH <username>,<password>
 */
class AuthCommand : public ICommand {
public:
    explicit AuthCommand(const Command& command);

    QString execute(bool& authenticated) override;

private:
    Command m_command;
};
#endif