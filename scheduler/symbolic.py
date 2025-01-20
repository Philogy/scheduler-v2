from dataclasses import dataclass
from typing import Optional, Self
from .graph import ValueNode


class SwapBeyondMaxDepth(Exception):
    pass


class DupBeyondMaxDepth(Exception):
    pass


class StackTooShallow(Exception):
    pass


class MissingLocal(Exception):
    pass


@dataclass
class Config:
    max_dup_depth: int
    max_swap_depth: int


class SymbolicVM:
    stack: list[ValueNode]
    locals: list[Optional[ValueNode]]
    __config: Config

    def __init__(self, config: Config) -> None:
        self.stack = []
        self.locals = []
        self.__config = config

    def __hash__(self) -> int:
        assert self.locals[-1] is not None
        return hash((
            tuple(self.stack),
            tuple(self.locals)
        ))

    @property
    def config(self) -> Config:
        return self.__config

    def pop(self) -> ValueNode:
        if self.stack:
            return self.stack.pop()
        raise StackTooShallow('Cannot pop from empty stack')

    def push(self, node: ValueNode):
        self.stack.append(node)

    def swap(self, depth: int):
        if depth <= 0 or depth > self.config.max_swap_depth:
            raise SwapBeyondMaxDepth(
                f'swap{depth} invalid, max_swap_depth: {self.config.max_swap_depth}'
            )
        if depth > len(self.stack) + 1:
            raise StackTooShallow(
                f'Attempting swap{depth}, stack depth: {len(self.stack)}'
            )
        ni = -depth - 1
        self.stack[ni], self.stack[-1] = self.stack[-1], self.stack[ni]

    def dup(self, depth: int):
        if depth <= 0 or depth > self.config.max_swap_depth:
            raise DupBeyondMaxDepth(
                f'dup{depth} invalid, max_dup_depth: {self.config.max_dup_depth}'
            )
        if depth > len(self.stack):
            raise StackTooShallow(
                f'Attempting dup{depth}, stack depth: {len(self.stack)}'
            )
        self.push(self.stack[-depth])

    def local_get(self, i: int) -> Optional[ValueNode]:
        if i >= len(self.locals):
            return None
        return self.locals[i]

    def local_set(self, i: int, value: ValueNode):
        self.locals.extend([None] * (i - len(self.locals) + 1))
        self.locals[i] = value

    def store(self, i: int):
        self.local_set(i, self.pop())

    def load(self, i: int):
        if (local := self.local_get(i)) is None:
            raise MissingLocal(f'No local[{i}]')
        self.push(local)

    def copy(self) -> 'SymbolicVM':
        new_vm = SymbolicVM(self.config)
        new_vm.stack = self.stack.copy()
        new_vm.locals = self.locals.copy()
        return new_vm

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolicVM):
            raise NotImplementedError(
                f'Comparison not supported between {self.__class__.__name__} and {other}'
            )
        return self.stack == other.stack and self.locals == other.locals
