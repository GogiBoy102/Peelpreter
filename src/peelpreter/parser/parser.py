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
from typing import Callable

from .. import astt
from ..error import Error, NoPrefixFunc, UnexpectedEOF, UnexpectedToken
from .. import token_type as ttoken

LOWEST = 1
EQUALS = 2
LESSGREATER = 3
SUM = 4
PRODUCT = 5
PREFIX = 6
CALL = 7
INDEX = 8


def parse(tokens: list[ttoken.Token], fname="stdin") -> tuple[astt.Program, list[Error]]:
    def advance(index: int) -> int:
        return index + 1 if index + 1 != len(tokens) else index

    def peek(index: int) -> ttoken.Token:
        return (
            tokens[index + 1] if tokens[index].ttype != ttoken.TT_EOF else tokens[index]
        )

    def get_precedence(token: ttoken.Token, precedences: dict[str, int]) -> int:
        if precedences.get(token.ttype) is not None:
            return precedences[token.ttype]
        return LOWEST

    def parse_statement(token: ttoken.Token, index: int) -> tuple[astt.LetStatement | astt.ReassignmentStatement | astt.ReturnStatement | astt.ExpressionStatement | None, int]:
        if token.ttype == ttoken.TT_LET:
            return parse_let(token, index, errors)
        elif token.ttype == ttoken.TT_RETURN:
            return parse_return(token, index)
        else:
            return parse_statementexpr(token, index)

    def parse_let(token: ttoken.Token, index: int, errors: list[Error]) -> tuple[astt.LetStatement | astt.ReassignmentStatement | None, int]:
        index = advance(index)

        if peek(index).ttype == ttoken.TT_ASSIGN:
            statement, index = parse_assign(token, index, errors)
        else:
            statement, index = parse_reassign(token, index, errors)

        return statement, index

    def parse_assign(token: ttoken.Token, index: int, errors: list[Error]) -> tuple[astt.LetStatement | None, int]:
        statement = astt.LetStatement(token, astt.Identifier(token), astt.Expression(""))
        
        token = tokens[index]
        statement.name = astt.Identifier(token)
        
        if peek(index).ttype != ttoken.TT_ASSIGN:
            errors.append(UnexpectedToken(fname, "=", peek(index).string, (-1, -1)))
            return None, index

        index = advance(advance(index))
        token = tokens[index]
        value, index = parse_expression(LOWEST, token, index)

        if value is not None:
            statement.value = value
        
        if peek(index).ttype == ttoken.TT_SEMICOLON:
            index = advance(index)
            token = tokens[index]

        return statement, index

    def parse_reassign(token: ttoken.Token, index: int, errors: list[Error]) -> tuple[astt.ReassignmentStatement | None, int]:
        statement = astt.ReassignmentStatement(token, astt.IndexExpression(token, astt.ArrayLiteral(token, [astt.Expression("")]), astt.Expression("")), astt.Expression(""))
        
        token = tokens[index]
        index_expr, index = parse_expression(LOWEST, token, index)

        if index_expr is not None:
            assert isinstance(index_expr, astt.IndexExpression)
            statement.index_expr = index_expr
        
        if peek(index).ttype != ttoken.TT_ASSIGN:
            errors.append(UnexpectedToken(fname, "=", peek(index).string, (-1, -1)))
            return None, index

        index = advance(advance(index))
        token = tokens[index]
        value, index = parse_expression(LOWEST, token, index)

        if value is not None:
            statement.value = value
        
        if peek(index).ttype == ttoken.TT_SEMICOLON:
            index = advance(index)
            token = tokens[index]

        return statement, index

    def parse_return(token: ttoken.Token, index: int) -> tuple[astt.ReturnStatement, int]:
        statment = astt.ReturnStatement(token, astt.Expression(""))

        index = advance(index)
        token = tokens[index]

        value, index = parse_expression(LOWEST, token, index)
        if value is not None:
            statment.valuexp = value

        if peek(index).ttype == ttoken.TT_SEMICOLON:
            index = advance(index)
            token = tokens[index]

        return statment, index

    def parse_block(token: ttoken.Token, index: int) -> tuple[astt.BlockStatement, int]:
        block = astt.BlockStatement(token, [])

        index = advance(index)
        token = tokens[index]

        while token.ttype != ttoken.TT_RBRACE and token.ttype != ttoken.TT_EOF:
            statment, index = parse_statement(token, index)
            if statment is not None:
                block.statements.append(statment)
            index = advance(index)
            token = tokens[index]

        return block, index

    def parse_statementexpr(token: ttoken.Token, index: int) -> tuple[astt.ExpressionStatement, int]:
        statment = astt.ExpressionStatement(token, astt.Expression(""))
        expression, index = parse_expression(LOWEST, token, index)
        if expression is not None:
            statment.expression = expression

        if peek(index).ttype == ttoken.TT_SEMICOLON:
            index = advance(index)
            token = tokens[index]

        return statment, index

    def parse_expression(
        precedence: int, token: ttoken.Token, index: int
    ) -> tuple[astt.Expression | None, int]:
        parse_prefixfns: dict[str, Callable] = {
            ttoken.TT_IDEN: parse_identifier,
            ttoken.TT_NUM: parse_num,
            ttoken.TT_STRING: parse_str,
            ttoken.TT_BANG: parse_prefixexpr,
            ttoken.TT_MINUS: parse_prefixexpr,
            ttoken.TT_TRUE: parse_boolean,
            ttoken.TT_FALSE: parse_boolean,
            ttoken.TT_NULL: parse_null,
            ttoken.TT_LPAREN: parse_groupedexpr,
            ttoken.TT_IF: parse_ifexpr,
            ttoken.TT_FUNC: parse_funcliteral,
            ttoken.TT_LBRACKET: parse_array_literal,
            ttoken.TT_LBRACE: parse_hash_literal,
        }
        precedences = {
            ttoken.TT_EQ: EQUALS,
            ttoken.TT_NTEQ: EQUALS,
            ttoken.TT_LT: LESSGREATER,
            ttoken.TT_GT: LESSGREATER,
            ttoken.TT_PLUS: SUM,
            ttoken.TT_MINUS: SUM,
            ttoken.TT_SLASH: PRODUCT,
            ttoken.TT_ASTERISK: PRODUCT,
            ttoken.TT_LPAREN: CALL,
            ttoken.TT_LBRACKET: INDEX,
        }

        parse_infixfns: dict[str, Callable] = {
            ttoken.TT_PLUS: parse_infixexpr,
            ttoken.TT_MINUS: parse_infixexpr,
            ttoken.TT_SLASH: parse_infixexpr,
            ttoken.TT_ASTERISK: parse_infixexpr,
            ttoken.TT_EQ: parse_infixexpr,
            ttoken.TT_NTEQ: parse_infixexpr,
            ttoken.TT_LT: parse_infixexpr,
            ttoken.TT_GT: parse_infixexpr,
            ttoken.TT_LPAREN: parse_callexpr,
            ttoken.TT_LBRACKET: parse_indexexpr,
        }

        prefix_func = parse_prefixfns.get(token.ttype)
        if prefix_func is None:
            errors.append(NoPrefixFunc(fname, token, (-1, -1)))
            return None, index
        left_expr, index = prefix_func(token, index)
        token = tokens[index]

        if left_expr is None:
            return None, index

        while peek(index) != ttoken.TT_SEMICOLON and precedence < get_precedence(
            tokens[advance(index)], precedences
        ):
            infix_func = parse_infixfns.get(peek(index).ttype)
            if infix_func is None:
                return left_expr

            index = advance(index)
            token = tokens[index]
            left_expr, index = infix_func(precedences, left_expr, token, index)

        return left_expr, index

    def parse_prefixexpr(token: ttoken.Token, index: int) -> tuple[astt.PrefixExpression | None, int]:
        expression = astt.PrefixExpression(token, astt.Expression(""))
        index = advance(index)
        token = tokens[index]
        if token.ttype == ttoken.TT_EOF:
            errors.append(UnexpectedEOF(fname, (-1, -1)))
            return None, index
        rightexpr, index = parse_expression(PREFIX, token, index)
        if rightexpr is None:
            return None, index

        expression.rightexpr = rightexpr

        return expression, index

    def parse_infixexpr(precedences: dict[str, int], leftexpr: astt.PrefixExpression, token: ttoken.Token, index: int) -> tuple[astt.InfixExpression | None, int]:
        expression = astt.InfixExpression(token, leftexpr, astt.Expression(""))
        precedence = get_precedence(token, precedences)

        index = advance(index)
        token = tokens[index]
        if token.ttype == ttoken.TT_EOF:
            errors.append(UnexpectedEOF(fname, (-1, -1)))
            return None, index
        rightexpr, index = parse_expression(precedence, token, index)
        if rightexpr is not None:
            expression.rightexpr = rightexpr

        return expression, index

    def parse_groupedexpr(token: ttoken.Token, index: int) -> tuple[astt.Expression | None, int]:
        index = advance(index)
        token = tokens[index]

        expression, index = parse_expression(LOWEST, token, index)

        if peek(index).ttype != ttoken.TT_RPAREN:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_RPAREN, peek(index).ttype, (-1, -1))
            )
            return None, index

        index = advance(index)

        return expression, index

    def parse_ifexpr(token: ttoken.Token, index: int) -> tuple[astt.IfExpression | None, int]:
        expression = astt.IfExpression(
            token, astt.Expression(""), astt.BlockStatement(token, [astt.Statement("")]), astt.BlockStatement(token, [astt.Statement("")])
        )

        if peek(index).ttype != ttoken.TT_LPAREN:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_LPAREN, peek(index).ttype, (-1, -1))
            )
            return None, index

        index = advance(advance(index))
        token = tokens[index]
        condition, index = parse_expression(LOWEST, token, index)
        if condition is not None:
            expression.condition = condition
        if peek(index).ttype != ttoken.TT_RPAREN:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_RPAREN, peek(index).ttype, (-1, -1))
            )
            return None, index
        index = advance(index)
        token = tokens[index]
        if peek(index).ttype != ttoken.TT_LBRACE:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_LBRACE, peek(index).ttype, (-1, -1))
            )
            return None, index
        index = advance(index)
        token = tokens[index]
        consequence, index = parse_block(token, index)
        if condition is not None:
            expression.consequence = consequence
        if peek(index).ttype == ttoken.TT_ELSE:
            index = advance(index)
            token = tokens[index]
            if peek(index).ttype != ttoken.TT_LBRACE:
                errors.append(
                    UnexpectedToken(
                        fname, ttoken.TT_LBRACE, peek(index).ttype, (-1, -1)
                    )
                )
            index = advance(index)
            token = tokens[index]
            alternative, index = parse_block(token, index)
            if alternative is not None:
                expression.alternative = alternative

        return expression, index

    def parse_funcliteral(token: ttoken.Token, index: int) -> tuple[astt.FunctionLiteral | None, int]:
        expression = astt.FunctionLiteral(token, [], astt.BlockStatement(token, [astt.Statement("")]))

        if peek(index).ttype != ttoken.TT_LPAREN:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_LPAREN, peek(index).ttype, (-1, -1))
            )
            return None, index
        index = advance(index)
        token = tokens[index]
        identifiers, index = parse_parametres(index)
        if identifiers is not None:
            expression.parameters = identifiers

        if peek(index).ttype != ttoken.TT_LBRACE:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_LBRACE, peek(index).ttype, (-1, -1))
            )
            return None, index

        index = advance(index)
        token = tokens[index]

        body, index = parse_block(token, index)
        if body is not None:
            expression.body = body

        return expression, index

    def parse_parametres(index: int) -> tuple[list[astt.Identifier] | None, int]:
        identifiers = []

        if peek(index).ttype == ttoken.TT_RPAREN:
            index = advance(index)
            token = tokens[index]
            return identifiers, index

        index = advance(index)
        token = tokens[index]
        identifier = astt.Identifier(token)
        identifiers.append(identifier)

        while peek(index).ttype == ttoken.TT_COMMA:
            index = advance(advance(index))
            token = tokens[index]
            identifier = astt.Identifier(token)
            identifiers.append(identifier)

        if peek(index).ttype != ttoken.TT_RPAREN:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_RPAREN, peek(index).ttype, (-1, -1))
            )
            return None, index

        index = advance(index)
        token = tokens[index]

        return identifiers, index

    def parse_callexpr(precedences: dict[str, int], function: astt.FunctionLiteral, token: ttoken.Token, index: int) -> tuple[astt.CallExpression, int]:
        expression = astt.CallExpression(token, function, [])
        arguments, index = parse_exprlist(index, ttoken.TT_RPAREN)

        if arguments is not None:
            expression.arguments = arguments

        return expression, index

    def parse_hash_literal(token: ttoken.Token, index: int) -> tuple[astt.HashLiteral | None, int]:
        hash_literal = astt.HashLiteral(token, dict())

        while peek(index).ttype != ttoken.TT_RBRACE:
            index = advance(index)
            token = tokens[index]

            key, index = parse_expression(LOWEST, token, index)
            if peek(index).ttype != ttoken.TT_COLON:
                errors.append(
                    UnexpectedToken(fname, ttoken.TT_COLON, peek(index).ttype, (-1, -1))
                )
                return None, index
            index = advance(advance(index))
            if peek(index).ttype == ttoken.TT_EOF:
                errors.append(UnexpectedEOF(fname, (-1, -1)))
                return None, index
            token = tokens[index]
            value, index = parse_expression(LOWEST, token, index)
            if key is not None and value is not None:
                hash_literal.pairs[key] = value
            if (
                peek(index).ttype != ttoken.TT_RBRACE
                and peek(index).ttype != ttoken.TT_COMMA
            ):
                errors.append(
                    UnexpectedToken(fname, ttoken.TT_COMMA, peek(index).ttype, (-1, -1))
                )
                return None, index
            if peek(index).ttype == ttoken.TT_COMMA:
                index = advance(index)
                token = tokens[index]

        index = advance(index)

        return hash_literal, index

    def parse_array_literal(token: ttoken.Token, index: int) -> tuple[astt.ArrayLiteral, int]:
        array = astt.ArrayLiteral(token, [])

        exprlist, index = parse_exprlist(index, ttoken.TT_RBRACKET)
        if exprlist is not None:
            array.elements = exprlist

        return array, index

    def parse_exprlist(index: int, end: str) -> tuple[list[astt.Expression] | None, int]:
        exprlist = []

        if peek(index).ttype == end:
            index = advance(index)
            return exprlist, index

        index = advance(index)
        token = tokens[index]

        expression, index = parse_expression(LOWEST, token, index)

        if expression is not None:
            exprlist.append(expression)

        while peek(index).ttype == ttoken.TT_COMMA:
            index = advance(index)
            token = tokens[index]
            if token.ttype == ttoken.TT_EOF:
                errors.append(UnexpectedEOF(fname, (-1, -1)))
            index = advance(index)
            token = tokens[index]
            expression, index = parse_expression(LOWEST, token, index)
            token = tokens[index]
            if expression is not None:
                exprlist.append(expression)

        if peek(index).ttype != end:
            if peek(index).ttype == ttoken.TT_EOF:
                errors.append(UnexpectedEOF(fname, (-1, -1)))
            else:
                errors.append(UnexpectedToken(fname, end, peek(index).ttype, (-1, -1)))
            return None, index

        index = advance(index)

        return exprlist, index

    def parse_indexexpr(precedences: dict[str, int], left: astt.ArrayLiteral | astt.HashLiteral, token: ttoken.Token, index: int) -> tuple[astt.IndexExpression | None, int]:
        expression = astt.IndexExpression(token, left, astt.Expression(""))
        index = advance(index)
        token = tokens[index]
        if token == ttoken.TT_EOF:
            errors.append(UnexpectedEOF(fname, (-1, -1)))
            return None, index

        indexexpr, index = parse_expression(LOWEST, token, index)
        if indexexpr is not None:
            expression.index = indexexpr

        if peek(index).ttype != ttoken.TT_RBRACKET:
            errors.append(
                UnexpectedToken(fname, ttoken.TT_RBRACKET, peek(index).ttype, (-1, -1))
            )
            return None, index

        index = advance(index)

        return expression, index

    def parse_boolean(token: ttoken.Token, index: int) -> tuple[astt.Boolean, int]:
        return astt.Boolean(token, token.ttype == ttoken.TT_TRUE), index

    def parse_null(token: ttoken.Token, index: int) -> tuple[astt.Null, int]:
        return astt.Null(token), index

    def parse_num(token: ttoken.Token, index: int) -> tuple[astt.Number, int]:
        assert isinstance(token.value, float)
        return astt.Number(token), index

    def parse_str(token: ttoken.Token, index: int) -> tuple[astt.String, int]:
        return astt.String(token), index

    def parse_identifier(token: ttoken.Token, index: int) -> tuple[astt.Identifier, int]:
        return astt.Identifier(token), index

    program = astt.Program([])
    errors: list[Error] = []
    index = advance(-1)
    token = tokens[index]

    while token.ttype != ttoken.TT_EOF:
        if token.ttype == ttoken.TT_EOF:
            break
        statment, index = parse_statement(token, index)
        if statment is not None:
            program.statements.append(statment)
        index = advance(index)
        token = tokens[index]

    return program, errors
