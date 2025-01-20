from scheduler.parser import parse_to_target
from scheduler.graph import Graph


def main():
    target = parse_to_target(
        '''
        main [
            in: [x, y]
            out: [z]
        ]

        sstore(y, sload(x))
        z = calldataload(4)
        '''
    )

    return Graph(target)


if __name__ == '__main__':
    g = main()
