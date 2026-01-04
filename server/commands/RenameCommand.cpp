#include "RenameCommand.hpp"

#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

#include <QFile>

RenameCommand::RenameCommand(const Command& command)
    : m_command(command) {}

QString RenameCommand::execute(bool&)
{
    // RENAME <oldname>;<newname>
    if (m_command.args.size() != 2) {
        return Response::error(BAD_REQUEST, "Invalid RENAME format");
    }

    const QString oldName = m_command.args[0];
    const QString newName = m_command.args[1];

    // Security checks
    if (!PathValidator::validPath(oldName) ||
        !PathValidator::validPath(newName)) {
        return Response::error(BAD_REQUEST, "Invalid file path");
    }

    QFile file(oldName);

    if (!file.exists()) {
        return Response::error(FILE_NOT_FOUND, "File not found");
    }

    if (!file.rename(newName)) {
        return Response::error(INTERNAL_ERROR, "Rename failed");
    }

    return Response::ok("File renamed");
}