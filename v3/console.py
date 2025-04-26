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
        if len(args) < 2:
            print("provide all required args")
            return True
        [username, days] = [args[0], int(args[1])]
        posts(username, days)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
