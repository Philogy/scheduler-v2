from typing import Generator, TypeAlias
from attrs import define, field


@define
class DataLayout:
    stack: list[str]
    locals: list[tuple[str, int]] = field()

    def size(self) -> int:
        return len(self.stack) + len(self.locals)

    def validate(self):
        slots: dict[int, str] = dict()
        for name, slot in self.locals:
            if (existing_name := slots.get(slot)) is not None:
                raise ValueError(
                    f'Local {name!r} conflicts with {existing_name!r} for slot {slot}')
            slots[slot] = name

    def names(self) -> Generator[str, None, None]:
        yield from self.stack
        for local_name, _ in self.locals:
            yield local_name


@define
class FuncSpec:
    inp: DataLayout
    out: DataLayout
    deps: set[str]
    affects: set[str]

    def validate(self):
        self.inp.validate()
        self.out.validate()

        overlap = self.deps & self.affects
        assert not overlap, f'Every dependecy must be unique in deps/affects, not unique: {overlap}'


@define
class NamedSpec:
    name: str
    spec: FuncSpec


@define
class Substitution:
    name: str
    params: list[int]


@define
class Call:
    name: str
    args: list['Expr']


Expr: TypeAlias = int | str | Call


@define
class SingleAssign:
    to: str
    expr: Expr


@define
class MultiAssign:
    to: list[str]
    call: Call


Statement: TypeAlias = Call | SingleAssign | MultiAssign


@define
class Target:
    defs: list[NamedSpec]
    sub_groups: list[list[Substitution]]
    main_def: FuncSpec
    body: list[Statement]

    def validate(self):
        for d in self.get_defs():
            d.validate()

        unique_names: set[str] = set()
        for d in self.defs:
            if d.name in unique_names:
                raise ValueError(f'Duplicate function with name {d.name!r}')
            unique_names.add(d.name)

        return self

    def get_defs(self) -> Generator[FuncSpec, None, None]:
        for d in self.defs:
            yield d.spec
        yield self.main_def
