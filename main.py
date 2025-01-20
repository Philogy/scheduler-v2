from scheduler.parser import parse_to_target
from scheduler.graph import Graph
from scheduler.state import State, Config


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

    g = Graph(target)
    s = State.from_graph(g, Config(16, 16))
    print(s)


if __name__ == '__main__':
    main()
