#include "Server.hpp"
#include "ClientSession.hpp"
#include "QDebug"
#include <QThread>

void Server::start(quint16 port)
{
    listen(QHostAddress::Any, port);
}

void Server::incomingConnection(qintptr socketDescriptor)
{
    QThread* thread = new QThread;
    
    qInfo()<<"New Thread has been established " ;
    ClientSession* session = new ClientSession(socketDescriptor);
    session->moveToThread(thread);                                     //session->moveToThread(thread); tells Qt which thread is allowed to execute session’s code.

    connect(thread, &QThread::started,session, &ClientSession::start);          // When the thread starts: Calls ClientSession::start()

    connect(session, &ClientSession::finished, thread, &QThread::quit);          // When the client disconnects: Stops the thread’s event loop

    connect(session, &ClientSession::finished, session, &QObject::deleteLater);  //Schedules the ClientSession for deletion Safe deletion inside Qt event loop

    connect(thread, &QThread::finished,thread, &QObject::deleteLater);           // Deletes the thread object after it stops

    thread->start();
}