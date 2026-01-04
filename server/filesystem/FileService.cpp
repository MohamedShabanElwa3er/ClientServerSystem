#include "FileService.hpp"
#include <QFile>

bool FileService::create(const QString &name)
{
    QFile f(name);
    if (f.exists())
        return false;
    return f.open(QIODevice::WriteOnly);
}

QString FileService::read(const QString &name)
{
    QFile f(name);
    if (!f.open(QIODevice::ReadOnly))
        return {};
    return f.readAll();
}