#include <QtTest>
#include "../../../common/protocol/Command.hpp"
#include "../../../server/commands/InfoCommand.hpp"

class TestInfoCommand : public QObject {
    Q_OBJECT
private slots:
    void infoFile() {
        QFile f("info.txt");
        QVERIFY(f.open(QIODevice::WriteOnly));
        f.write("data");
        f.close();

        Command cmd;
        cmd.name = "INFO";
        cmd.args = {"info.txt"};

        bool auth = false;
        InfoCommand info(cmd);
        QString res = info.execute(auth);

        QVERIFY(res.startsWith("OK"));
        QFile::remove("info.txt");
    }
};

QTEST_MAIN(TestInfoCommand)
#include "test_info.moc"
