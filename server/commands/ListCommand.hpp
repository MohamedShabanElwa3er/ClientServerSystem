#ifndef __LIST__COMMAND__HPP__
#define __LIST__COMMAND__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

/*
 * LIST
 *
 * Response on success:
 *   OK <count>
 *   <filename>
 *   <filename>
 *   ...
 */
class ListCommand : public ICommand {
public:
    explicit ListCommand(const Command& command);

    QString execute(bool& authenticated) override;

private:
    Command m_command;
};

#endif