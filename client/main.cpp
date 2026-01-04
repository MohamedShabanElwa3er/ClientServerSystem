#include <QTcpSocket>
#include <QTextStream>
#include <QCoreApplication>

int main(int argc, char* argv[])
{
    QCoreApplication app(argc, argv);

    QTcpSocket socket;
    QTextStream in(stdin);
    QTextStream out(stdout);

    socket.connectToHost("127.0.0.1", 12345);
    if (!socket.waitForConnected(3000)) 
    {
        out << "Failled to Connect With the Server \n";
        return 1;
    }
    else
    {
        out << "Connection Established with the Server \n";
    }

    while (true) {
        out << "> " << Qt::flush;
        QString line = in.readLine(); 
        if (line.isNull()) // Detects EOF (Ctrl+D / Ctrl+Z) Exits the loop cleanly
            break;

        socket.write((line + "\n").toUtf8()); //the server requires a newline to detect a full command.

        socket.flush(); // Forces Qt to send buffered data immediately

        // Read ALL server response
        if (!socket.waitForReadyRead(3000)) {
            out << "No response from server\n";
            continue;
        }

        QByteArray response; // Creates a buffer to store server response bytes
        do {
            response += socket.readAll();
        } while (socket.waitForReadyRead(50));

        out << response;
    }

    return 0;
}