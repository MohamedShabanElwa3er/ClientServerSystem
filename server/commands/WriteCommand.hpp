#ifndef __WRITE__COMMAND__HPP__
#define __WRITE__COMMAND__HPP__
#include "ICommand.hpp"
#include "../../common/protocol/Command.hpp"

/*
 * WRITE <filename>;<data>
 * Everything after the first semicolon is treated as file content
 *
 * Example:
 *   WRITE hi.txt;Hello World
 */
class WriteCommand : public ICommand {
public:
    explicit WriteCommand(const Command& command);

    QString execute(bool& authenticated) override;

private:
    Command m_command;
};
#endif