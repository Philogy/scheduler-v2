from typing import Optional
from dataclasses import dataclass
from collections import defaultdict
from abc import ABC
from .target import *


class Producer(ABC):
    pass


@dataclass
class Const(Producer):
    value: int


class FunctionNode(Producer):
    calls: str
    preds: set['FunctionNode']
    succs: set['FunctionNode']
    inputs: list['ValueNode']
    outputs: list['ValueNode']

    def __init__(self, calls: str, inputs: list['ValueNode']) -> None:
        self.calls = calls
        self.preds = set()
        self.succs = set()
        self.inputs = inputs
        for inp in inputs:
            inp.consumers.add(self)
        self.outputs = []

    def set_outputs(self, outs: list['ValueNode']):
        for out in outs:
            out.producer = self
        self.outputs = outs

    def add_pred(self, node: 'FunctionNode'):
        self.preds.add(node)
        node.succs.add(self)


class ValueNode:
    name: Optional[str]
    producer: Optional[Producer]
    consumers: set[FunctionNode]

    def __init__(self, name: Optional[str], producer: Optional[Producer]) -> None:
        self.name = name
        self.producer = producer
        self.consumers = set()


class GraphBuilder:
    target: Target
    vars: dict[str, ValueNode]
    last_deps: dict[str,  set[FunctionNode]]
    last_affects: dict[str, FunctionNode]
    specs: dict[str, NamedSpec]
    fns: set[FunctionNode]

    def __init__(self, target: Target):
        self.target = target
        self.vars = {}
        self.last_deps = defaultdict(set)
        self.last_affects = {}
        self.fns = set()

        self.specs: dict[str, NamedSpec] = {
            d.name: d
            for d in target.defs
        }

        for inp in target.main_def.inp.names():
            self.vars[inp] = ValueNode(inp, None)

        for stmt in target.body:
            if isinstance(stmt, Call):
                outs = self.add_expr(stmt)
                assert not outs, f'Expected {stmt.name!r} to have 0 outputs, returned {len(outs)}'
            elif isinstance(stmt, SingleAssign):
                outs = self.single_arg_expr(stmt.expr)
                self.vars[stmt.to] = outs
            else:
                assert isinstance(stmt, MultiAssign), f'{stmt}'
                outs = self.add_expr(stmt.call)
                assert len(outs) == len(stmt.to), \
                    f'Expected {stmt.call.name!r} to have {len(stmt.to)} outputs, got {len(outs)}'
                for to, out in zip(stmt.to, outs):
                    self.vars[to] = out

    def single_arg_expr(self, expr: Expr) -> ValueNode:
        nodes_out = self.add_expr(expr)
        assert len(nodes_out) == 1, \
            f'Expected exactly 1 value node, got: {len(nodes_out)} ({expr})'
        return nodes_out[0]

    def add_expr(self, expr: Expr) -> list[ValueNode]:
        if isinstance(expr, int):
            const = Const(expr)
            return [ValueNode(f'const:{expr}', const)]

        if isinstance(expr, str):
            assert (value := self.vars.get(expr)) is not None, \
                f'Variable {expr!r} not defined'
            return [value]

        assert isinstance(expr, Call)
        assert (named_spec := self.specs.get(expr.name)) is not None, \
            f'Referenced function {expr.name!r} not found'
        spec = named_spec.spec
        assert spec.inp.size() == len(expr.args), \
            f'Calling with {expr.name!r} with {len(expr.args)} expected {spec.inp.size}'

        inputs = [
            self.single_arg_expr(arg)
            for arg in expr.args
        ]

        fn = FunctionNode(named_spec.name, inputs)
        self.fns.add(fn)

        fn.set_outputs(outputs := [
            ValueNode(f'call[{expr.name!r}]={i + 1}', fn)
            for i in range(spec.out.size())

        ])

        spec.validate()  # not needed, sanity check

        for affect in spec.affects:
            if (last_deps := self.last_deps.get(affect)) is not None:
                for dep in last_deps:
                    fn.add_pred(dep)
                self.last_deps[affect].clear()

            if (last_affect := self.last_affects.get(affect)) is not None:
                fn.add_pred(last_affect)

            self.last_affects[affect] = fn

        for dep in spec.deps:
            if (last_affect := self.last_affects.get(dep)) is not None:
                fn.add_pred(last_affect)
            self.last_deps[dep].add(fn)

        return outputs
