#ifndef __I_COMMAND__HPP__
#define __I_COMMAND__HPP__
#include <QString>

class ICommand {
public:
    virtual ~ICommand() = default;
    virtual QString execute(bool& authenticated) = 0;
};
#endif