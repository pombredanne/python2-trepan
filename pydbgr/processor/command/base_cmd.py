# -*- coding: utf-8 -*-
"""A base class for debugger commands.

This file is the one module in this directory that isn't a real command
and commands.py needs to take care to avoid instantiating this class
and storing it as a list of known debugger commands.
"""

NotImplementedMessage = "This method must be overriden in a subclass"

class DebuggerCommand():
    """Base Class for Debugger commands. We pull in some helper
    functions for command from module cmdfns."""

    category = 'misc'

    def __init__(self, proc):
        """proc contains the command processor object that this
        command is invoked through.  A debugger field gives access to
        the stack frame and I/O."""
        self.proc = proc

        # Convenience class access. We don't expect that either core
        # or debugger will change over the course of the program
        # execution like errmsg(), msg(), and msg_nocr() might. (See
        # the note below on these latter 3 methods.)
        # 
        self.core     = proc.core
        self.debugger = proc.debugger
        self.settings = self.debugger.settings
        return

    name_aliases = ('YourCommandName', 'alias1', 'alias2..',)

    def confirm(self, msg, default=False):
        """ Convenience short-hand for self.debugger.intf[-1].confirm """
        return self.debugger.intf[-1].confirm(msg, default)

    # Note for errmsg, msg, and msg_nocr we don't want to simply make
    # an assignment of method names like self.msg = self.debugger.intf.msg,
    # because we want to allow the interface (intf) to change 
    # dynamically. That is, the value of self.debugger may change
    # in the course of the program and if we made such an method assignemnt
    # we wouldn't pick up that change in our self.msg
    def errmsg(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].errmsg """
        return(self.debugger.intf[-1].errmsg(msg))
               
    def msg(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].msg """
        return(self.debugger.intf[-1].msg(msg))
               
    def msg_nocr(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].msg_nocr """
        return(self.debugger.intf[-1].msg_nocr(msg))

        
    def run(self, args):
        """ The method that implements the debugger command.
        Help on the command comes from the docstring of this method.
        """
        raise NotImplementedError, NotImplementedMessage

    pass

if __name__ == '__main__':
    import os, sys
    from import_relative import *
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    dd = DebuggerCommand(cp)
    dd.msg("hi")
    dd.errmsg("Don't do that")