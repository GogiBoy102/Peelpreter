########################################################################################
#    Peelpreter is a interpreter designed to interpret the language, Monkey.
#    Copyright (C) 2024 Jeebak Samajdwar
#
#    This file is part of Peelpreter
#
#    Peelpreter is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    Peelpreter is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
########################################################################################

from __future__ import annotations
from .. import error
from .. import objectt as obj


def arg_error(fname, expected, got, func):
    return obj.Error(error.ArgumentError(fname, expected, got, func, (-1, -1)))

def m_len(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return obj.Error(error.ArgumentError(fname, 1, len(args), "len", (-1, -1)))
    if type(args[0]) == obj.String:
        return obj.Number(len(args[0].value))
    elif type(args[0]) == obj.Array:
        return obj.Number(len(args[0].elements))
    else:
        return obj.Error(error.UnsupportedType(fname, args[0], "len", (-1, -1)))


def m_type(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return obj.Error(error.ArgumentError(fname, 1, len(args), "type", (-1, -1)))
    return obj.String(args[0].type())


def m_puts(_: str, args: list[obj.Object]) -> obj.Object:
    for arg in args:
        if type(arg) == obj.String:
            print(arg.inspect()[1:-1], end=" ")
        else:
            print(arg.inspect(), end=" ")
    print()

    return obj.NULL


def m_push(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 2:
        return obj.Error(error.ArgumentError(fname, 2, len(args), "push", (-1, -1)))
    if args[0].type() != obj.OBJ_ARRAY:
        return obj.Error(error.UnsupportedType(fname, args[0], "push", (-1, -1)))
    assert isinstance(args[0], obj.Array)
    arr = args[0].elements
    arr.append(args[1])

    return obj.NULL


def m_tail(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return arg_error(fname, 1, len(args), "tail")
    if args[0].type == obj.OBJ_ARRAY:
        assert isinstance(args[0], obj.Array)
        sequence = args[0].elements
        _, *tail = sequence
        return obj.Array(tail)
    elif args[0].type() == obj.OBJ_STRING:
        assert isinstance(args[0], obj.String)
        string = args[0].value
        tail = string[1:]
        return obj.String(tail)
    else:
        return obj.Error(error.UnsupportedType(fname, args[0], "tail", (-1, -1)))


def m_head(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return arg_error(fname, 1, len(args), "head")
    if args[0].type() == obj.OBJ_ARRAY:
        assert isinstance(args[0], obj.Array)
        arr = args[0].elements
        head, *_ = arr
        return obj.Array([head])
    elif args[0].type() == obj.OBJ_STRING:
        assert isinstance(args[0], obj.String)
        string = args[0].value
        head = string[0:-1]
        return obj.String(head)
    else:
        return obj.Error(error.UnsupportedType(fname, args[0], "head", (-1, -1)))


def m_first(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return arg_error(fname, 1, len(args), "first")
    if args[0].type() == obj.OBJ_ARRAY:
        assert isinstance(args[0], obj.Array)
        arr = args[0].elements
        start = arr[0]
        return start
    elif args[0].type() == obj.OBJ_STRING:
        assert isinstance(args[0], obj.String)
        string = args[0].value
        start = string[0]
        return obj.String(start)
    else:
        return obj.Error(error.UnsupportedType(fname, args[0], "first", (-1, -1)))


def m_last(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return arg_error(fname, 1, len(args), "last")
    if args[0].type() == obj.OBJ_ARRAY:
        assert isinstance(args[0], obj.Array)
        arr = args[0].elements
        end = arr[-1]
        return end
    elif args[0].type() == obj.OBJ_STRING:
        assert isinstance(args[0], obj.String)
        arr = args[0].value
        end = arr[-1]
        return obj.String(end)
    else:
        return obj.Error(error.UnsupportedType(fname, args[0], "last", (-1, -1)))


def m_insert(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 3:
        return arg_error(fname, 1, len(args), "insert")
    if args[0].type() != obj.OBJ_ARRAY:
       return obj.Error(error.UnsupportedType(fname, args[0], "insert", (-1, -1)))
    elif args[1].type() != obj.OBJ_NUM:
        return obj.Error(error.UnsupportedType(fname, args[0], "insert", (-1, -1)))

    assert isinstance(args[0], obj.Array)
    assert isinstance(args[1], obj.Number)
    arr = args[0].elements.copy()
    if len(arr) < args[1].value:
        arr = arr + [obj.NULL] * (int(args[1].value) - len(arr))
    arr.insert(int(args[1].value), args[2])

    return obj.Array(arr)


def m_change(fname: str, args: list[obj.Object]) -> obj.Object:
    if len(args) != 3:
        return arg_error(fname, 1, len(args), "change")
    elif args[0].type() != obj.OBJ_ARRAY:
       return obj.Error(error.UnsupportedType(fname, args[0], "change", (-1, -1)))
    elif args[1].type() != obj.OBJ_NUM:
        return obj.Error(error.UnsupportedType(fname, args[0], "change", (-1, -1)))
    
    assert isinstance(args[0], obj.Array)
    assert isinstance(args[1], obj.Number)
    arr = args[0].elements.copy()
    if args[1].value >= len(arr):
        return obj.Error("Too high")
    arr[int(args[1].value)] = args[2]

    return obj.Array(arr)


builtins: dict[str, obj.Builtin] = {
    "len": obj.Builtin(m_len),
    "type": obj.Builtin(m_type),
    "puts": obj.Builtin(m_puts),
    "push": obj.Builtin(m_push),
    "tail": obj.Builtin(m_tail),
    "head": obj.Builtin(m_head),
    "first": obj.Builtin(m_first),
    "last": obj.Builtin(m_last),
    "change": obj.Builtin(m_change),
    "insert": obj.Builtin(m_insert),
}
