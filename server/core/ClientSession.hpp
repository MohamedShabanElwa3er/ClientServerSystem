#ifndef __CLIENT__SESSION__HPP__
#define __CLIENT__SESSION__HPP__

#include <QObject>
#include <QTcpSocket>

class ClientSession : public QObject {
    Q_OBJECT
public:
    explicit ClientSession(qintptr socketDescriptor, QObject* parent = nullptr);

public slots:
    void start();
    void onReadyRead();
    void onDisconnected();

signals:
    void finished();

private:
    qintptr m_socketDescriptor;
    QTcpSocket* m_socket = nullptr;
    bool authenticated = false;
};

#endif