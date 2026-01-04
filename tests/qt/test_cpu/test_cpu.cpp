#include <QtTest>
#include "../../../common/protocol/Command.hpp"
#include "../../../server/commands/CpuLoadCommand.hpp"

class TestCpuLoad : public QObject {
    Q_OBJECT
private slots:
    void cpuLoad() {
        Command cmd;
        cmd.name = "CPU_LOAD";
        bool auth = false;

        CpuLoadCommand cpu(cmd);
        QString res = cpu.execute(auth);

        QVERIFY(res.startsWith("OK"));
    }
};

QTEST_MAIN(TestCpuLoad)
#include "test_cpu.moc"
