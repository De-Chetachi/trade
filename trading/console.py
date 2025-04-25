#!/usr/bin/env python3

import cmd
from request import posts


class HBNBCommand(cmd.Cmd):
    """
    this is a class defines the CI
    It inherits from class Cmd int the cmd module
    """
    prompt = "(trade) "

    def do_quit(self, line):
        """handles the quit command"""
        return True

    def do_EOF(self, line):
        """handles the end of file condition"""
        return True

    def do_run(self, arg):
        args = arg.split()
        if len(args) < 4:
            print("provide all required args")
            return True
        [username, coin, ticker, days] = [args[0], args[1], args[2], int(args[3])]
        posts(username, coin, ticker, days)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
