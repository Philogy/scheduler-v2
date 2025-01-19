from scheduler.parser import PARSER, EVMTransformer, Target
from scheduler.evm import EVM_EXT
from scheduler.graph import GraphBuilder


def main():
    tree = PARSER.parse(
        EVM_EXT + '\n' +
        '''
        main [
            in: [x, y]
            out: []
        ]

        b = sload(x)
        sstore(y, b)
        '''
    )

    print(tree.pretty())

    out = EVMTransformer().transform(tree)
    assert isinstance(out, Target)

    return GraphBuilder(out)


if __name__ == '__main__':
    g = main()
