from typing import Optional
from .graph import ValueNode


class SwapBeyondMaxDepth(Exception):
    pass


class DupBeyondMaxDepth(Exception):
    pass


class StackTooShallow(Exception):
    pass


class MissingLocal(Exception):
    pass


class SymbolicVM:
    stack: list[ValueNode]
    locals: dict[int, ValueNode]
    max_dup_depth: int
    max_swap_depth: int

    def __init__(self, max_dup_depth: int, max_swap_depth: int) -> None:
        self.stack = []
        self.locals = {}
        self.max_dup_depth = max_dup_depth
        self.max_swap_depth = max_swap_depth

    def pop(self) -> ValueNode:
        if self.stack:
            return self.stack.pop()
        raise StackTooShallow('Cannot pop from empty stack')

    def push(self, node: ValueNode):
        self.stack.append(node)

    def swap(self, depth: int):
        if depth <= 0 or depth > self.max_swap_depth:
            raise SwapBeyondMaxDepth(
                f'swap{depth} invalid, max_swap_depth: {self.max_swap_depth}'
            )
        if depth > len(self.stack) + 1:
            raise StackTooShallow(
                f'Attempting swap{depth}, stack depth: {len(self.stack)}'
            )
        ni = -depth - 1
        self.stack[ni], self.stack[-1] = self.stack[-1], self.stack[ni]

    def dup(self, depth: int):
        if depth <= 0 or depth > self.max_swap_depth:
            raise DupBeyondMaxDepth(
                f'dup{depth} invalid, max_dup_depth: {self.max_dup_depth}'
            )
        if depth > len(self.stack):
            raise StackTooShallow(
                f'Attempting dup{depth}, stack depth: {len(self.stack)}'
            )
        self.push(self.stack[-depth])

    def store(self, i: int):
        value = self.pop()
        self.locals[i] = value

    def load(self, i: int):
        if (local := self.locals.get(i)) is None:
            raise MissingLocal(f'No local[{i}]')
        self.push(local)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolicVM):
            return False
        return self.stack == other.stack and self.locals == other.locals
