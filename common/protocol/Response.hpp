#ifndef __RESPONSE__HPP__
#define __RESPONSE__HPP__

#include <QString>

class Response {
public:
    static QString ok(const QString& message = "");
    static QString error(int code, const QString& message);
};

#endif