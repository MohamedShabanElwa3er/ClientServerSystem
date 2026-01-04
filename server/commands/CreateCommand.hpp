#ifndef __CREATE_COMMAND_HPP__
#define __CREATE_COMMAND_HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

/*
 * CREATE <filename>
 * Example:
 *   CREATE hi.txt
 */
class CreateCommand : public ICommand {
public:
    explicit CreateCommand(const Command& command);

    QString execute(bool& authenticated) override;

private:
    Command m_command;
};
#endif