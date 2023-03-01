import re

from keyword import iskeyword
from dataclasses import dataclass

from prettyprinter import cpprint as pp, register_pretty, pretty_call

#------------------------------------------------------------------------------

# Options:  -<letter> or --<word>
# Values:   '<'<word>'>' or plain word
#
# All words folded to lowercase.
#
# Resolve to arguments object with values and options in separate name spaces :
#   a.opt.<option_name>
#   a.val.<value_name>
#
# i.e. --test-name => f.opt.test_name
#      FILE        => f.val.file

def fields(args):

    if ( '--debug' in args and args['--debug'] and
         '--verbose' in args and bool(args['--verbose']) ) :
        pp(args)

    # { <field-name> : <value> , ... }
    options = { }
    values = { }

    # Options: -<letter> or --<word>
    def option ( key ):
        field = key.lower()
        if field.startswith('-'):
            field = field[1:]
        if field.startswith('-'):
            field = field[1:]
        field = field.replace('-','_')
        if hasattr(options, field):
            raise ValueError("Options, resolved field name clash '{field}' -- please address")
        options[field] = args[key]

    # Positional arguments: <name> , or name, or NAME
    def value ( key ):
        field = key.lower().strip('<>')
        if hasattr(values, field):
            raise ValueError("Values, resolved field name clash '{field}' -- please address")
        values[field] = args[key]

    for key in args:
        if key.startswith('-') or isinstance(args[key], bool):
            option(key)
        else:
            value(key)

    # print('[options]') ; pp(options) ; print("\n- - - - -\n")
    # Options = namedtuple('Options', ' '.join(options.keys()))
    named_attributes('Options', ' '.join(options.keys()))
    opt = Options(*options.values())
    # print('[options]') ; pp(opt) ; print("\n- - - - -\n")

    # print('[values]') ; pp(values) ; print("\n- - - - -\n")
    # Values = namedtuple('Values', ' '.join(values.keys()))
    named_attributes('Values', ' '.join(values.keys()))
    val = Values(*values.values())
    # print('[values]') ; pp(val) ; print("\n- - - - -\n")

    def Arguments_init ( self, opt, val ):
        self.opt = opt
        self.val = val

    Arguments = type("Arguments", (object,), {"__init__" : Arguments_init})

    @register_pretty(Arguments)
    def pretty_Arguments(value, ctx):
        return pretty_call(
            ctx,
            Arguments,
            opt=value.opt,
            val=value.val,
        )

    argx = Arguments(opt, val)

    def argx_str ( a ):
        return "Arguments( opt = {repr(a.opt)}, val = {repr(a.val)} )"
    setattr ( argx, '__str__', argx_str )
    setattr ( argx, '__repr__', argx_str )

    # pp(argx)

    return argx

# ------------------------------------------------------------------------------

def named_attributes(name, field_name_string, bases=(object,)):
    """
    Create data class with the named fields.  Same interface as namedtuple()
    but the instance attributes are mutable.

    An optional third arguent lets you specify a base class or classes.  It
    must be either a str, type or tuple of such.
    """

    if not isinstance(bases, tuple):
        bases = (bases,)

    bases = list(bases)

    for idx in range(len(bases)):
        base = bases[idx]
        if isinstance(base, type):
            base = bases[idx] = base.__name__
        if not isinstance(base, str):
            raise TypeError("Members the <base> tuple may be either a type "
                            f"or type name (str), not '{str(type(base))}' "
                            f"(base member {1+idx})")

    bases_string = ', '.join(bases)

    code = f"""
        from dataclasses import dataclass
        @dataclass
        class {name} ({bases_string}):
            pass
"""

    pretty = f"""
        @register_pretty({name})
        def pretty_{name}(value, ctx):
            return pretty_call(
                ctx,
                {name},
"""

    for field_name in field_name_string.split():
        if iskeyword(field_name):
            field_name += '_'
        code += f"            {field_name} : object\n"
        pretty += f"                {field_name} = value.{field_name},\n"

    pretty += "            )\n"

    def dedent(text, n):
        prefix = ' ' * n
        lines = text.splitlines()
        for idx in range(len(lines)):
            if lines[idx].startswith(prefix):
                lines[idx] = lines[idx][n:]
        return "\n".join(lines)

    def remove_matching_lines(text, regex):
        # print(f": remove lines matching '{regex}'")
        matcher = re.compile(regex)
        lines = text.splitlines()
        found = 0
        idx = 0
        while idx < len(lines):
            if matcher.match(lines[idx]):
                del lines[idx]
                found += 1
                continue
            idx += 1
        # n = code.count('\n')
        # print(f": removed {found}, remaining {n}")
        return "\n".join(lines)

    # n = code.count('\n')
    # print(f": code lines = {n}")

    if code.count('\n') > 5:
        code = remove_matching_lines(code, r'^\s*pass$')

    code = dedent(code, 8)
    pretty = dedent(pretty, 8)
    # print(code)
    # print(pretty)

    exec(code, globals())
    exec(pretty, globals())

#------------------------------------------------------------------------------
