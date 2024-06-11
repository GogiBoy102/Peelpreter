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

from ..error import Error

TT_NUM = "TT_NUM"
TT_STRING = "TT_STRING"
TT_IDEN = "TT_IDEN"

TT_ASSIGN = "TT_ASSIGN"
TT_PLUS = "TT_PLUS"
TT_MINUS = "TT_MINUS"
TT_SLASH = "TT_SLASH"
TT_ASTERISK = "TT_ASTERISK"

TT_BANG = "TT_BANG"
TT_EQ = "TT_EQ"
TT_NTEQ = "TT_NTEQ"
TT_LT = "TT_LT"
TT_GT = "TT_GT"

TT_COMMA = "TT_COMMA"
TT_COLON = "TT_COLON"
TT_SEMICOLON = "TT_SEMICOLON"
TT_LBRACE = "TT_LBRACE"
TT_RBRACE = "TT_RBRACE"
TT_LPAREN = "TT_LPAREN"
TT_RPAREN = "TT_RPAREN"
TT_LBRACKET = "TT_LBRACKET"
TT_RBRACKET = "TT_RBRACKET"

TT_LET = "TT_LET"
TT_FUNC = "TT_FUNC"
TT_TRUE = "TT_TRUE"
TT_FALSE = "TT_FALSE"
TT_IF = "TT_IF"
TT_ELSE = "TT_ELSE"
TT_RETURN = "TT_RETURN"

TT_NULL = "TT_NULL"
TT_ERR = "TT_ERR"
TT_EOF = "TT_EOF"

keywords = {
    "fn": TT_FUNC,
    "let": TT_LET,
    "true": TT_TRUE,
    "false": TT_FALSE,
    "null": TT_NULL,
    "if": TT_IF,
    "else": TT_ELSE,
    "return": TT_RETURN
}

class Token:
    def __init__(self, ttype: str, string: str, value: Error | float | None) -> None:
        self.ttype = ttype
        self.string = string
        self.value = value
    def __repr__(self) -> str:
        if self.value is None and self.ttype != TT_IDEN:
            return f"{self.ttype}"
        elif self.ttype == TT_ERR:
            if isinstance(self.value, Error):
                return f"{self.ttype}: {self.value.errtype}"
        elif self.ttype == TT_IDEN:
            return f"{self.ttype}: {self.string}"
        return f"{self.ttype}: {self.string}"
