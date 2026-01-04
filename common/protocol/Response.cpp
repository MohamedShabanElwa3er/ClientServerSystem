#include "Response.hpp"

QString Response::ok(const QString &message)
{
    return ( message.isEmpty() == true) ? "OK\n" : "OK " + (message + "\n");
}

QString Response::error(int code, const QString &message)
{
    return QString("ERROR %1 %2\n").arg(code).arg(message);
}