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

from .. import token_type as ttype

class Node:
    def __init__(self, literal: str) -> None:
        self.literal = literal
    def __repr__(self) -> str:
        return str()

class Statement(Node):
    def __init__(self, literal: str) -> None:
        super().__init__(literal)

    def __repr__(self) -> str:
        return f"{self.literal}"

class BlockStatement(Statement):
    def __init__(self, token: ttype.Token, statements: list[Statement]) -> None:
        super().__init__(token.string)
        self.token = token
        self.statements = statements

    def __repr__(self) -> str:
        result = "{\n"
        for statement in self.statements:
            result += "    " + repr(statement) + ";\n"
        return result + "}"

class Expression(Node):
    def __init__(self, literal: str) -> None:
        super().__init__(literal)

    def __repr__(self) -> str:
        return f"{self.literal}"

class Program(Node):
    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements
    
    def __repr__(self) -> str:
        result = ""
        for statement in self.statements:
            result += repr(statement) + "\n"
        result = result[:-1]

        return result

class Identifier(Expression):
    def __init__(self, token: ttype.Token) -> None:
        super().__init__(token.string)
        self.token = token

    def __repr__(self) -> str:
        return f"{self.literal}"

class Number(Expression):
    def __init__(self, token: ttype.Token) -> None:
        super().__init__(token.string)
        self.token = token
        assert isinstance(token.value, float)
        self.value: float = token.value

    def __repr__(self) -> str:
        return self.literal

class String(Expression):
    def __init__(self, token: ttype.Token) -> None:
        super().__init__(token.string)
        self.token = token
        self.string = token.string

    def __repr__(self) -> str:
        return "\"" + self.string + "\""

class Boolean(Expression):
    def __init__(self, token: ttype.Token, value: bool) -> None:
        super().__init__(token.string)
        self.token = token
        self.value = value
    
    def __repr__(self) -> str:
        return self.literal

class Null(Expression):
    def __init__(self, token: ttype.Token) -> None:
        super().__init__(token.string)
        self.token = token

    def __repr__(self) -> str:
        return self.literal

class PrefixExpression(Expression):
    def __init__(self, token: ttype.Token, rightexpr: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.operator = self.literal
        self.rightexpr = rightexpr

    def __repr__(self) -> str:
        return f"({self.operator}{self.rightexpr})"

class InfixExpression(Expression):
    def __init__(self, token: ttype.Token, leftexpr: Expression, rightexpr: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.leftexpr = leftexpr
        self.operator = self.literal
        self.rightexpr = rightexpr

    def __repr__(self) -> str:
        return f"({self.leftexpr} {self.operator} {self.rightexpr})"

class IfExpression(Expression):
    def __init__(self, token: ttype.Token, condition: Expression, consequence: BlockStatement, alternative: BlockStatement) -> None:
        super().__init__(token.string)
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self) -> str:
        result = f"if {self.condition} {self.consequence}{' else '+ repr(self.alternative) if self.alternative.literal != 'if' else ''}"
        return result

class FunctionLiteral(Expression):
    def __init__(self, token: ttype.Token, parameters: list[Identifier], body: BlockStatement) -> None:
        super().__init__(token.string)
        self.token = token
        self.parameters = parameters
        self.body = body
    
    def __repr__(self) -> str:
        result = f"{self.literal}({', '.join([repr(parametre) for parametre in self.parameters])}) {self.body}"

        return result

class ArrayLiteral(Expression):
    def __init__(self, token: ttype.Token, elements: list[Expression]) -> None:
        super().__init__(token.string)
        self.elements = elements

    def __repr__(self) -> str:
        return repr(self.elements)

class HashLiteral(Expression):
    def __init__(self, token: ttype.Token, pairs: dict[Expression, Expression]) -> None:
        super().__init__(token.string)
        self.token = token
        self.pairs = pairs
    
    def __repr__(self) -> str:
        return repr(self.pairs)

class LetStatement(Statement):
    def __init__(self, token: ttype.Token, name: Identifier, value: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"{self.literal} {self.name} = {self.value}"

class IndexExpression(Expression):
    def __init__(self, token: ttype.Token, left: ArrayLiteral | HashLiteral, index: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.left = left
        self.index = index

    def __repr__(self) -> str:
        return f"{self.left}[{self.index}]"

class ReassignmentStatement(Statement):
    def __init__(self, token: ttype.Token, index_expr: IndexExpression, value: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.index_expr = index_expr
        self.value = value

    def __repr__(self) -> str:
        return f"{self.literal} {self.index_expr} = {self.value}"

class ReturnStatement(Statement):
    def __init__(self, token: ttype.Token, expression: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.valuexp = expression

    def __repr__(self) -> str:
        return f"{self.literal} {self.valuexp}"

class CallExpression(Expression):
    def __init__(self, token: ttype.Token, function: FunctionLiteral, arguments: list[Expression]) -> None:
        super().__init__(token.string)
        self.token = token = token
        self.function = function
        self.arguments = arguments
    
    def __repr__(self) -> str:
        result = f"{self.function}({', '.join(repr(argument) for argument in self.arguments)})"
        return result

class ExpressionStatement(Statement):
    def __init__(self, token: ttype.Token, expression: Expression) -> None:
        super().__init__(token.string)
        self.token = token
        self.expression = expression

    def __repr__(self) -> str:
        return f"{self.expression}"
