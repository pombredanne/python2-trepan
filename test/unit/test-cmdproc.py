#!/usr/bin/env python
'Unit test for pydbgr.processor.cmdproc'
import inspect, os, sys, unittest
from import_relative import import_relative

Mcmdproc = import_relative('processor.cmdproc', '...pydbgr')
Mmock    = import_relative('processor.command.mock', '...pydbgr')

class TestCmdProc(unittest.TestCase):

    def setUp(self):
        self.errors             = []
        self.msgs               = []
        self.d                  = Mmock.MockDebugger()
        self.cp                 = Mcmdproc.CommandProcessor(self.d.core)
        self.cp.intf[-1].msg    = self.msg 
        self.cp.intf[-1].errmsg = self.errmsg
        return

    def errmsg(self, msg):
        self.errors.append(msg)
        return

    def msg(self, msg):
        self.msg.append(msg)
        return

    def test_basic(self):

        # We assume there's at least one command
        self.assertTrue(len(self.cp.name2cmd) > 0)
        self.assertTrue(len(self.cp.alias2name) > 0)

        # In fact we assume there is a 'quit' command...
        self.assertEqual('quit', Mcmdproc.resolve_name(self.cp, 'quit'))
        #   with alias 'q'
        self.assertEqual('quit', Mcmdproc.resolve_name(self.cp, 'q'))
#         processor.cmdproc.print_source_line(self.msg, 100, 
#                                             'source_line_test.py')

        self.cp.frame = sys._getframe()
        self.cp.setup()
        self.assertEqual(3, self.cp.eval('1+2'))
        return

    def test_class_vars(self):
        for cmd in self.cp.name2cmd.values():
            for attr in ['category', 'min_args', 'max_args', 'name_aliases',
                         'need_stack', 'short_help']:
                name = cmd.__class__
                self.assertTrue(hasattr(cmd, attr),
                                '%s command should have a %s attribute' %
                                (name, attr))
                pass
            if cmd.min_args is not None:
                if cmd.max_args is not None:
                    self.assertTrue(cmd.min_args <= cmd.max_args,
                                    "%s min_args: %d, max_args: %d" % 
                                    (name, cmd.min_args, cmd.max_args))
                    pass
                pass
            pass

    def test_args_split(self):
        for test, expect in (
            ("Now is the time",    [['Now', 'is', 'the', 'time']],),
            ("Now is the time ;;", [['Now', 'is', 'the', 'time'], []],),
            ("Now is 'the time'",  [['Now', 'is', "'the time'"]]),
            ("Now is the time ;; for all good men",
             [['Now', 'is', 'the', 'time'], ['for', 'all', 'good', 'men']],),
            ("Now is the time ';;' for all good men",
             [['Now', 'is', 'the', 'time', "';;'", 
               'for', 'all', 'good', 'men']],)
            ):
            self.assertEqual(expect, Mcmdproc.arg_split(test))
            pass
        return

    def test_parse_position(self):
        self.cp.frame = sys._getframe()
        self.cp.setup()

        # See that we can parse a file/line combo: e.g. filename.py:10 
        filename = os.path.realpath(os.path.abspath(__file__))
        modfunc, f, l = self.cp.parse_position("%s:10" % filename)
        self.assertEqual(filename, f, 'file:line parsing bolixed')

        # Without the line number should be a problem though
        modfunc, f, l = self.cp.parse_position(filename)
        self.assertEqual(None, f, 'file should not work')
        return 


    def test_parse_position_one_arg(self):
        self.assertEqual((None, None, None), 
                         self.cp.parse_position_one_arg('4+1'))
        self.cp.frame = sys._getframe()
        self.cp.setup()
        modfunc, f, l = self.cp.parse_position_one_arg('4+1')
        self.assertEqual(5, l)
        self.assertTrue(f.endswith('test-cmdproc.py'))
        self.assertEqual(None, modfunc)

        # See that we can a module name
        modfunc, f, l = self.cp.parse_position_one_arg('os.path')
        self.assertTrue(inspect.ismodule(modfunc),
                        'Module name, e.g. os.path bolixed')

        def foo(): pass
        for name in ('os.path.join', 'foo', 'self.test_parse_position_one_arg'):
            modfunc, f, l = self.cp.parse_position_one_arg(name)
            self.assertTrue(inspect.isfunction(modfunc),
                            'function name %s bolixed' % name)
            pass
        return

    def test_preloop_hooks(self):
        fn = self.cp.name2cmd['list']
        self.assertEqual(0, len(self.cp.preloop_hooks),
                         'Should start out with no preloop hooks')
        self.assertEqual(False, self.cp.remove_preloop_hook(fn),
                         'Should not be able to return a non-existent hook')
        self.cp.add_preloop_hook(fn)
        self.assertEqual(1, len(self.cp.preloop_hooks),
                         'Should now have one preloop hook added')
        self.assertEqual(True, self.cp.remove_preloop_hook(fn))
        self.assertEqual(0, len(self.cp.preloop_hooks),
                         'Should be back to no preloop hooks')
        # FIXME try adding and running a couple of hooks.
        return

if __name__ == '__main__':
    unittest.main()
    pass