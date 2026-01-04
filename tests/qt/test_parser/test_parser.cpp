#include <QtTest>
#include "../../../common/protocol/CommandParser.hpp"

class TestParser : public QObject {
    Q_OBJECT
private slots:
    void parseWrite() {
        Command cmd = CommandParser::parse("WRITE hi.txt;Hello");
        QCOMPARE(cmd.name, QString("WRITE"));
        QCOMPARE(cmd.args[0], QString("hi.txt"));
        QCOMPARE(cmd.args[1], QString("Hello"));
    }
};

QTEST_MAIN(TestParser)
#include "test_parser.moc"
