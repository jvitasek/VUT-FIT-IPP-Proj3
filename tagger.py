#!/usr/bin/python3
# -*- coding: utf-8 -*-
#SYN:xjanou06

import re
from error import Error
from tag import Tag

# tag macros
BOLD = 'bold'
ITALIC = 'italic'
UNDERLINE = 'underline'
TELETYPE = 'teletype'
SIZE = 'size:\d+'
COLOR = 'color:[0-9a-fA-F]{6}'
SPLIT_SIZE = 5
MAX_COLOR = 6


class Tagger():

    def validateCommands(commands):
        for layer in commands:
            for command in layer:
                # test if the command is valid
                Tagger.getTagsForCommand(command)

                # test if size is a valid number
                if re.match(SIZE, command):
                    if(int(command[SPLIT_SIZE:]) not in range(1, 8)):
                        Error.formatError()
                # test if color is valid HEX
                elif re.match('color:[a-zA-Z0-9]+', command):
                    code = command.split(':')[-1]
                    if not re.match('[0-9a-fA-F]{6}', code):
                        Error.formatError()

    def validateExpressions(expressions):
        for expression in expressions:
            # two dots (without the percent sign)
            if re.search('(?<!%)\.\.', expression):
                Error.formatError()

            # invalid after exclamation point
            elif re.search('![\\\|\+\)\*\.!]', expression):
                Error.formatError()

            # invalid after dot
            elif re.search('\.[\*\|\+\)]', expression):
                Error.formatError()

            # invalid after pipe
            elif re.search('\|[\*\|\+\)\.]', expression):
                Error.formatError()

            # invalid after plus
            elif re.search('\+[\*\+!]', expression):
                Error.formatError()

            # invalid after asterisk
            elif re.search('\*[\*\|\+!]', expression):
                Error.formatError()

            # invalid after left parenthesis
            elif re.search('\([\*\+\.]', expression):
                Error.formatError()

            # empty priority parentheses
            elif re.search('\((\s+)?\)', expression):
                Error.formatError()

    def getTagsForCommand(command):
        if command == BOLD:
            return ('<b>', '</b>')
        elif command == ITALIC:
            return ('<i>', '</i>')
        elif command == UNDERLINE:
            return ('<u>', '</u>')
        elif command == TELETYPE:
            return ('<tt>', '</tt>')
        elif re.match(SIZE, command):
            if(int(command[SPLIT_SIZE:]) not in range(1, 8)):
                Error.formatError()
            return ('<font size=' + command[SPLIT_SIZE:] + '>', '</font>')
        elif re.match(COLOR, command):
            return ('<font color=#' + command[MAX_COLOR:] + '>', '</font>')
        # invalid command keyword
        else:
            Error.formatError()

    def replaceNegation(expression):
        # first replace all special regexes
        expression = re.sub('!%n', r'[^\n]', expression)
        expression = re.sub('!%d', r'[^0-9]', expression)
        expression = re.sub('!%t', r'[^\t]', expression)
        expression = re.sub('!%s', r'\S', expression)
        expression = re.sub('!%L', r'[^A-Z]', expression)
        expression = re.sub('!%l', r'[^a-z]', expression)
        expression = re.sub('!%a', r'', expression)
        expression = re.sub('!%w', r'[^a-zA-Z]', expression)
        expression = re.sub('!%W', r'[^\w]', expression)

        # then replace any other characters
        expression = re.sub('!(.)', r'[^\1]', expression)
        return expression

    def cleanSeparateLineFeeds(rules):
        result = []
        for rule in rules:
            if rule == '\n':
                continue
            else:
                result.append(rule)
        return result

    def makeRegex(expression):
        regex = ''
        p = False
        spec = False

        for i in range(0, len(expression)):
            # after % or !
            if p is True:
                p = False
                spec = False
                if expression[i] == '%':
                    regex += '%'
                elif expression[i] == 's':
                    regex += '\s'
                elif expression[i] == 'a':
                    regex += '.'
                elif expression[i] == 'd':
                    regex += '\d'
                elif expression[i] == 'l':
                    regex += '[a-z]'
                elif expression[i] == 'L':
                    regex += '[A-Z]'
                elif expression[i] == 'w':
                    regex += '[a-zA-Z]'
                elif expression[i] == 'W':
                    regex += '[a-zA-Z0-9]'
                elif expression[i] == 't':
                    regex += '\\t'
                elif expression[i] == 'n':
                    regex += '\\n'
                elif expression[i] == '.':
                    regex += '\.'
                elif expression[i] == '|':
                    regex += '\|'
                elif expression[i] == '!':
                    regex += '!'
                elif expression[i] == '*':
                    regex += '\*'
                elif expression[i] == '+':
                    regex += '\+'
                elif expression[i] == '(':
                    regex += '\('
                elif expression[i] == ')':
                    regex += '\)'
                elif expression[i] == '\\':
                    regex += '\\\\\\\\'

            # not after % or !
            else:
                # following special regex
                if expression[i] == '%' or expression[i] == '\\':
                    p = True  # after %
                    continue
                # negation
                elif expression[i] == '!':
                    p = True
                    continue
                # skipping concatenation
                elif expression[i] == '.':
                    spec = True
                    continue
                # any standalone characters
                elif expression[i] == '|':
                    spec = True
                    regex += expression[i]
                    continue
                # any character other than the above
                regex += expression[i]
                spec = False

        if p is True or spec is True:
            Error.formatError()

        return regex

    def bonusEscapeSpecial(output):
        # escaping ampersand
        output = re.sub('&', '&amp;', output)
        # escaping less than
        output = re.sub('\<(?!\/|[b|i|u|tt|font])', '&lt;', output)
        # escaping greater than
        output = re.sub('(?<![b|i|u|tt|font])\>', '&gt;', output)
        return output

    def bonusNoOverlap(output):
        p = re.compile(r'\<(\w)\>.*(\<\w\>).*\<\/\1\>', re.DOTALL)
        res = p.finditer(output)
        for item in res:
            prob = item.group()
            container_len = len(item.group(1))
            tag = item.group(2)[0:1] + '/' + item.group(2)[1:]
            res = prob[:-(container_len+3)] + tag + prob[len(prob)-container_len-3:]
            output = re.sub(prob, res, output)

        return output

    def bonusFindOpeningTags(output):
        tag_list = []
        tag = False
        tag_name = ''
        for i in range(0, len(output)):
            if tag is False:
                if output[i] == '<' and output[i+1] != '/':
                    tag = True
            else:
                tag_name += output[i]
                if output[i+1] == '>':
                    tag_list.append(Tag(i, i+len(tag_name), tag_name))
                    tag = False
                    tag_name = ''

        return tag_list

    def bonusFindClosingTags(output):
        tag_list = []
        tag = False
        tag_name = ''
        for i in range(0, len(output)):
            if tag is False:
                if output[i] == '<' and output[i+1] == '/':
                    tag = True
            else:
                if output[i] != '/':
                    tag_name += output[i]
                if output[i+1] == '>':
                    tag_list.append(Tag(i, i+len(tag_name), tag_name))
                    tag = False
                    tag_name = ''

        return tag_list

    def bonusMultipleQuantifiersPriority(quantifiers):
        if re.search('\!', quantifiers):
            return '!'
        elif re.search('\*', quantifiers):
            return '*'
        elif re.search('\+', quantifiers):
            return '+'
        elif re.search('\.', quantifiers):
            return '.'
        elif re.search('\|', quantifiers):
            return '|'

    def bonusReformatMutlipleQuantifiers(expression):
        quantifiers = re.search('[\!|\*|\+|\.|\|]+$', expression)
        if quantifiers:
            quant = Tagger.bonusMultipleQuantifiersPriority(quantifiers.group(0))
        else:
            return expression
        quantifiers = re.sub('[\!|\*|\+|\.|\|]+$', quant, expression)
        return quantifiers
