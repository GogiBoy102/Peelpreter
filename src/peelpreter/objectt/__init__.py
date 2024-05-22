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

from .objectt import (
    OBJ_ARRAY as OBJ_ARRAY,
    OBJ_BOOLEAN as OBJ_BOOLEAN,
    OBJ_BUILTIN as OBJ_BUILTIN,
    OBJ_ERROR as OBJ_ERROR,
    OBJ_FUNCTION as OBJ_FUNCTION,
    OBJ_HASH as OBJ_HASH,
    OBJ_NULL as OBJ_NULL,
    OBJ_NUM as OBJ_NUM,
    OBJ_RETURN_VALUE as OBJ_RETURN_VALUE,
    OBJ_STRING as OBJ_STRING,
    Object as Object,
    HashKey as HashKey,
    Hashable as Hashable,
    HashPair as HashPair,
    Number as Number,
    String as String,
    Boolean as Boolean,
    ReturnValue as ReturnValue,
    Function as Function,
    Array as Array,
    Hash as Hash,
    Builtin as Builtin,
    Null as Null,
    Error as Error,
    TRUE as TRUE,
    FALSE as FALSE,
    NULL as NULL,
)
from .enviroment import Enviroment as Enviroment
