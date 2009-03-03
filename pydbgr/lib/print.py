# -*- coding: utf-8 -*-
#   Copyright (C) 2007, 2008, 2009 Rocky Bernstein
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

import types

def print_dict(s, obj, title):
    if hasattr(obj, "__dict__"):
        obj = obj.__dict__
        pass
    if isinstance(obj, types.DictType) or isinstance(obj, types.DictProxyType):
        s += "\n%s:\n" % title
        keys = obj.keys()
        keys.sort()
        for key in keys:
            s+="  %s:\t%s\n" % (repr(key), obj[key])
            pass
        pass
    return s

def print_obj(arg, frame, format=None, short=False):
    """Return a string representation of an object """
    try:
        if not frame:
            # ?? Should we have set up a dummy globals
            # to have persistence? 
            val = eval(arg, None, None)
        else:
            val = eval(arg, frame.f_globals, frame.f_locals)
            pass
    except:
        return 'No symbol "' + arg + '" in current context.'
    #format and print
    what = arg
    if format:
        what = format + ' ' + arg
        val = printf(val, format)
    s = '%s = %s' % (what, val)
    if not short:
        s += '\ntype = %s' % type(val)
        # Try to list the members of a class.
        # Not sure if this is correct or the
        # best way to do.
        s = print_dict(s, val, "object variables")
        if hasattr(val, "__class__"):
            s = print_dict(s, val.__class__, "class variables")
    return s

pconvert = {'c':chr, 'x': hex, 'o': oct, 'f': float, 's': str}
twos = ('0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
        '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111')

def printf(val, fmt):
    global pconvert, twos
    if not fmt:
        fmt = ' ' # not 't' nor in pconvert
    # Strip leading '/'
    if fmt[0] == '/':
        fmt = fmt[1:]
    f = fmt[0]
    if f in pconvert.keys():
        try:
            return apply(pconvert[f], (val,))
        except:
            return str(val)
    # binary (t is from 'twos')
    if f == 't':
        try:
            res = ''
            while val:
                res = twos[val & 0xf] + res
                val = val >> 4
            return res
        except:
            return str(val)
    return str(val)

if __name__ == '__main__':
    print print_dict('', globals(), 'my globals')
    assert printf(31, "/o") == '037'
    assert printf(31, "/t") == '00011111'
    assert printf(33, "/c") == '!'
    assert printf(33, "/x") == '0x21'