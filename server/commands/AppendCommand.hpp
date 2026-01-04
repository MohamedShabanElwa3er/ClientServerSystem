#ifndef __APPEND__COMMAND__HPP
#define __APPEND__COMMAND__HPP

#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"


class AppendCommand : public ICommand
{
    public:
    explicit AppendCommand(const Command& command);
    
    QString execute(bool& authenticated) override;
    private:
    Command m_command;

};




#endif