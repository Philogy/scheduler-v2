from lark import Lark, Transformer
from .evm import EVM_EXT
from .target import *

PARSER = Lark(
    '''
    %import common.CNAME
    %import common.WS
    %import common.INT

    start: (ext_def | sub_group)* main

    ext_def: "ext" CNAME "[" fn_def "]"
    fn_def: deps? affects? "in:" data_layout "out:" data_layout

    deps: "deps" "(" name_list? ")"
    affects: "affects" "(" name_list? ")"

    data_layout: "[" name_list? "]" local*
    local: CNAME "@" INT

    sub_group: "sub" "[" sub sub+ "]"
    sub: CNAME "(" INT ("," INT)+ ")"

    main: "main" "[" fn_def "]" stmt*

    stmt: call | assign

    assign: single_assign | multi_assign
    single_assign: CNAME "=" expr
    multi_assign: CNAME ("," CNAME)+ ","? "=" call

    expr: INT | CNAME | call
    call: CNAME "(" (expr ("," expr)* ","?)? ")"

    COMMENT: "//" /[^\\n]*/
    name_list: CNAME ("," CNAME)* ","?

    %ignore WS
    %ignore COMMENT
    '''
)


class EVMTransformer(Transformer):
    def start(self, items):
        defs = []
        sub_groups = []
        main_def = None
        statements = []

        for item in items:
            if isinstance(item, NamedSpec):
                defs.append(item)
            elif isinstance(item, list) and all(isinstance(x, Substitution) for x in item):
                sub_groups.append(item)
            elif isinstance(item, tuple) and len(item) == 2:
                main_def, stmts = item
                statements = stmts

        assert main_def is not None

        return Target(
            defs=defs,
            sub_groups=sub_groups,
            main_def=main_def,
            body=statements
        ).validate()

    def ext_def(self, items):
        name, fn_def = items
        return NamedSpec(name=str(name), spec=fn_def)

    def fn_def(self, items):
        deps = set()
        affects = set()
        inp = None
        out = None

        i = 0
        while i < len(items):
            item = items[i]
            if isinstance(item, tuple) and len(item) == 2:
                # This is a tuple of (type, set) where type is either 'deps' or 'affects'
                type_name, value = item
                if type_name == 'deps':
                    deps = value
                elif type_name == 'affects':
                    affects = value
            elif isinstance(item, DataLayout):
                if inp is None:
                    inp = item
                else:
                    out = item
            i += 1

        assert inp is not None
        assert out is not None
        return FuncSpec(inp=inp, out=out, deps=deps, affects=affects)

    def deps(self, items):
        return ('deps', set(items[0]) if items else set())

    def affects(self, items):
        return ('affects', set(items[0]) if items else set())

    def data_layout(self, items):
        stack = []
        locals: list[tuple[str, int]] = []

        if items and isinstance(items[0], list):
            stack = items[0]

        for item in items[1:]:
            if isinstance(item, tuple):
                name, index = item
                assert isinstance(name, str)
                assert isinstance(index, int)
                locals.append((name, index))

        return DataLayout(stack=stack, locals=locals)

    def local(self, items):
        name, index = items
        return (str(name), int(index))

    def sub(self, items):
        name = str(items[0])
        params = [int(x) for x in items[1:]]
        return Substitution(name=name, params=params)

    def main(self, items):
        fn_def, *statements = items
        return fn_def, statements

    def stmt(self, items):
        item = items[0]
        assert isinstance(item, Statement)
        return item

    def call(self, items):
        name, *args = items
        assert all(isinstance(arg, Expr) for arg in args)
        return Call(name=name, args=args)

    def assign(self, items):
        return items[0]

    def single_assign(self, items):
        to, expr = items
        return SingleAssign(to=str(to), expr=expr)

    def multi_assign(self, items):
        *targets, call = items
        return MultiAssign(to=[str(t) for t in targets], call=call)

    def expr(self, items):
        item, = items
        if isinstance(item, str) and item.isdigit():
            return int(item)
        return item

    def name_list(self, items):
        return list(map(str, items))

    def INT(self, token):
        return int(token)

    def CNAME(self, token):
        return str(token)


def parse_to_target(input: str) -> Target:
    tree = PARSER.parse(EVM_EXT + '\n' + input)
    target = EVMTransformer().transform(tree)
    assert isinstance(target, Target)
    return target
