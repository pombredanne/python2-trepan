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

import columnize
from import_relative import import_relative

# Our local modules
Mbase_subcmd  = import_relative('base_subcmd', '..', 'pydbgr')

class ShowAliases(Mbase_subcmd.DebuggerShowIntSubcommand):
    '''show aliases [ALIAS ...| *]

 Show command aliases. If parameters are given a list of all aliases and
the command they run are printed. Alternatively one can list specific
alias names for the commands those specific aliases are attached to.
If instead of an alias '*' appears anywhere as an alias then just a list
of aliases is printed, not what commands they are attached to.
'''

    min_abbrev = 2 # Need at least "show al"
    short_help = "Show command aliases"
    run_cmd    = False

    def _alias_header(self):
        self.msg("%-10s : %s" % ('Alias', 'Command'))
        self.msg("%-10s : %s" % ('-' * 10, '-' * 11))
        return

    def _alias_line(self, alias):
        self.msg("%-10s : %s" % (alias, self.proc.alias2name[alias]))
        return

    def run(self, args):
        aliases = self.proc.alias2name.keys()
        aliases.sort()
        if len(args) == 0:
            self._alias_header()
            for alias in aliases:
                self._alias_line(alias)
                pass
            return
        if '*' in args:
            self.msg("Current aliases:")
            self.msg(columnize.columnize(aliases, lineprefix='    '))
        else:
            self._alias_header()
            for alias in args:
                if alias in aliases:
                    self._alias_line(alias)
                else:
                    self.errsg("%s is not an alias" % alias)
                    pass
                pass
            return
        return

if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Mshow = import_relative('show', '..')
    Mdebugger = import_relative('debugger', '....')
    d = Mdebugger.Debugger()
    d, cp = mock.dbg_setup(d)
    i = Mshow.ShowCommand(cp)
    sub = ShowAliases(i)
    sub.run([])
    sub.run(['*'])
    sub.run(['s+', "n+"])
    pass