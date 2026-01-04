#include "CreateCommand.hpp"

#include "../filesystem/FileService.hpp"
#include "../../common/protocol/Response.hpp"
#include "../../common/protocol/ErrorCodes.hpp"
#include "../../common/security/PathValidator.hpp"

CreateCommand::CreateCommand(const Command& command)
    : m_command(command) {}

QString CreateCommand::execute(bool&)
{
    // Must have exactly one argument: filename
    if (m_command.args.size() != 1) {
        return Response::error(BAD_REQUEST, "Invalid CREATE format");
    }

    const QString filename = m_command.args[0];

    // Security: reject unsafe paths
    if (!PathValidator::validPath(filename)) {
        return Response::error(BAD_REQUEST, "Invalid file path");
    }

    // Attempt to create file
    if (!FileService::create(filename)) {
        return Response::error(INTERNAL_ERROR, "File exists or cannot be created");
    }

    return Response::ok("File created");
}