#ifndef __SERVER__HPP__
#define __SERVER__HPP__
#include <QTcpServer>

class Server : public QTcpServer {
    Q_OBJECT
public:
    void start(quint16 port);
protected:
    void incomingConnection(qintptr handle) override;
};
#endif