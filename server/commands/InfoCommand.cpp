#include "InfoCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

#include <QFileInfo>
#include <QDateTime>

InfoCommand::InfoCommand(const Command &cmd) : m_command(cmd)
{
    /*DoNothing*/
}

QString InfoCommand::execute(bool &)
{
    QString retvalue = "";
    QString filename = "";
    if (m_command.args.size() != 1)
    {
        retvalue = Response::error(BAD_REQUEST, "Invalid INFO format");
    }
    else
    {
        filename = m_command.args[0];

        if (!PathValidator::validPath(filename))
        {
            retvalue = Response::error(BAD_REQUEST, "Invalid file path");
        }
        else
        {
            QFileInfo info(filename);
            if (!info.exists())
            {
                retvalue = Response::error(FILE_NOT_FOUND, "File not found");
            }
            else
            {
                retvalue = QString("OK size=%1 modified= ").arg(info.size());
                retvalue += info.lastModified().toString();
            }
        }
    }

    return retvalue;
}