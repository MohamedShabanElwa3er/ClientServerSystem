#include "ReadCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

#include <QFile>

ReadCommand::ReadCommand(const Command &command): m_command(command) 
{
    /*DoNothing*/
}

QString ReadCommand::execute(bool &)
{
    // Must have exactly one argument: filename
    QString retvalue = "";
    if (m_command.args.size() != 1)
    {
        retvalue = Response::error(BAD_REQUEST, "Invalid READ format");
    }
    else
    {
        const QString filename = m_command.args[0];

        // Security check
        if (!PathValidator::validPath(filename))
        {
            retvalue = Response::error(BAD_REQUEST, "Invalid file path");
        }
        else
        {
            QFile file(filename);

            if (!file.exists())
            {
                retvalue = Response::error(FILE_NOT_FOUND, "File not found");
            }
            else
            {
                if (!file.open(QIODevice::ReadOnly))
                {
                    retvalue = Response::error(INTERNAL_ERROR, "Cannot read file");
                }
                else
                {
                    const QByteArray content = file.readAll();
                    file.close();
                    QString response = QString("OK %1\n").arg(content.size());
                    response += QString::fromUtf8(content);
                    response += "\n";

                    retvalue = response;
                }
            }
        }
    }
    return retvalue ;
}