from typing import Optional, TypeAlias
from dataclasses import dataclass
from .target import *


@dataclass
class Const:
    value: int


class FunctionNode:
    calls: str
    preds: list['FunctionNode']
    succs: list['FunctionNode']
    inputs: list['ValueNode']
    outputs: list['ValueNode']

    def __init__(self, calls: str) -> None:
        self.calls = calls
        self.preds = []
        self.succs = []
        self.inputs = []
        self.outputs = []


Producer: TypeAlias = Const | FunctionNode


class ValueNode:
    name: Optional[str]
    producer: Producer
    consumers: list[FunctionNode]

    def __init__(self, name: Optional[str], producer: Producer) -> None:
        self.name = name
        self.producer = producer
        self.consumers = []


class GraphBuilder:
    target: Target

    def __init__(self, target: Target):
        self.target = target
