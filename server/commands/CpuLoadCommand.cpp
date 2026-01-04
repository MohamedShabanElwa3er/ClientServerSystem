#include "CpuLoadCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include <QRegularExpression>

#include <QFile>
#include <QStringList>

/**
 * 
[0] "cpu"
[1] "2255"      // user
[2] "34"        // nice
[3] "2290"      // system
[4] "22625563"  // idle
[5] "6290"      // iowait
[6] "127"       // irq
[7] "456"       // softirq

*/


CpuLoadCommand::CpuLoadCommand(const Command &cmd) : m_command(cmd)
{
    /*DoNothing*/
}

double CpuLoadCommand::readCpuLoad()
{
    QFile file("/proc/stat");
    double retval = 0.00;
    QString line{};
    QStringList values{};
    static long long lastIdle = 0;
    static long long lastTotal = 0;
    long long idle = 0;
    long long total = 0;
    long long diffIdle = 0;
    long long diffTotal = 0;
    if (!file.open(QIODevice::ReadOnly))
    {
        retval = -1;
    }
    else
    {
        line = file.readLine();
        values = line.split(QRegularExpression("\\s+"), Qt::SkipEmptyParts);
        idle = values[4].toLongLong();
        for (int i = 1; i < values.size(); ++i)
        {
            total += values[i].toLongLong();
        }

        diffIdle = idle - lastIdle;
        diffTotal = total - lastTotal;

        lastIdle = idle;
        lastTotal = total;
        retval = (diffTotal == 0) ? 0 : (1.0 - (double)diffIdle / diffTotal) * 100.0;
        file.close();
    }
    return retval;
}

QString CpuLoadCommand::execute(bool &)
{
    double load = readCpuLoad();
    if (load < 0)
    {
        return Response::error(INTERNAL_ERROR, "CPU load unavailable");
    }
    else
    {
        return QString("OK %1\n").arg(QString::number(load, 'f', 2));
    }
}