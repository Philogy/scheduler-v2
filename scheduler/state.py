from .symbolic import SymbolicVM, Config
from .graph import FunctionNode, ValueNode, Graph
from dataclasses import dataclass


@dataclass
class State:
    vm: SymbolicVM
    fn_pending_preds: list[int]
    value_remaining_uses: list[int]

    def __hash__(self) -> int:
        return hash((
            self.vm,
            tuple(self.fn_pending_preds),
            tuple(self.value_remaining_uses)
        ))

    @classmethod
    def from_graph(cls, graph: Graph, config: Config) -> 'State':
        vm = SymbolicVM(config)
        spec = graph.target.main_def

        vm.stack = [
            graph.inputs[stack_var]
            for stack_var in spec.inp.stack
        ]
        for var, slot in spec.inp.locals:
            vm.local_set(slot, graph.inputs[var])

        fn_pending_preds = [0] * graph.total_fns
        for fn in graph.fns:
            fn_pending_preds[fn.fid] = len(fn.preds)

        value_remaining_uses = [0] * graph.total_values
        for value in graph.values:
            value_remaining_uses[value.vid] = len(value.consumers) + any(
                value == graph.vars[out]
                for out in graph.target.main_def.out.names()
            )

        return cls(vm, fn_pending_preds, value_remaining_uses)

    def copy(self) -> 'State':
        return State(
            self.vm.copy(),
            self.fn_pending_preds.copy(),
            self.value_remaining_uses.copy()
        )
