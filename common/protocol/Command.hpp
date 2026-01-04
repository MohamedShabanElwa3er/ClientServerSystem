#ifndef __COMMAND__HPP__
#define __COMMAND__HPP__
#include <QString>
#include <QStringList>

struct Command {
    QString name;
    QStringList args;
};
#endif