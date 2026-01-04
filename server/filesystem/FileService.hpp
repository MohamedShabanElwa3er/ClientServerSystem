#ifndef __FILE__SERVER__HPP__
#define __FILE__SERVER__HPP__
#include <QString>

class FileService {
public:
    static bool create(const QString& name);
    static QString read(const QString& name);
};
#endif