#!/usr/bin/python3
# -*- coding: utf-8 -*-
#SYN:xjanou06

import unittest
from tagger import Tagger
from error import Error


class testSyntaxHighlightingClass(unittest.TestCase):

    """ Command Validator tests. """
    def testCommandValidatorUnknownCommand(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateCommands([['foobar']])

        self.assertEqual(exit_val.exception.code, 4)

    def testCommandValidatorInvalidSize(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateCommands([['size:352333']])

        self.assertEqual(exit_val.exception.code, 4)

    def testCommandValidatorZeroSize(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateCommands([['size:0']])

        self.assertEqual(exit_val.exception.code, 4)

    def testCommandValidatorMinSize(self):
        Tagger.validateCommands([['size:1']])
        self.assertTrue(self)

    def testCommandValidatorMaxSize(self):
        Tagger.validateCommands([['size:7']])
        self.assertTrue(self)

    def testCommandValidatorInvalidColor(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateCommands([['color:qwe@*fefeee']])

        self.assertEqual(exit_val.exception.code, 4)

    """ Expression Validator tests. """
    def testExpressionValidatorTwoDots(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a..b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorNegationAndDot(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a!.b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorEmptyBrackets(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['(())'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorNegationAndPipe(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a!|b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorNegationAndNegation(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a!!b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorNegationAndAsterisk(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a!*b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorConcatenationAndDisjunction(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a.|b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorDisjunctionAndConcatenation(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a|.b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorPlusAndAsterisk(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a+*b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorAsteriskAndExclamation(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['a*!b'])

        self.assertEqual(exit_val.exception.code, 4)

    def testExpressionValidatorLeftParenthesisAndPipe(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.validateExpressions(['(|)'])

        self.assertEqual(exit_val.exception.code, 4)

    """ Command -> Tag transformation tests. """
    def testTaggerBoldTags(self):
        self.assertEqual(Tagger.getTagsForCommand('bold'), ('<b>', '</b>'))

    def testTaggerItalicTags(self):
        self.assertEqual(Tagger.getTagsForCommand('italic'), ('<i>', '</i>'))

    def testTaggerUnderlineTags(self):
        self.assertEqual(Tagger.getTagsForCommand('underline'), ('<u>', '</u>'))

    def testTaggerTeletypeTags(self):
        self.assertEqual(Tagger.getTagsForCommand('teletype'), ('<tt>', '</tt>'))

    def testTaggerSizeTags(self):
        self.assertEqual(Tagger.getTagsForCommand('size:4'), ('<font size=4>', '</font>'))

    def testTaggerColorTags(self):
        self.assertEqual(Tagger.getTagsForCommand('color:FF0000'), ('<font color=#FF0000>', '</font>'))

    def testTaggerZeroSizeError(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.getTagsForCommand('size:0')

        self.assertEqual(exit_val.exception.code, 4)

    def testTaggerNegativeSizeError(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.getTagsForCommand('size:-1')

        self.assertEqual(exit_val.exception.code, 4)

    """ Command -> Regex transformation tests. """
    def testRegexLetters(self):
        self.assertEqual(Tagger.makeRegex('test'), 'test')

    def testRegexNumbers(self):
        self.assertEqual(Tagger.makeRegex('12314'), '12314')

    def testRegexSpecialWhitespace(self):
        self.assertEqual(Tagger.makeRegex('%s'), '\s')

    def testRegexSpecialArbitraryLetter(self):
        self.assertEqual(Tagger.makeRegex('%a'), '.')

    def testRegexSpecialNumbers(self):
        self.assertEqual(Tagger.makeRegex('%d'), '\d')

    def testRegexSpecialLowercaseLetters(self):
        self.assertEqual(Tagger.makeRegex('%l'), '[a-z]')

    def testRegexSpecialUppercaseLetters(self):
        self.assertEqual(Tagger.makeRegex('%L'), '[A-Z]')

    def testRegexSpecialLowerUpperLetters(self):
        self.assertEqual(Tagger.makeRegex('%w'), '[a-zA-Z]')

    def testRegexSpecialLowerUpperLettersAndNumbers(self):
        self.assertEqual(Tagger.makeRegex('%W'), '[a-zA-Z0-9]')

    def testRegexSpecialTab(self):
        self.assertEqual(Tagger.makeRegex('%t'), '\\t')

    def testRegexNewline(self):
        self.assertEqual(Tagger.makeRegex('%n'), '\\n')

    def testRegexEscapeDot(self):
        self.assertEqual(Tagger.makeRegex('%.'), '\.')

    def testRegexEscapePipe(self):
        self.assertEqual(Tagger.makeRegex('%|'), '\|')

    def testRegexEscapeExclamation(self):
        self.assertEqual(Tagger.makeRegex('%!'), '!')

    def testRegexEscapeAsterisk(self):
        self.assertEqual(Tagger.makeRegex('%*'), '\*')

    def testRegexEscapePlus(self):
        self.assertEqual(Tagger.makeRegex('%+'), '\+')

    def testRegexEscapeLeftParenthesis(self):
        self.assertEqual(Tagger.makeRegex('%('), '\(')

    def testRegexEscapeRightParenthesis(self):
        self.assertEqual(Tagger.makeRegex('%)'), '\)')

    def testRegexEscapePercent(self):
        self.assertEqual(Tagger.makeRegex('%%'), '%')

    def testRegexEscapeBackslash(self):
        self.assertEqual(Tagger.makeRegex('\\\\'), r'\\\\')

    def testRegexOnlyConcatenation(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.makeRegex('.')

        self.assertEqual(exit_val.exception.code, 4)

    def testRegexOnlyPipe(self):
        with self.assertRaises(SystemExit) as exit_val:
            Tagger.makeRegex('|')

        self.assertEqual(exit_val.exception.code, 4)

    """ Negation replacer tests. """
    def testRegexNegationNewline(self):
        self.assertEqual(Tagger.replaceNegation('!%n'), '[^\n]')

    def testRegexNegationDigit(self):
        self.assertEqual(Tagger.replaceNegation('!%d'), '[^0-9]')

    def testRegexNegationTab(self):
        self.assertEqual(Tagger.replaceNegation('!%t'), '[^\t]')

    def testRegexNegationWhitespace(self):
        self.assertEqual(Tagger.replaceNegation('!%s'), '\S')

    def testRegexNegationUppercaseLetter(self):
        self.assertEqual(Tagger.replaceNegation('!%L'), '[^A-Z]')

    def testRegexNegationLowercaseLetter(self):
        self.assertEqual(Tagger.replaceNegation('!%l'), '[^a-z]')

    def testRegexNegationAnyCharacter(self):
        self.assertEqual(Tagger.replaceNegation('!%a'), '')

    def testRegexNegationUppercaseAndLowercaseLetter(self):
        self.assertEqual(Tagger.replaceNegation('!%w'), '[^a-zA-Z]')

    def testRegexNegationAnyLetterOrDigit(self):
        self.assertEqual(Tagger.replaceNegation('!%W'), '[^\w]')

    def testRegexNegationSpecificCharacter(self):
        self.assertEqual(Tagger.replaceNegation('!a'), '[^a]')

    """ Testing the exit value when exceptions are thrown. """
    def testParamErrorReturnValue(self):
        with self.assertRaises(SystemExit) as exit_val:
            Error.paramError()

        self.assertEqual(exit_val.exception.code, 1)

    def testInputErrorReturnValue(self):
        with self.assertRaises(SystemExit) as exit_val:
            Error.inputError()

        self.assertEqual(exit_val.exception.code, 2)

    def testOutputErrorReturnValue(self):
        with self.assertRaises(SystemExit) as exit_val:
            Error.outputError()

        self.assertEqual(exit_val.exception.code, 3)

    def testFormatErrorReturnValue(self):
        with self.assertRaises(SystemExit) as exit_val:
            Error.formatError()

        self.assertEqual(exit_val.exception.code, 4)

    """ Separate line feeds cleaner. """
    def testCleanSeparateLineFeed(self):
        self.assertEqual(Tagger.cleanSeparateLineFeeds(['a\tbold\n', '\n', 'b\titalic\n', 'c\tunderline\n', '\n', 'd\tteletype\n', 'e\tsize:1\n', '\n', 'f\tsize:7\n', 'g\tcolor:000000\n', '\n', 'h\tcolor:FFFFFF\n', '\n']), ['a\tbold\n', 'b\titalic\n', 'c\tunderline\n', 'd\tteletype\n', 'e\tsize:1\n', 'f\tsize:7\n', 'g\tcolor:000000\n', 'h\tcolor:FFFFFF\n'])

    """ Bonus escape special char tests. """
    def testBonusEscapeAmpersand(self):
        self.assertEqual(Tagger.bonusEscapeSpecial('<b>testovaci <i>soubor</b> s &</i>'), '<b>testovaci <i>soubor</b> s &amp;</i>')

    def testBonusEscapeLessThan(self):
        self.assertEqual(Tagger.bonusEscapeSpecial('<b>testovaci <i>soubor</b> s <</i>'), '<b>testovaci <i>soubor</b> s &lt;</i>')

    def testBonusEscapeMoreLessThan(self):
        self.assertEqual(Tagger.bonusEscapeSpecial('<b><<<<<<</b>'), '<b>&lt;&lt;&lt;&lt;&lt;&lt;</b>')

    def testBonusEscapeGreaterThan(self):
        self.assertEqual(Tagger.bonusEscapeSpecial('<b>testovaci <i>soubor</b> s ></i>'), '<b>testovaci <i>soubor</b> s &gt;</i>')

    def testBonusEscapeMoreGreaterThan(self):
        self.assertEqual(Tagger.bonusEscapeSpecial('<b>>>>>>></b>'), '<b>&gt;&gt;&gt;&gt;&gt;&gt;</b>')

    """ Bonus no overlap tests. """
    def testExampleOverlapping(self):
        self.assertEqual(Tagger.bonusNoOverlap('<u>111<i>222</u><b>333</b></i>'), '<u>111<i>222</i></u><b><i>333</i></b>')

    """ Bonus quantifier priority tests. """
    def testQuantifierPriorityExclamationAndAsterisk(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('****!*'), '!')

    def testQuantifierPriorityExclamationAndPlus(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('+++!++'), '!')

    def testQuantifierPriorityExclamationAndDot(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('..!!..'), '!')

    def testQuantifierPriorityExclamationAndPipe(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('||!!|'), '!')

    def testQuantifierPriorityAsteriskAndPlus(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('+**+*'), '*')

    def testQuantifierPriorityAsteriskAndDot(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('**.**...'), '*')

    def testQuantifierPriorityAsteriskAndPipe(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('||*|||**'), '*')

    def testQuantifierPriorityPlusAndDot(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('+++.++..+'), '+')

    def testQuantifierPriorityPlusAndPipe(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('|++||+'), '+')

    def testQuantifierPriorityDotAndPipe(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('..|||...'), '.')

    def testQuantifierPriorityExclamation(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('!!!!!!'), '!')

    def testQuantifierPriorityAsterisk(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('******'), '*')

    def testQuantifierPriorityPlus(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('+++++++'), '+')

    def testQuantifierPriorityDot(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('..........'), '.')

    def testQuantifierPriorityPipe(self):
        self.assertEqual(Tagger.bonusMultipleQuantifiersPriority('||||'), '|')

    """ Bonus quantifier reformat tests. """
    def testReformatMultipleQuantifiers(self):
        self.assertEqual(Tagger.bonusReformatMutlipleQuantifiers('sub+++'), 'sub+')

unittest.main()
