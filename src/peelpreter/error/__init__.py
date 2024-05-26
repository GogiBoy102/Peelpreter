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

from .error import (
    Error as Error,
    IllegalCharErr as IllegalCharErr,
    UnexpectedToken as UnexpectedToken,
    NoPrefixFunc as NoPrefixFunc,
    UnknownOperator as UnknownOperator,
    UnknownIdentifier as UnknownIdentifier,
    NotAFunction as NotAFunction,
    UnexpectedEOF as UnexpectedEOF,
    ArgumentError as ArgumentError,
    UnsupportedType as UnsupportedType,
    UnsupportedIndexAccessType as UnsupportedIndexAccessType,
    UnsupportedIndexType as UnsupportedIndexType,
    UnsupporteKeyType as UnsupporteKeyType,
    UnknownNode as UnknownNode,
)
