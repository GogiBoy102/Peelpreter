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

from ..token_type.token_type import (
    TT_ASSIGN as TT_ASSIGN,
    TT_ASTERISK as TT_ASTERISK,
    TT_BANG as TT_BANG,
    TT_COLON as TT_COLON,
    TT_COMMA as TT_COMMA,
    TT_ELSE as TT_ELSE,
    TT_EOF as TT_EOF,
    TT_EQ as TT_EQ,
    TT_ERR as TT_ERR,
    TT_FALSE as TT_FALSE,
    TT_FUNC as TT_FUNC,
    TT_GT as TT_GT,
    TT_IDEN as TT_IDEN,
    TT_IF as TT_IF,
    TT_LBRACE as TT_LBRACE,
    TT_LBRACKET as TT_LBRACKET,
    TT_LET as TT_LET,
    TT_LPAREN as TT_LPAREN,
    TT_LT as TT_LT,
    TT_MINUS as TT_MINUS,
    TT_NTEQ as TT_NTEQ,
    TT_NULL as TT_NULL,
    TT_NUM as TT_NUM,
    TT_PLUS as TT_PLUS,
    TT_RBRACE as TT_RBRACE,
    TT_RBRACKET as TT_RBRACKET,
    TT_RETURN as TT_RETURN,
    TT_RPAREN as TT_RPAREN,
    TT_SEMICOLON as TT_SEMICOLON,
    TT_SLASH as TT_SLASH,
    TT_STRING as TT_STRING,
    TT_TRUE as TT_TRUE,
    keywords as keywords,
    Token as Token,
)
