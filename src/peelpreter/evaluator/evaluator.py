##############################################################################
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
##############################################################################

from __future__ import annotations
from sys import setrecursionlimit

from .. import astt
from ..objectt.enviroment import Enviroment
from .. import error
from ..evaluator.mbuiltins import builtins
from .. import objectt as obj

setrecursionlimit(10**6)


def evaluate(node: astt.Node, env: Enviroment, fname="stdin") -> obj.Object:
    def istruthy(cond_object: obj.Object):
        if cond_object == obj.NULL:
            return False
        elif cond_object == obj.TRUE:
            return True
        elif cond_object == obj.FALSE:
            return False
        else:
            return True

    def is_error(tobject: obj.Object) -> bool:
        return tobject.type() == obj.OBJ_ERROR

    def eval_program(statements: list[astt.Statement]) -> obj.Object:
        result = obj.Object()
        for statement in statements:
            result = evaluate(statement, env)

            if isinstance(result, obj.ReturnValue):
                return result.value
            elif isinstance(result, obj.Error):
                return result

        return result

    def eval_blockstmt(block: astt.BlockStatement) -> obj.Object:
        result = obj.Object()

        for statement in block.statements:
            result = evaluate(statement, env)

            if (
                result.type() == obj.OBJ_RETURN_VALUE
                or result.type() == obj.OBJ_ERROR
            ):
                return result

        return result

    def eval_prefixexpr(operator: str, right: obj.Object) -> obj.Object:
        if operator ==  "!":
            return eval_bang(right)
        elif operator ==  "-":
            return eval_minus(right)
        else:
            return obj.Error(
                error.UnknownOperator(fname, operator, None, right.type(), (-1, -1))
            )

    def eval_infixexpr(operator: str, left: obj.Object, right: obj.Object) -> obj.Object:
        if left.type() == obj.OBJ_NUM and right.type() == obj.OBJ_NUM:
            assert isinstance(left, obj.Number) and isinstance(right, obj.Number)
            return eval_num_infixexpr(operator, left, right)
        elif left.type() == obj.OBJ_STRING and right.type() == obj.OBJ_STRING:
            assert isinstance(left, obj.String) and isinstance(right, obj.String)
            return eval_str_infixexpr(operator, left, right)
        elif operator == "==":
            return obj.TRUE if left == right else obj.FALSE
        elif operator == "!=":
            return obj.TRUE if left != right else obj.FALSE
        else:
            return obj.Error(
                error.UnknownOperator(
                    fname, operator, left.type(), right.type(), (-1, -1)
                )
            )

    def eval_num_infixexpr(operator: str, left: obj.Number, right: obj.Number) -> obj.Object:
        leftval = left.value
        rightval = right.value

        if operator == "+":
            return obj.Number(leftval + rightval)
        elif operator == "-":
            return obj.Number(leftval - rightval)
        elif operator == "*":
            return obj.Number(leftval * rightval)
        elif operator == "/":
            return obj.Number(leftval / rightval)
        elif operator == "<":
            return obj.TRUE if leftval < rightval else obj.FALSE
        elif operator == ">":
            return obj.TRUE if leftval > rightval else obj.FALSE
        elif operator == "==":
            return obj.TRUE if leftval == rightval else obj.FALSE
        elif operator == "!=":
            return obj.TRUE if leftval != rightval else obj.FALSE
        else:
            return obj.Error(
                error.UnknownOperator(
                    fname, operator, left.type(), right.type(), (-1, -1)
                )
            )

    def eval_str_infixexpr(operator: str, left: obj.String, right: obj.String) -> obj.Object:
        if operator != "+":
            return obj.Error(
                error.UnknownOperator(
                    fname, operator, left.type(), right.type(), (-1, -1)
                )
            )
        left_val = left.value
        right_val = right.value

        return obj.String(left_val + right_val)

    def eval_exprs(expressions: list[astt.Expression], env: Enviroment) -> list[obj.Object]:
        result = []
        for expression in expressions:
            evaluated = evaluate(expression, env)
            if is_error(evaluated):
                return [evaluated]
            result.append(evaluated)

        return result

    def eval_ifexpr(ifelse: astt.IfExpression) -> obj.Object:
        condition = evaluate(ifelse.condition, env)
        if is_error(condition):
            return condition

        if istruthy(condition):
            return evaluate(ifelse.consequence, env)
        elif ifelse.alternative.literal != "if":
            return evaluate(ifelse.alternative, env)
        else:
            return obj.NULL

    def eval_hashlit(node: astt.HashLiteral, env: Enviroment) -> obj.Object:
        pairs: dict[obj.HashKey, obj.HashPair] = dict()

        for key_node, val_node in node.pairs.items():
            key = evaluate(key_node, env)
            if is_error(key):
                return key
            if not isinstance(key, obj.Hashable):
                return obj.Error(error.UnsupporteKeyType(fname, key, (-1, -1)))
            value = evaluate(val_node, env)
            if is_error(value):
                return value
            hashed = key.hash_key()
            pairs[hashed] = obj.HashPair(key, value)

        return obj.Hash(pairs)

    def eval_indexexpr(left: obj.Object, indexexpr: obj.Object) -> obj.Object:
        if left.type() == obj.OBJ_ARRAY and indexexpr.type() == obj.OBJ_NUM:
            assert isinstance(left, obj.Array) and isinstance(indexexpr, obj.Number)
            return eval_arr_indexexpr(left, indexexpr)
        elif left.type() == obj.OBJ_STRING and indexexpr.type() == obj.OBJ_NUM:
            assert isinstance(left, obj.String) and isinstance(indexexpr, obj.Number)
            return eval_str_indexexpr(left, indexexpr)
        elif left.type() == obj.OBJ_HASH:
            assert isinstance(left, obj.Hash)
            return eval_hash_indexexpr(left, indexexpr)
        elif indexexpr.type() != obj.OBJ_NUM:
            return obj.Error(error.UnsupportedIndexType(fname, indexexpr, (-1, -1)))
        else:
            return obj.Error(error.UnsupportedIndexAccessType(fname, left, (-1, -1)))

    def eval_str_indexexpr(string: obj.String, indexexpr: obj.Number) -> obj.String:
        index = int(indexexpr.value)
        maximum = len(string.value) - 1

        if index < 0 or index > maximum:
            return obj.String("")
        return obj.String(string.value[index])

    def eval_hash_indexexpr(hash: obj.Hash, indexexpr: obj.Object) -> obj.Object:
        if not isinstance(indexexpr, obj.Hashable):
            return obj.Error(error.UnsupporteKeyType(fname, indexexpr, (-1, -1)))
        pair = hash.pairs.get(indexexpr.hash_key())
        if pair is None:
            return obj.NULL
        return pair.value

    def eval_hash_reassign(hash: obj.Hash, key: obj.Object, value: obj.Object) -> obj.Object:
        if not isinstance(key, obj.Hashable):
            return obj.Error(error.UnsupporteKeyType(fname, key, (-1, -1)))

        hash.pairs[key.hash_key()] = obj.HashPair(key, value)

        return value

    def eval_arr_indexexpr(array: obj.Array, indexexpr: obj.Number) -> obj.Object:
        index = int(indexexpr.value)
        maximum = len(array.elements) - 1

        if index < 0 or index > maximum:
            return obj.NULL
        return array.elements[index]

    def eval_arr_reassign(array: obj.Array, indexexpr: obj.Number, value: obj.Object) -> obj.Object:
        index = int(indexexpr.value)
        maximum = len(array.elements) - 1

        if index < 0 or index > maximum:
            return obj.Error("Out of Bounds")

        array.elements[index] = value

        return value

    def eval_identifier(node: astt.Identifier, env: Enviroment) -> obj.Object:
        value = env.get(node.literal)
        if value is not None:
            return value
        builtin = builtins.get(node.literal)
        if builtin is not None:
            return builtin

        return obj.Error(error.UnknownIdentifier(fname, node.literal, (-1, -1)))

    def eval_minus(right: obj.Object) -> obj.Object:
        if not isinstance(right, obj.Number):
            return obj.Error(
                error.UnknownOperator(fname, "-", None, right.type(), (-1, -1))
            )
        value = right.value
        return obj.Number(-value)

    def eval_bang(right: obj.Object) -> obj.Object:
        if right == obj.TRUE:
            return obj.FALSE
        elif right == obj.FALSE:
            return obj.TRUE
        elif right == obj.NULL:
            return obj.TRUE
        else:
            return obj.FALSE

    def apply_func(func: obj.Object, arguments: list[obj.Object]) -> obj.Object:
        if isinstance(func, obj.Function):
            if len(arguments) != len(func.parametres):
                return obj.Error("Mismatched number of args")
            extended_env = extend_funcenv(func, arguments)
            evaluated = evaluate(func.body, extended_env)
            return unwrap_rtrvalue(evaluated)
        elif isinstance(func, obj.Builtin):
            return func.func(fname, arguments)

        return obj.Error(error.NotAFunction(fname, func, (-1, -1)))

    def extend_funcenv(func: obj.Function, arguments: list[obj.Object]) -> Enviroment:
        env = Enviroment(func.env)
        for index, parameter in enumerate(func.parametres):
            env.set_iden(parameter.literal, arguments[index])
        return env

    def unwrap_rtrvalue(tobject: obj.Object) -> obj.Object:
        if isinstance(tobject, obj.ReturnValue):
            return tobject.value
        return tobject

    if isinstance(node, astt.Program):
        program: astt.Program = node
        return eval_program(program.statements)
    elif isinstance(node, astt.ExpressionStatement):
        return evaluate(node.expression, env)
    elif isinstance(node, astt.PrefixExpression):
        rightexpr = evaluate(node.rightexpr, env)
        if is_error(rightexpr):
            return rightexpr
        return eval_prefixexpr(node.operator, rightexpr)
    elif isinstance(node, astt.InfixExpression):
        left = evaluate(node.leftexpr, env)
        if is_error(left):
            return left
        right = evaluate(node.rightexpr, env)
        if is_error(right):
            return right
        return eval_infixexpr(node.operator, left, right)
    elif isinstance(node, astt.BlockStatement):
        return eval_blockstmt(node)
    elif isinstance(node, astt.FunctionLiteral):
        parametres = node.parameters
        body = node.body
        return obj.Function(parametres, body, env)
    elif isinstance(node, astt.CallExpression):
        function = evaluate(node.function, env)
        if is_error(function):
            return function
        arguments = eval_exprs(node.arguments, env)
        if len(arguments) == 1 and is_error(arguments[0]):
            return arguments[0]
        return apply_func(function, arguments)
    elif isinstance(node, astt.HashLiteral):
        return eval_hashlit(node, env)
    elif isinstance(node, astt.ArrayLiteral):
        elements = eval_exprs(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        return obj.Array(elements)
    elif isinstance(node, astt.IndexExpression):
        leftexpr = evaluate(node.left, env)
        if is_error(leftexpr):
            return leftexpr
        indexexpr = evaluate(node.index, env)
        if is_error(indexexpr):
            return indexexpr
        return eval_indexexpr(leftexpr, indexexpr)
    elif isinstance(node, astt.IfExpression):
        return eval_ifexpr(node)
    elif isinstance(node, astt.ReturnStatement):
        value = evaluate(node.valuexp, env)
        if is_error(value):
            return value
        return obj.ReturnValue(value)
    elif isinstance(node, astt.LetStatement):
        value = evaluate(node.value, env)
        if is_error(value):
            return value
        env.set_iden(name=node.name.literal, value=value)
        return value
    elif isinstance(node, astt.ReassignmentStatement):
        structure = evaluate(node.index_expr.left, env)
        index = evaluate(node.index_expr.index, env)
        value = evaluate(node.value, env)
        if isinstance(structure, obj.Array):
            if not isinstance(index, obj.Number):
                return obj.Error("Type mismatch for index")
            return eval_arr_reassign(structure, index, value)
        elif isinstance(structure, obj.Hash):
            return eval_hash_reassign(structure, index, value)
        else:
            return obj.Error("Unsupported")

    elif isinstance(node, astt.Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, astt.Number):
        return obj.Number(node.value)
    elif isinstance(node, astt.String):
        return obj.String(node.string)
    elif isinstance(node, astt.Boolean):
        if node.value:
            return obj.TRUE
        return obj.FALSE
    elif isinstance(node, astt.Null):
        return obj.NULL

    return obj.Error(error.UnknownNode(fname, (-1, -1)))
