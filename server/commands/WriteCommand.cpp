#include "WriteCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

#include <QFile>
#include <qdebug.h>
WriteCommand::WriteCommand(const Command &command): m_command(command) 
{
    /*Do Nothing*/
}

QString WriteCommand::execute(bool &)
{
    // Must have filename and data
    qInfo()<<"the write command name is  --> "<<m_command.name;
    qInfo()<<"the write command arg_0 is  --> "<<m_command.args[0];
    qInfo()<<"the write command arg_1 is  --> "<<m_command.args[1];
    if (m_command.args.size() < 2)
    {
        return Response::error(BAD_REQUEST, "Invalid WRITE format");
    }

    const QString filename = m_command.args[0];

    // Reconstruct data (everything after first semicolon)
    QString data = m_command.args.mid(1).join(";");

    // Security check
    if (!PathValidator::validPath(filename))
    {
        return Response::error(BAD_REQUEST, "Invalid file path");
    }

    QFile file(filename);

    // File must already exist
    if (!file.exists())
    {
        return Response::error(FILE_NOT_FOUND, "File not found");
    }

    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate))
    {
        return Response::error(INTERNAL_ERROR, "Cannot write file");
    }

    file.write(data.toUtf8());
    file.close();

    return Response::ok("Data written");
}