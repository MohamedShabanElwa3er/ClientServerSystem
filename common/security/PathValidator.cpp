#include "PathValidator.hpp"

bool PathValidator::validPath(const QString& path)
{
    bool retvalue = true;
    if (path.startsWith('/') || path.contains(':') || path.contains("..") || path.contains('/') || path.contains('\\'))
    {
        retvalue = false;
    }
    return retvalue ;
}