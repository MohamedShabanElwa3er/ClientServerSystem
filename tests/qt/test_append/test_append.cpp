#include <QtTest>
#include "../../../common/protocol/Command.hpp"
#include "../../../server/commands/AppendCommand.hpp"

class TestAppendCommand : public QObject {
    Q_OBJECT
private slots:
    void appendNewLine() {
        QFile f("append.txt");
        QVERIFY(f.open(QIODevice::WriteOnly));
        f.write("Line1");
        f.close();

        Command cmd;
        cmd.name = "APPEND";
        cmd.args = {"append.txt", "Line2"};

        bool auth = false;
        AppendCommand a(cmd);
        QString res = a.execute(auth);

        QVERIFY(res.startsWith("OK"));
        QVERIFY(QFile("append.txt").open(QIODevice::ReadOnly));

        QFile::remove("append.txt");
    }
};

QTEST_MAIN(TestAppendCommand)
#include "test_append.moc"
