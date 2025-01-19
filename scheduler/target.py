from typing import Generator, TypeAlias
from attrs import define, field


@define
class DataLayout:
    stack: list[str]
    locals: list[tuple[str, int]] = field()

    def validate(self):
        slots: dict[int, str] = dict()
        for name, slot in self.locals:
            if (existing_name := slots.get(slot)) is not None:
                raise ValueError(
                    f'Local {name!r} conflicts with {existing_name!r} for slot {slot}')
            slots[slot] = name


@define
class FuncDef:
    inp: DataLayout
    out: DataLayout
    deps: set[str]
    affects: set[str]


@define
class ExternalDef:
    name: str
    fn_def: FuncDef


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
    defs: list[ExternalDef]
    sub_groups: list[list[Substitution]]
    main_def: FuncDef
    statements: list[Statement]

    def validate(self):
        for d in self.get_defs():
            d.inp.validate()
            d.out.validate()

        unique_names: set[str] = set()
        for d in self.defs:
            if d.name in unique_names:
                raise ValueError(f'Duplicate function with name {d.name!r}')
            unique_names.add(d.name)

        return self

    def get_defs(self) -> Generator[FuncDef, None, None]:
        for d in self.defs:
            yield d.fn_def
        yield self.main_def
