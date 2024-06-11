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

from typing import TYPE_CHECKING, Callable

from .. import astt
from .. import error

if TYPE_CHECKING:
    from .enviroment import Enviroment

OBJ_NUM = "OBJ_NUM"
OBJ_STRING = "OBJ_STRING"
OBJ_BOOLEAN = "OBJ_BOOLEAN"
OBJ_NULL = "OBJ_NULL"
OBJ_RETURN_VALUE = "OBJ_RETURN_VALUE"
OBJ_FUNCTION = "OBJ_FUNCTION"
OBJ_ARRAY = "OBJ_ARRAY"
OBJ_HASH = "OBJ_HASH"
OBJ_BUILTIN = "OBJ_BUILTIN"
OBJ_ERROR = "OBJ_ERROR"

class Object:
    def type(self) -> str:
        return str()
    def inspect(self) -> str:
        return str()

class HashKey:
    def __init__(self, obj_type: str, value: float | str) -> None:
        self.obj_type = obj_type
        self.value = value
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, HashKey):
            return False
        return value.value == self.value
    def __ne__(self, value: object) -> bool:
        if not isinstance(value, HashKey):
            return True
        return not value.value == self.value
    def __hash__(self) -> int:
        return hash(f"{self.obj_type}: {self.value}")
    def __repr__(self) -> str:
        return f"{self.value}"

class Hashable:
    def hash_key(self) -> HashKey:
        return HashKey("", int())

class HashPair:
    def __init__(self, key: Object, value: Object) -> None:
        self.key = key
        self.value = value
    def __repr__(self) -> str:
        return f"{self.value}"

class Number(Hashable, Object):
    def __init__(self, value: float) -> None:
        self.value = value
    def type(self) -> str:
        return OBJ_NUM
    def inspect(self) -> str:
        return str(self.value)
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), self.value)
    def __repr__(self) -> str:
        return self.inspect()

class String(Hashable, Object):
    def __init__(self, value: str) -> None:
        self.value = value
    def type(self) -> str:
        return OBJ_STRING
    def inspect(self) -> str:
        return "\"" + self.value + "\""
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), hash(self.value))
    def __repr__(self) -> str:
        return self.inspect()

class Boolean(Hashable, Object):
    def __init__(self, value: bool) -> None:
        self.value = value
    def type(self) -> str:
        return OBJ_BOOLEAN
    def inspect(self) -> str:
        return str(self.value).lower()
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), 1 if self.value else 0)
    def __repr__(self) -> str:
        return self.inspect()

class ReturnValue(Object):
    def __init__(self, value: Object) -> None:
        self.value = value
    def type(self) -> str:
        return OBJ_RETURN_VALUE
    def inspect(self) -> str:
        return self.value.inspect()

class Function(Object):
    def __init__(self, parametres: list[astt.Identifier], body: astt.BlockStatement, env: "Enviroment") -> None:
        self.parametres = parametres
        self.body = body
        self.env = env
    def type(self) -> str:
        return OBJ_FUNCTION
    def inspect(self) -> str:
        return f"fn({', '.join([repr(parametre) for parametre in self.parametres])}) {repr(self.body)}"

class Array(Object):
    def __init__(self, elements: list[Object]) -> None:
        self.elements = elements
    def type(self) -> str:
        return OBJ_ARRAY
    def inspect(self) -> str:
        return f"[{', '.join([element.inspect() for element in self.elements])}]"

class Hash(Object):
    def __init__(self, pairs: dict[HashKey, HashPair]) -> None:
        self.pairs = pairs
    def type(self) -> str:
        return OBJ_HASH
    def inspect(self) -> str:
        return f"{{{str([hashpair.key.inspect() + ': ' + hashpair.value.inspect() for hashpair in self.pairs.values()])[1:-1]}}}".replace("'", "")
    def __repr__(self) -> str:
        return self.inspect()

class Builtin(Object):
    def __init__(self, func: Callable) -> None:
        self.func = func
    def type(self) -> str:
        return OBJ_BUILTIN
    def inspect(self) -> str:
        return "Builtin Function"

class Null(Object):
    def type(self) -> str:
        return OBJ_NULL
    def inspect(self) -> str:
        return "null"
    def __repr__(self) -> str:
        return self.inspect()

class Error(Object):
    def __init__(self, error: str | error.Error) -> None:
        self.error = error
    def type(self) -> str:
        return OBJ_ERROR
    def inspect(self) -> str:
        return f"ERROR: {str(self.error)}"

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()
