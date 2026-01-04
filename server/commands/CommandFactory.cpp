#include "CommandFactory.hpp"

#include "AuthCommand.hpp"
#include "CreateCommand.hpp"
#include "WriteCommand.hpp"
#include "ReadCommand.hpp"
#include "ListCommand.hpp"
#include "AppendCommand.hpp"
#include "InfoCommand.hpp"
#include "CpuLoadCommand.hpp"
#include "DeleteCommand.hpp"
#include "RenameCommand.hpp"
#include <unordered_map>
#include <functional>

using FactoryFn = std::function<std::unique_ptr<ICommand>(const Command&)>;

static const std::unordered_map<QString, FactoryFn> commandMap = 
{
    { "AUTH",      [](const Command& c) { return std::make_unique<AuthCommand>(c); } },
    { "CREATE",    [](const Command& c) { return std::make_unique<CreateCommand>(c); } },
    { "WRITE",     [](const Command& c) { return std::make_unique<WriteCommand>(c); } },
    { "READ",      [](const Command& c) { return std::make_unique<ReadCommand>(c); } },
    { "LIST",      [](const Command& c) { return std::make_unique<ListCommand>(c); } },
    { "APPEND",    [](const Command& c) { return std::make_unique<AppendCommand>(c); } },
    { "INFO",      [](const Command& c) { return std::make_unique<InfoCommand>(c); } },
    { "CPU_LOAD",  [](const Command& c) { return std::make_unique<CpuLoadCommand>(c); } },
    { "DELETE",    [](const Command& c) { return std::make_unique<DeleteCommand>(c); } },
    { "RENAME",    [](const Command& c) { return std::make_unique<RenameCommand>(c); } }
};


std::unique_ptr<ICommand> CommandFactory::create(const Command& cmd)
{
    std::unique_ptr<ICommand> UPtrRet=nullptr;

    auto it = commandMap.find(cmd.name.toUpper());

    UPtrRet = (it != commandMap.end()) ? (it->second(cmd)) : nullptr ;

    return UPtrRet;
}