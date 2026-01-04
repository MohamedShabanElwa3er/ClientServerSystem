#ifndef __CPU__LOAD__COMMAND__HPP__
#define __CPU__LOAD__COMMAND__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

class CpuLoadCommand : public ICommand {
public:
    explicit CpuLoadCommand(const Command& cmd);
    QString execute(bool& authenticated) override;

private:
    Command m_command;
    double readCpuLoad();
};
#endif