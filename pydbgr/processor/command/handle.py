# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301 USA.

# Our local modules
from import_relative import import_relative
Mbase_cmd  = import_relative('base_cmd')
Msig       = import_relative('sighandler', '...lib', 'pydbgr')

class HandleCommand(Mbase_cmd.DebuggerCommand):
    """handle [SIG [action1 action2 ...]]

Specify how to handle a signal SIG. SIG can be a signal name like
SIGINT or a signal number like 2. The absolute value is used for
numbers so -9 is the same as 9 (SIGKILL). When signal names are used,
you can drop off the leading "SIG" if you want. Also capitalzation is
not important either.

Arguments are signals and actions to apply to those signals.
recognized actions include "stop", "nostop", "print", "noprint",
"pass", "nopass", "ignore", or "noignore".

- Stop means reenter debugger if this signal happens (implies print and
  nopass).
- Print means print a message if this signal happens.
- Pass means let program see this signal; otherwise program doesn't know.
- Ignore is a synonym for nopass and noignore is a synonym for pass.
- Pass and Stop may not be combined. (This is different from gdb)

Without any action names the current settings are shown.

Examples:
  handle INT         # Show current settings of SIGINT
  handle SIGINT      # same as above
  handle int         # same as above
  handle 2           # Probably the same as above
  handle -2          # the same as above
  handle INT nostop  # Don't stop in the debugger on SIGINT
"""

    category     = 'running'
    min_args      = 1
    max_args      = None
    name_aliases = ('handle',)
    need_stack    = False
    short_help    = "Specify how to handle a signal"
    
    def run(self, args):
        if (self.debugger.sigmgr.action(' '.join(args[1:]))
            and len(args) > 2):
            # Show results of recent change
            self.debugger.sigmgr.info_signal([args[1]])
            pass
        return 
    pass

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = HandleCommand(d.core.processor)
    command.run(['handle', 'USR1'])
    command.run(['handle', 'term', 'stop'])
    pass

