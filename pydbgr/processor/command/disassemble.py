# -*- coding: utf-8 -*-
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from import_relative import import_relative

# Our local modules
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns   = import_relative('cmdfns', top_name='pydbgr')
Mdis      = import_relative('disassemble', '...lib', 'pydbgr')

class DisassembleCommand(Mbase_cmd.DebuggerCommand):
    """disassemble [obj-or-class] [[+|-]start-line|. [[+|-]end-line|.]]
    
With no argument, disassemble the current frame.  With an integer
start-line, the disassembly is narrowed to show lines starting
at that line number or later; with an end-line number, disassembly
stops when the next line would be greater than that or the end of the
code is hit.

If start-line or end-line is '.', '+', or '-', the current line number
is used.  If instead it starts with a plus or minus prefix to a
number, then the line number is relative to the current frame number.

With a class, method, function, code or string argument disassemble
that.

Examples

   disassemble    # Possibly lots of stuff dissassembled
   disassemble .  # Disassemble lines starting at current stopping point.
   disassemble +                  # Same as above
   disassemble +0                 # Same as above
   disassemble os.path            # Disassemble all of os.path
   disassemble os.path.normcase   # Disaassemble just method os.path.normcase
   disassemble -3  # Disassemble subtracting 3 from the current line number 
   disassemble +3  # Disassemble adding 3 from the current line number 
   disassemble 3   # Disassemble starting from line 3
   disassemble 3 10  # Disassemble lines 3 to 10
"""

    category      = 'data'
    min_args      = 0
    max_args      = 2
    name_aliases  = ('disassemble','disas') # Note: we will have disable
    need_stack    = True
    short_help    = 'Disassemble Python bytecode'

    def parse_arg(self, arg):
        if arg in ['+', '-', '.']:
            return self.proc.curframe.f_lineno, True
        lineno = self.proc.get_int_noerr(arg)
        if lineno is not None:
            if arg[0:1] in ['+', '-']:
                return lineno + self.proc.curframe.f_lineno, True
            else:
                return lineno, False
            pass
        return None, None

    def run(self, args):
        start_line = end_line = None
        if not self.proc.curframe:
            self.errmsg("No frame selected.")
            return
        relative_pos = False
        if len(args) > 1:
            start_line, relative_pos = self.parse_arg(args[1])
            if start_line is None:
                # First argument should be an evaluatable object
                try:
                    obj=self.proc.eval(args[1])
                except:
                    self.errmsg(("Object '%s' is not something we can"
                                 + " disassemble.") % args[1])
                    return 
                if len(args) > 2:
                    start_line, relative_pos = self.parse_arg(args[2])
                    if start_line is None:
                        self.errmsg = ('Start line should be a number. Got %s.' 
                                       % args[2])
                        return
                    if len(args) == 4:
                        end_line, relative_pos = self.parse_arg(args[3])
                        if end_line is None: 
                            self.errmsg = ('End line should be a number. ' +
                                           ' Got %s.' % args[3])
                            return
                        pass
                    elif len(args) > 4:
                        self.errmsg("Expecting 0-3 parameters. Got %d" %
                                    len(args)-1)
                        return
                    pass
                
                try:
                    obj=Mcmdfns.get_val(self.proc.curframe, 
                                        self.errmsg, args[1])
                except:
                    return
                pass
                Mdis.dis(self.msg, self.msg_nocr, self.errmsg, obj, 
                         start_line=start_line, end_line=end_line, 
                         relative_pos=relative_pos)
            else:
                if len(args) == 3:
                    end_line, not_used = self.parse_arg(args[2])
                    if end_line is None: 
                        self.errmsg = ('End line should be a number. ' +
                                       ' Got %s.' % args[2])
                        return
                    pass
                elif len(args) > 3:
                    self.errmsg("Expecting 1-2 line parameters. Got %d." %
                                len(args)-1)
                    return False
                pass
            pass
        Mdis.dis(self.msg, self.msg_nocr, self.errmsg, 
                 self.proc.curframe, 
                 start_line=start_line, end_line=end_line, 
                 relative_pos=relative_pos)
        return False

# Demo it
if __name__ == '__main__':
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    import inspect
    cp.curframe = inspect.currentframe()
    command = DisassembleCommand(cp)
    prefix = '-' * 20 + ' disassemble '
    print prefix + 'cp.errmsg'
    command.run(['dissassemble', 'cp.errmsg'])
    print prefix
    command.run(['disassemble'])
    print prefix + 'me'
    command.run(['disassemble', 'me'])
    print prefix + '+0 2'
    command.run(['disassemble', '+0', '2'])
    print prefix + '+ 2-1'
    command.run(['disassemble', '+', '2-1'])
    print prefix + '- 1'
    command.run(['disassemble', '-', '1'])
    print prefix + '.'
    command.run(['disassemble', '.'])
    pass
