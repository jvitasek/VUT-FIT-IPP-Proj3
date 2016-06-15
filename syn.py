#!/usr/bin/python3
# -*- coding: utf-8 -*-
#SYN:xjanou06

import sys
import getopt
import re
from error import Error
from tagger import Tagger

# valid arguments
ARGUMENTS = ['help', 'input=', 'output=', 'format=', 'br', 'escape', 'nooverlap']


def main():
    # getting the arguments
    try:
        optlist, extra = getopt.getopt(sys.argv[1:], '', ARGUMENTS)
    except getopt.GetoptError:
        Error.paramError()

    if len(extra) > 0:
        Error.paramError()

    # all once at maximum.
    keys = [opt[0] for opt in optlist]
    counts = [keys.count(x) for x in keys]

    if len(counts) > 0 and max(counts) > 1:
        Error.paramError()

    # help present in arguments
    if '--help' in keys:
        # help with more arguments
        if len(keys) > 1:
            Error.paramError()

        print("IPP SYN")
        print("--help\t\t\tprints help")
        print("--input\t\t\tinput file")
        print("--output\t\toutput file")
        print("--format\t\tformat file")
        print("--escape\t\tescape ampersand, less than and greater than")
        print("--br\t\t\t<br /> is added at the end of each line")
        exit(0)

    # parse the format file
    rules = []
    if '--format' in keys:
        try:
            ffile = open([opt[1] for opt in optlist if opt[0] == '--format'][0], 'r')
            rules = ffile.readlines()
            ffile.close()
        except:
            Error.inputError()

    # clean separate line feeds
    rules = Tagger.cleanSeparateLineFeeds(rules)

    # expressions
    expressions = [rule.split('\t', 1)[0] for rule in rules]

    # bonus NQS
    bonus_expressions = []
    for expression in expressions:
        bonus_expressions.append(Tagger.bonusReformatMutlipleQuantifiers(expression))
    expressions = bonus_expressions
    # end bonus NQS, remove this block if needed for basic functionality

    if(expressions):
        Tagger.validateExpressions(expressions)

    # commands
    commands = [[x.strip() for x in rule.split('\t', 1)[-1].split(',')] for rule in rules]
    if(commands):
        Tagger.validateCommands(commands)

    # reading the input file
    if '--input' in keys:
        try:
            ifile = open([opt[1] for opt in optlist if opt[0] == '--input'][0], 'r')
            lines = ifile.readlines()
            ifile.close()
        except:
            Error.inputError()
    else:
        lines = sys.stdin.readlines()
    stream = "".join([line for line in lines])

    # match expressions
    matches = []
    for i in range(0, len(rules)):
        # first try to replace negation
        replaced = Tagger.replaceNegation(expressions[i])

        # anything but negation
        if replaced == expressions[i]:
            regex = Tagger.makeRegex(expressions[i])
        # negation
        else:
            regex = replaced

        # compile the obtained regex
        try:
            p = re.compile(regex, re.DOTALL)
        except:
            Error.formatError()

        matches.append([])
        for m in p.finditer(stream):
            if len(m.group()) > 0:
                matches[i].append([m.start(), len(m.group())])

    # pair matches with tags
    changes = []
    for i in range(0, len(matches)):
        for match in matches[i]:
            for command in commands[i]:
                if len(command) > 0:
                    changes.append([match, Tagger.getTagsForCommand(command)])
    changes.sort(key=lambda tup: tup[0][0])

    # insert tags
    marked = ""
    sorted_ends = sorted(changes, key=lambda tup: tup[0][0] + tup[0][1], reverse=True)
    for i in range(0, len(stream) + 1):
        ends = [change[1][1] for change in sorted_ends if change[0][0] + change[0][1] == i]

        for end in reversed(ends):
            marked += end
        starts = [change[1][0] for change in changes if change[0][0] == i]
        for start in starts:
            marked += start
        if i != len(stream):
            if stream[i] == '\n' and '--br' in keys:
                marked += "<br />"
            marked += stream[i]

    # bonus part
    if '--escape' in keys:
        marked = Tagger.bonusEscapeSpecial(marked)
    # end bonus HTM, remove this block if basic functionality is needed

    # bonus part
    if '--nooverlap' in keys:
        marked = Tagger.bonusNoOverlap(marked)
    # end bonus HTM, remove this block if basic functionality is needed

    # output the results
    if '--output' in keys:
        try:
            ofile = open([opt[1] for opt in optlist if opt[0] == '--output'][0], 'w')
            ofile.write(marked)
            ofile.close()
        except:
            Error.outputError()
    else:
        print(marked, end='')

    exit(0)

if __name__ == '__main__':
    main()
