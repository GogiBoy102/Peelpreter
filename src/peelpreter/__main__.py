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
import readline  # noqa: F401
from sys import argv
from typing import Optional, Union

from .astt import Program
from . import error
from .evaluator import evaluate
from .objectt import NULL, Enviroment
from . import parser
from .token_type import TT_ERR, Token
from . import lexer
from . import objectt as obj


def run(fname: Optional[str], source: str, env) -> tuple[Union[Program, list[Token], str], Union[list[error.Error], None]]:
    def check_err(tokens):
        for token in tokens:
            if token.ttype == TT_ERR:
                return True
        return False

    def get_errs(tokens):
        errs = []
        for token in tokens:
            if token.ttype == TT_ERR:
                errs.append(token.value)
        return errs
    if fname is None:
        tokens = lexer.tokenize(source)
    else:
        tokens = lexer.tokenize(source, fname=fname)

    if check_err(tokens):
        return tokens, get_errs(tokens)

    program, errors = parser.parse(tokens)

    if len(errors) > 0:
        return program, errors

    result = str()
    result_obj = evaluate(program, env)
    if isinstance(result_obj, obj.Error):
        result = result_obj.inspect()
        errors.append(result_obj.error)
        return result, errors

    if result_obj != NULL:
        result = result_obj.inspect()

    return result, None

def repl():
    print(
    """    Peelpreter, Copyright (C) 2024 Jeebak Samajdwar

    This program comes with ABSOLUTELY NO WARRANTY; type "warranty" 
    for more details.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type "license" for details or visit 
    https://www.gnu.org/licenses/gpl-3.0.html.\n"""
    )
    print("Welcome! This is the the monkey programming language!")
    env = Enviroment(None)
    while True:
        try:
            source = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 

        if source == "license":
            print(
                """    Peelpreter is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version."""
            )
            continue
        elif source == "warranty":
            print( 
                """    Peelpreter is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""
            )    
            continue        

        result, errs = run(None, source, env)
        if not errs:
            if result == "":
                #TODO throw proper error
                continue
            print(result)
        else:
            for err in errs:
                print(str(err))

def main():
    if len(argv) == 1:
        repl()
    elif len(argv) == 2:
        with open(argv[1], "r") as sourcef:
            env = Enviroment(None)
            result, errors = run(argv[1], sourcef.read(), env)
            if errors is not None:
                result = ""
                for error in errors:
                    result += str(error)
                print(result)
    else:
        print("Invalid command line arguments. Please input only one argument being the file name or no argument for REPL")

if __name__ == "__main__":
    main()
