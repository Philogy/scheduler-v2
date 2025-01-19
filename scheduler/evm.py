EVM_EXT = '''
// Stop and Arithmetic Operations
ext stop [
    deps(control_flow)
    in: []
    out: []
]

ext add [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext mul [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext sub [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext div [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext sdiv [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext mod [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext smod [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext addmod [
    deps(control_flow)
    in: [a, b, n]
    out: [c]
]

ext mulmod [
    deps(control_flow)
    in: [a, b, n]
    out: [c]
]

ext exp [
    deps(control_flow)
    in: [base, exponent]
    out: [result]
]

// Comparison & Bitwise Logic Operations
ext lt [
    deps(control_flow)
    in: [a, b]
    out: [result]
]

ext gt [
    deps(control_flow)
    in: [a, b]
    out: [result]
]

ext slt [
    deps(control_flow)
    in: [a, b]
    out: [result]
]

ext sgt [
    deps(control_flow)
    in: [a, b]
    out: [result]
]

ext eq [
    deps(control_flow)
    in: [a, b]
    out: [result]
]

ext iszero [
    deps(control_flow)
    in: [a]
    out: [result]
]

ext and [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext or [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext xor [
    deps(control_flow)
    in: [a, b]
    out: [c]
]

ext not [
    deps(control_flow)
    in: [a]
    out: [b]
]

ext byte [
    deps(control_flow)
    in: [i, x]
    out: [y]
]

ext shl [
    deps(control_flow)
    in: [shift, value]
    out: [result]
]

ext shr [
    deps(control_flow)
    in: [shift, value]
    out: [result]
]

ext sar [
    deps(control_flow)
    in: [shift, value]
    out: [result]
]

// Commutative arithmetic operations
sub [
    add(0, 1)
    add(1, 0)
]

sub [
    mul(0, 1)
    mul(1, 0)
]

sub [
    addmod(0, 1, 2)
    addmod(1, 0, 2)
]

sub [
    mulmod(0, 1, 2)
    mulmod(1, 0, 2)
]

// Commutative bitwise operations
sub [
    and(0, 1)
    and(1, 0)
]

sub [
    or(0, 1)
    or(1, 0)
]

sub [
    xor(0, 1)
    xor(1, 0)
]

// Equality is commutative
sub [
    eq(0, 1)
    eq(1, 0)
]

// Comparison symmetries
sub [
    lt(0, 1)
    gt(1, 0)
]

sub [
    sgt(0, 1)
    slt(1, 0)
]

// SHA3
ext sha3 [
    deps(control_flow, memory)
    in: [offset, size]
    out: [hash]
]

// Environmental Information
ext address [
    deps(control_flow)
    in: []
    out: [addr]
]

ext balance [
    deps(control_flow, balance)
    in: [addr]
    out: [bal]
]

ext origin [
    deps(control_flow)
    in: []
    out: [addr]
]

ext caller [
    deps(control_flow)
    in: []
    out: [addr]
]

ext callvalue [
    deps(control_flow)
    in: []
    out: [val]
]

ext calldataload [
    deps(control_flow)
    in: [i]
    out: [data]
]

ext calldatasize [
    deps(control_flow)
    in: []
    out: [size]
]

ext calldatacopy [
    deps(control_flow)
    affects(memory)
    in: [destOffset, offset, size]
    out: []
]

ext codesize [
    deps(control_flow, code)
    in: []
    out: [size]
]

ext codecopy [
    deps(control_flow)
    affects(memory)
    in: [destOffset, offset, size]
    out: []
]

ext gasprice [
    deps(control_flow)
    in: []
    out: [price]
]

ext extcodesize [
    deps(control_flow, extcode)
    in: [addr]
    out: [size]
]

ext extcodecopy [
    deps(control_flow, extcode)
    affects(memory)
    in: [addr, destOffset, offset, size]
    out: []
]

ext returndatasize [
    deps(control_flow, returndata)
    in: []
    out: [size]
]

ext returndatacopy [
    deps(control_flow, returndata)
    affects(memory)
    in: [destOffset, offset, size]
    out: []
]

ext extcodehash [
    deps(control_flow, code)
    in: [addr]
    out: [hash]
]

// Block Information
ext blockhash [
    deps(control_flow)
    in: [number]
    out: [hash]
]

ext coinbase [
    deps(control_flow)
    in: []
    out: [addr]
]

ext timestamp [
    deps(control_flow)
    in: []
    out: [time]
]

ext number [
    deps(control_flow)
    in: []
    out: [num]
]

ext difficulty [
    deps(control_flow)
    in: []
    out: [diff]
]

ext gaslimit [
    deps(control_flow)
    in: []
    out: [limit]
]

// Stack, Memory, Storage and Flow Operations
ext pop [
    deps(control_flow)
    in: [a]
    out: []
]

ext mload [
    deps(control_flow, memory)
    in: [offset]
    out: [value]
]

ext mstore [
    deps(control_flow)
    affects(memory)
    in: [offset, value]
    out: []
]

ext mcopy [
    deps(control_flow)
    affects(memory)
    in: [dest, src, len]
    out: []
]

ext mstore8 [
    deps(control_flow)
    affects(memory)
    in: [offset, value]
    out: []
]

ext sload [
    deps(control_flow, storage)
    in: [key]
    out: [value]
]

ext sstore [
    deps(control_flow)
    affects(storage)
    in: [key, value]
    out: []
]

ext jump [
    affects(control_flow)
    in: [dest]
    out: []
]

ext jumpi [
    affects(control_flow)
    in: [dest, condition]
    out: []
]

ext gas [
    deps(control_flow)
    in: []
    out: [remaining]
]

ext jumpdest [
    affects(control_flow)
    in: []
    out: []
]

// Logging Operations
ext log0 [
    deps(control_flow, memory)
    affects(logs)
    in: [offset, size]
    out: []
]

ext log1 [
    deps(control_flow, memory)
    affects(logs)
    in: [offset, size, topic1]
    out: []
]

ext log2 [
    deps(control_flow, memory)
    affects(logs)
    in: [offset, size, topic1, topic2]
    out: []
]

ext log3 [
    deps(control_flow, memory)
    affects(logs)
    in: [offset, size, topic1, topic2, topic3]
    out: []
]

ext log4 [
    deps(control_flow, memory)
    affects(logs)
    in: [offset, size, topic1, topic2, topic3, topic4]
    out: []
]

// System Operations
ext create [
    deps(control_flow)
    affects(memory, returndata, logs, balance, storage, extcode)
    in: [value, offset, size]
    out: [addr]
]

ext create2 [
    deps(control_flow)
    affects(memory, returndata, logs, balance, storage, extcode)
    in: [value, offset, size, salt]
    out: [addr]
]

ext call [
    deps(control_flow)
    affects(memory, returndata, logs, balance, storage, extcode)
    in: [gas, addr, value, argsOffset, argsSize, retOffset, retSize]
    out: [success]
]

ext callcode [
    deps(control_flow)
    affects(memory, returndata, logs, balance, storage, extcode)
    in: [gas, addr, value, argsOffset, argsSize, retOffset, retSize]
    out: [success]
]

ext delegatecall [
    deps(control_flow)
    affects(memory, returndata, logs, balance, storage, extcode)
    in: [gas, addr, argsOffset, argsSize, retOffset, retSize]
    out: [success]
]

ext staticcall [
    deps(control_flow, storage, balance)
    affects(memory, returndata)
    in: [gas, addr, argsOffset, argsSize, retOffset, retSize]
    out: [success]
]

ext selfdestruct [
    affects(control_flow)
    in: [addr]
    out: []
]

ext revert [
    deps(memory)
    affects(control_flow)
    in: [offset, size]
    out: []
]

ext invalid [
    affects(control_flow)
    in: []
    out: []
]


ext return [
    deps(memory)
    affects(control_flow)
    in: [offset, size]
    out: []
]
'''
