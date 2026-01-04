#include "AppendCommand.hpp"
#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

#include <QFile>
#include <qdebug.h>
AppendCommand::AppendCommand(const Command &command) : m_command(command)
{
    /*DoNothing*/
}

QString AppendCommand::execute(bool &)
{
    QString filename{};
    QString data{};
    QString retvalue{};
    if (m_command.args.size() < 2)
    {
        retvalue = Response::error(BAD_REQUEST, "Invalid WRITE format");
    }
    else
    {

        filename = m_command.args[0];

        // Reconstruct data (everything after first semicolon)
        data = m_command.args.mid(1).join(";");

        // Security check
        if (!PathValidator::validPath(filename))
        {
            retvalue = Response::error(BAD_REQUEST, "Invalid file path");
        }
        else
        {

            QFile file(filename);

            // File must already exist
            if (!file.exists())
            {
                retvalue = Response::error(FILE_NOT_FOUND, "File not found");
            }
            else
            {

                if (!file.open(QIODevice::WriteOnly | QIODevice::Append))
                {
                    retvalue = Response::error(INTERNAL_ERROR, "Cannot write file");
                }
                else
                {

                    if (file.size() > 0)
                    {
                        file.seek(file.size() - 1);
                        char lastChar;
                        file.getChar(&lastChar);

                        if (lastChar != '\n')
                        {
                            file.write("\n");
                        }
                    }

                    // Move to end before appending
                    file.seek(file.size());

                    file.write(data.toUtf8());
                    file.write("\n");
                    file.close();

                    retvalue = Response::ok("Data appended");
                }
            }
        }
    }
    return retvalue;
}