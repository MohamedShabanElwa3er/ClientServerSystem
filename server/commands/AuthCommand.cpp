#include "AuthCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"

AuthCommand::AuthCommand(const Command &command) : m_command(command)
{
    /*DoNothing*/
}

QString AuthCommand::execute(bool &authenticated)
{
    // Expect exactly one argument: username,password
    QString retvalue = "";
    QString username = "";
    QString password = "";
    QStringList creds{};
    if (m_command.args.size() != 1)
    {
        authenticated = false;
        retvalue = Response::error(BAD_REQUEST, "Invalid AUTH format");
    }
    else
    {

        creds = m_command.args[0].split(',');
        if (creds.size() != 2)
        {
            authenticated = false;
            retvalue = Response::error(BAD_REQUEST, "Invalid AUTH format");
        }
        else
        {

            username = creds[0];
            password = creds[1];

            if (username == "admin" && password == "admin")
            {
                authenticated = true;
                retvalue = Response::ok("Authenticated");
            }
            else
            {
                authenticated = false;
                retvalue = Response::error(AUTH_FAILED, "Invalid username or password");
            }
        }
    }
    return retvalue;
}