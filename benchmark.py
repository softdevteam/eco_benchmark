#! /usr/bin/env python2.7

from __future__ import print_function
from grammars.grammars import java
from treemanager import TreeManager
from incparser.astree import BOS, EOS
from time import time
import sys, os

def run(filename):
    # Load grammar
    parser, lexer = java.load()
    treemanager = TreeManager()
    treemanager.add_parser(parser, lexer, "")

    # Load file
    print("Running", filename)
    with open(filename, "r") as f:
        treemanager.import_file(f.read())

    if not parser.last_status:
        print("Couldn't parse file. Skip.")
        return

    filesize = os.path.getsize(filename)

    timings = []

    # Insert `1+` after every `=`
    node = treemanager.get_bos()
    while type(node) is not EOS:
        if node.symbol.name == "=":
            node.insert("1+", len(node.symbol.name))
            node.mark_changed()
            treemanager.relex(node)
            treemanager.post_keypress("")
            treemanager.save_current_version()
            parser.prev_version = treemanager.version
            parser.reference_version = treemanager.reference_version
            start = time()
            parser.inc_parse()
            end = time()
            parser.top_down_reuse()
            treemanager.save_current_version(postparse=True) # save post parse tree
            if parser.last_status:
                treemanager.reference_version = treemanager.version
            TreeManager.version = treemanager.version

            if not parser.last_status:
                break
            timings.append(str(end-start))
        node = node.next_term

    if len(timings) > 0:
        with open("results.csv", "a+") as f:
            f.write("{} {} {}".format(filename, filesize, ",".join(timings)))
            f.write("\n")

if __name__ == "__main__":
    filename = sys.argv[1]
    run(filename)
