#! /usr/bin/env python2.7

import sys, re, os
from time import time
from grammars.grammars import java
from grammar_parser.gparser import Terminal
from treelexer.lexer import Lexer
from incparser.syntaxtable import FinishSymbol, Reduce, Accept, Shift

class Parser(object):

    def __init__(self, stable):
        self.stable = stable
        self.state = 0
        self.stack = [("$", 0)]

    def parse(self, tokens):
        tokens = iter(tokens)
        la = Terminal(tokens.next()[1])
        while True:
            elem = self.stable.lookup(self.state, la)
            if type(elem) is Shift:
                self.state = elem.action
                self.stack.append((la, self.state))
                try:
                    token = tokens.next()
                    la = Terminal(token[1])
                except StopIteration:
                    la = FinishSymbol()
            elif type(elem) is Reduce:
                for i in range(elem.amount()):
                    self.stack.pop()
                self.state = self.stack[-1][1]
                goto = self.stable.lookup(self.state, elem.action.left)
                assert goto != None
                self.state = goto.action
                self.stack.append((elem.action.left, self.state))
            elif type(elem) is Accept:
                return True
            else:
                print("Could not parse", token)
                return False

if __name__ == "__main__":
    filename = sys.argv[1]
    filesize = os.path.getsize(filename)

    print("Running", filename)
    with open(filename, "r") as f:
        source = f.read()
    incparser, inclexer = java.load()
    lexer = inclexer.lexer
    stable = incparser.syntaxtable

    source = source.replace("\n", "\r") # Eco grammar compatiblity fix

    timings = []
    r = re.compile("=")
    delta = 0

    # initial parse
    tokens = lexer.lex(source)
    parser = Parser(stable)
    start = time()
    status = parser.parse(tokens)
    end = time()
    timings.append(str(end-start))

    for m in []:#r.finditer(source):
        # Edit file by inserting `1+` after every `=`
        pos = m.start() + 1 + delta
        source = source[:pos] + "1+" + source[pos:]

        lstart = time()
        tokens = lexer.lex(source)
        lend = time()
        parser = Parser(stable)
        start = time()
        status = parser.parse(tokens)
        end = time()
        if not status:
            break
        timings.append(str(end-start))

        delta += 2
    if len(timings) > 0:
        with open("results_t.csv", "a+") as f:
            f.write("{} {} {}".format(filename, filesize, ",".join(timings)))
            f.write("\n")
    else:
        print("No results.")
