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

class Error:
    def __init__(self, fname: str, errtype: str, info: str, location: tuple[int, int]) -> None:
        self.fname = fname
        self.errtype = errtype
        self.info = info
        self.location = location

    def __str__(self) -> str:
        return f"File <{self.fname}> at line {self.location[0]} and column {self.location[1]},\n{self.errtype}: {self.info}"

class IllegalCharErr(Error):
    def __init__(self, fname: str, char: str, location: tuple[int, int]) -> None:
        super().__init__(fname, "IllegalCharErr", f"illegal charecter '{char}'", location)

class UnexpectedToken(Error):
    def __init__(self, fname: str, expected_token, got_token, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnexpectedToken", f"expected token {expected_token}, got {got_token}", location)

class NoPrefixFunc(Error):
    def __init__(self, fname: str, token, location: tuple[int, int]) -> None:
        super().__init__(fname, "NoPrefixFunc", f"no prefix function for parsing {token.string} found", location)

class TypeMismatch(Error):
    def __init__(self, fname: str, operator, left_type, right_type, location: tuple[int, int]) -> None:
        super().__init__(fname, "TypeMismatch", f"Type mismatched in expression with operator: {operator} between {left_type} and {right_type}", location)

class UnknownOperator(Error):
    def __init__(self, fname: str, operator, left_type, right_type, location: tuple[int, int]) -> None:
        if left_type is not None:
            super().__init__(fname, "UnknownOperator", f"unknown operator: {operator} between {left_type} and {right_type}", location)
        else:
            super().__init__(fname, "UnknownOperator", f"unknown operator: {operator} for {right_type}", location)

class UnknownIdentifier(Error):
    def __init__(self, fname: str, name: str, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnknownIdentifier", f"unknown identifier '{name}'", location)

class NotAFunction(Error):
    def __init__(self, fname: str, obj, location: tuple[int, int]) -> None:
        super().__init__(fname, "NotAFunction", f"{obj.type()} is not a function", location)

class UnexpectedEOF(Error):
    def __init__(self, fname: str, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnexpectedEOF", "sudden unexpected EOF token encountered", location)

class ArgumentError(Error):
    def __init__(self, fname: str, expected, got, func, location: tuple[int, int]) -> None:
        super().__init__(fname, "ArgumentError", f"wrong number of arguments, expected {expected} but got {got} for function {func}", location)

class UnsupportedType(Error):
    def __init__(self, fname: str, got, func, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnsupportedType", f"argument of type {got} not supported for function {func}", location)

class UnsupportedIndexAccessType(Error):
    def __init__(self, fname: str, type, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnsupportedIndexAccessType", f"{type} not supported for index access expressions", location)

class UnsupportedIndexType(Error):
    def __init__(self, fname: str, got, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnsupportedIndexType", f"index of type {got} is not supported for array", location)

class UnsupporteKeyType(Error):
    def __init__(self, fname: str, type, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnsupportedKeyType", f"unsupported type {type} as key", location)

class UnknownNode(Error):
    def __init__(self, fname: str, location: tuple[int, int]) -> None:
        super().__init__(fname, "UnknownNode", "unknown ast node encountered", location)
