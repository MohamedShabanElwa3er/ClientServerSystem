#include "core/Server.hpp"
#include <QCoreApplication>

int main(int argc, char *argv[]) {
    QCoreApplication a(argc, argv);
    Server server;
    server.start(12345);
    return a.exec();
}