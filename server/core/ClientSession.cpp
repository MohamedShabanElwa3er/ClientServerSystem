#include "ClientSession.hpp"

#include "../../common/protocol/CommandParser.hpp"
#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../commands/CommandFactory.hpp"

ClientSession::ClientSession(qintptr socketDescriptor, QObject *parent) : QObject(parent), m_socketDescriptor(socketDescriptor)
{
    /* Do Nothing */
}

void ClientSession::start()
{

    m_socket = new QTcpSocket(this);

    if (!m_socket->setSocketDescriptor(m_socketDescriptor)) // setSocketDescriptor() tells Qt: “This socket already exists — take control of it”
    {
        emit finished();
        return;
    }

    connect(m_socket, &QTcpSocket::readyRead, this, &ClientSession::onReadyRead);

    connect(m_socket, &QTcpSocket::disconnected, this, &ClientSession::onDisconnected);
}

void ClientSession::onReadyRead()
{
    while (m_socket->canReadLine())
    {
        QString line = m_socket->readLine();
        Command cmd = CommandParser::parse(line);

  
        if (!authenticated)
        {
            if (cmd.name != "AUTH")
            {
                m_socket->write(Response::error(AUTH_FAILED, "Authentication required").toUtf8());
                continue; // ⬅ do NOT reset auth
            }
        }

        auto command = CommandFactory::create(cmd);

        if (!command)
        {
            m_socket->write(Response::error(BAD_REQUEST, "Unknown command").toUtf8());
            continue; // ⬅ auth state preserved
        }

        QString response = command->execute(authenticated);
        m_socket->write(response.toUtf8());
        m_socket->flush();
    }
}

void ClientSession::onDisconnected()
{
    m_socket->deleteLater();
    emit finished();
}