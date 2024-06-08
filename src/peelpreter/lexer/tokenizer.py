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
from ..error import Error, IllegalCharErr, UnexpectedEOF
from .. import token_type as ttoken

def tokenize(source: str, fname: str = "stdin") -> list[ttoken.Token]:
    def advance(position: int) -> int:
        return position + 1 if position < len(source) -1 else -1
    def peek(position: int) -> str:
        return source[position + 1] if position + 1 != len(source) else ""
    def handle_num(position: int, current: str, tokens: list[ttoken.Token]) -> int:
        num = current
        index = position
        while num.isdigit():
            index += 1
            if not index < len(source):
                break
            num = source[index]
        if not num == ".":
            tokens.append(ttoken.Token(ttoken.TT_NUM, source[position:index], float(source[position:index]))) 
            return index - 1
        if peek(index).isdigit() and num == ".":
            index += 1
            num = source[index]
            while num.isdigit():
                index += 1
                if not index < len(source):
                    break
                num = source[index]
        tokens.append(ttoken.Token(ttoken.TT_NUM, source[position:index], float(source[position:index])))
        return index - 1

    def handle_str(position: int, current: str, tokens: list[ttoken.Token], line: int, column: int) -> int:
        start_pos = position
        position = advance(position)
        if position == -1:
            add_err(UnexpectedEOF(fname, (line, column)), current, tokens)
            return start_pos
        current = source[position]
        while current != "\"":
            old_pos = position
            position = advance(position)
            if position == -1:
                add_err(UnexpectedEOF(fname, (line, column)), current, tokens)
                return old_pos
            current = source[position]

        tokens.append(ttoken.Token(ttoken.TT_STRING, source[start_pos + 1:position], None))
        return position

    def handle_indentifier(position: int, current: str, tokens: list[ttoken.Token]) -> int:
        index = position
        char = current
        while char.isalpha() or char == "_":
            index += 1
            if not index < len(source):
                break
            char = source[index]
        if source[position:index] in ttoken.keywords:
            tokens.append(ttoken.Token(ttoken.keywords[source[position:index]], source[position:index], None))
            return index - 1
        tokens.append(ttoken.Token(ttoken.TT_IDEN, source[position:index], None))
        return index - 1

    def add_token(ttype: str, current: str, tokens: list[ttoken.Token]) -> None:
        tokens.append(ttoken.Token(ttype, current, None))
    def add_err(err: Error, current, tokens: list[ttoken.Token]) -> None:
        tokens.append(ttoken.Token(ttoken.TT_ERR, current, err))

    tokens: list[ttoken.Token] = []
    line = 0
    column = 0
    position = -1
    current = None

    while True:
        position = advance(position)
        if position == -1:
            break
        column += 1
        current = source[position]

        if current == "=":
            if peek(position) == "=" and peek(position) != "":
                position = advance(position)
                add_token(ttoken.TT_EQ, "==", tokens)
                continue
            add_token(ttoken.TT_ASSIGN, current, tokens)
        elif current == "+":
            add_token(ttoken.TT_PLUS, current, tokens)
        elif current == "-":
            add_token(ttoken.TT_MINUS, current, tokens)
        elif current == "/":
            add_token(ttoken.TT_SLASH, current, tokens)
        elif current == "*":
            add_token(ttoken.TT_ASTERISK, current, tokens)
        elif current == "!":
            if peek(position) == "=":
                position = advance(position)
                add_token(ttoken.TT_NTEQ, "!=", tokens)
                continue
            add_token(ttoken.TT_BANG, current, tokens)
        elif current == "<":
            add_token(ttoken.TT_LT, current, tokens)
        elif current == ">":
            add_token(ttoken.TT_GT, current, tokens)
        elif current == "(":
            add_token(ttoken.TT_LPAREN, current, tokens)
        elif current == ")":
            add_token(ttoken.TT_RPAREN, current, tokens)
        elif current == "{":
            add_token(ttoken.TT_LBRACE, current, tokens)
        elif current == "}":
            add_token(ttoken.TT_RBRACE, current, tokens)
        elif current == "[":
            add_token(ttoken.TT_LBRACKET, current, tokens)
        elif current == "]":
            add_token(ttoken.TT_RBRACKET, current, tokens)
        elif current == ",":
            add_token(ttoken.TT_COMMA, current, tokens)
        elif current == ":":
            add_token(ttoken.TT_COLON, current, tokens)
        elif current == " ":
            continue
        elif current == "\t":
            continue
        elif current == "\n":
            column = 1
            line += 1
        elif current == ";":
            add_token(ttoken.TT_SEMICOLON, current, tokens)
        elif current == "\"":
            position = handle_str(position, current, tokens, line, column)
        elif current.isalpha():
            position = handle_indentifier(position, current, tokens)
        elif current.isdigit():
            position = handle_num(position, current, tokens)
        else:
            add_err(IllegalCharErr(fname, current, (line, column)), current, tokens)
                    
    add_token(ttoken.TT_EOF, "", tokens)

    return tokens
