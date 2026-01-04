#ifndef __COMMAND__FACTORY__HPP__
#define __COMMAND__FACTORY__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"
#include <memory>

class CommandFactory {
public:
    static std::unique_ptr<ICommand> create(const Command& cmd);
};
#endif