#include "ListCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"

#include <QDir>

ListCommand::ListCommand(const Command &command): m_command(command) 
{
    /*DoNothing*/
}

QString ListCommand::execute(bool &)
{
    // LIST has no arguments
    if (!m_command.args.isEmpty())
    {
        return Response::error(BAD_REQUEST, "Invalid LIST format");
    }

    QDir dir("."); // it is the location wherever the server executable was started
    QStringList entries = dir.entryList(QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot, QDir::Name);

    QString response = QString("OK %1\n").arg(entries.size());
    for (auto &it : entries)
    {
        response += it + "\n";
    }

    return response;
}