#ifndef __COMMAND__PARSER__HPP__
#define __COMMAND__PARSER__HPP__
#include "Command.hpp"
class CommandParser {
public:
    static Command parse(const QString& line) ;
};
#endif