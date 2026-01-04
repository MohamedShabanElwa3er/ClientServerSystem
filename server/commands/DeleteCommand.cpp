#include "DeleteCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

#include <QFile>

DeleteCommand::DeleteCommand(const Command &command)
    : m_command(command) {}

QString DeleteCommand::execute(bool &)
{
    // DELETE <filename>
    QString retvalue = "";
    if (m_command.args.size() != 1)
    {
        retvalue = Response::error(BAD_REQUEST, "Invalid DELETE format");
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
                if (!file.remove())
                {
                    retvalue = Response::error(INTERNAL_ERROR, "Cannot delete file");
                }
                else
                {
                    retvalue = Response::ok("File deleted");
                }
            }
        }
    }
    return retvalue;
}