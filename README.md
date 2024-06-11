# Monkey
Peelpreter is a interpreter for the language Monkey specified in the book `Writing an Interpreter in Go`.
It is not not designed to be the fastest implementation but instead a (mostly) readable one. 
I, personally don't find encapsulating every little function of a program in classes to be particularly readable.
Hence, I have kept things bare-bone functions where I thought it made sense and used classes to encapsulate data like C-Structs
and sometimes to store methods.

### Monkey Features
Peelpreter supports all features of the canon implementation as well as some more.
They are:-
1. Variables
2. If expressions
3. First-Class Functions
4. Closures
5. Array
6. Hash Map (Dictionary)
7. Builtin Functions
8. Array and Hash mutability
9. Improved `puts` function

### Features Planned to be added
Some features which I wish for in a programming language are not present yet in this.
Suppport for them will be slowly added ~as soon as type annotations are improved for the existing code base~.
They are:-
1. Input function
2. Type conversion
3. Constants
4. Loops
5. Structs
6. Chaining variable assignments. E.g, `let x = y = 7`
7. Import System
8. Extension modules using Python

I might also added a Type Checker later on, but thats upto the future.

## Installation
For installation of the package run,
```
pip install peelpreter
```
Or if you would prefer to build and install yourself for a more up-to-date version, clone the repository and cd into it,
```
git clone https://github.com/GogiBoy102/Peelpreter.git
cd Peelpreter
```
then run,
```
python3 -m build
```
If `build` is not already installed onto the system then install it with,
```
pip install --upgrade build
```
After the build process ends, cd into `dist` and install the tar with,
```
cd dist
pip install peelpreter-<version>.tar.gz
```
And, voila! Peelpreter has been installed! For usage, follow the next section.

## Usage
Peelpreter comes with a script called `monkey` which is the entry point for the interpreter and also the reccomended way for it to be used.

Files in monkey usually have the extension ".mon".

`monkey`, when executed with no command line arguments starts the REPL for Monkey. However, it can also execute files if the path to those files are supplied as a command line argument.
The examples directory can be looked at for example programs writen in Monkey.
```
monkey (for starting a repl)
```
```
monkey /path/to/file (for running a file)
```

## License
Peelpreter is license under the GNU General Public License version 3 or above with it also being copyrighted by `Jeebak Samajdwar`

