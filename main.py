from scheduler.parser import PARSER, EVMTransformer
from scheduler.evm import EVM_EXT


def main():
    tree = PARSER.parse(
        '''
        ext sstore [
            affects(storage)
            in: [slot, value]
            out: []
        ]

        ext sload [
            deps(storage)
            in: [slot]
            out: [value]
        ]

        ext sload [
            in: []
            out: []
        ]

        ext my_func [
            deps(storage, msize) affects(memory)
            in: [x] wow@3
            out: [y, z] wow@3
        ]

        sub [
            add(0, 1)
            add(1, 0)
        ]

        sub [
            addmod(0, 1, 2)
            addmod(1, 0, 2)
        ]

        main [
            in: [x]
            out: []
        ]

        a = add(nice, how(bob))
        x, y, z = glob(3, 4)
        '''
    )

    print(tree.pretty())

    out = EVMTransformer().transform(tree)

    print(out)
    # tree =

    # # print(tree.pretty())

    # print(PARSER.parse(EVM_EXT + '\nmain [in: [] out: []]').pretty())


if __name__ == '__main__':
    main()
