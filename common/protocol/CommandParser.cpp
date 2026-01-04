#include "CommandParser.hpp"

Command CommandParser::parse(const QString &line)
{
    Command cmd;
    QString args ="";
    QString trimmed = line.trimmed();
    int space = trimmed.indexOf(' ');

    if (space == -1)
    {
        cmd.name = trimmed;
    }
    else 
    {
        cmd.name = trimmed.left(space);
        args = trimmed.mid(space + 1);
        cmd.args = args.split(';');
    }

    return cmd;
}