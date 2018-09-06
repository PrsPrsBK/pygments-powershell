# -*- coding: utf-8 -*-
"""
    pygments.lexers.shell
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for various shells.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, do_insertions, bygroups, \
    include, default, this, using, words
from pygments.token import Punctuation, \
    Text, Comment, Operator, Keyword, Name, String, Number, Generic
from pygments.util import shebang_matches


__all__ = ['BashLexer', 'BashSessionLexer', 'TcshLexer', 'BatchLexer',
           'MSDOSSessionLexer', 'PowerShellLexer',
           'PowerShellSessionLexer', 'TcshSessionLexer', 'FishShellLexer']

line_re = re.compile('.*?\n')




class PowerShellLexer(RegexLexer):
    """
    For Windows PowerShell code.

    .. versionadded:: 1.5
    """
    name = 'PowerShell'
    aliases = ['powershell', 'posh', 'ps1', 'psm1']
    filenames = ['*.ps1', '*.psm1']
    mimetypes = ['text/x-powershell']

    flags = re.DOTALL | re.IGNORECASE | re.MULTILINE

    keywords = (
        'while validateset validaterange validatepattern validatelength '
        'validatecount until trap switch return ref process param parameter in '
        'if global: function foreach for finally filter end elseif else '
        'dynamicparam do default continue cmdletbinding break begin alias \\? '
        '% #script #private #local #global mandatory parametersetname position '
        'valuefrompipeline valuefrompipelinebypropertyname '
        'valuefromremainingarguments helpmessage try catch throw').split()

    operators = (
        'and as band bnot bor bxor casesensitive ccontains ceq cge cgt cle '
        'clike clt cmatch cne cnotcontains cnotlike cnotmatch contains '
        'creplace eq exact f file ge gt icontains ieq ige igt ile ilike ilt '
        'imatch ine inotcontains inotlike inotmatch ireplace is isnot le like '
        'lt match ne not notcontains notlike notmatch or regex replace '
        'wildcard').split()

    verbs = (
        'write where wait use update unregister undo trace test tee take '
        'suspend stop start split sort skip show set send select scroll resume '
        'restore restart resolve resize reset rename remove register receive '
        'read push pop ping out new move measure limit join invoke import '
        'group get format foreach export expand exit enter enable disconnect '
        'disable debug cxnew copy convertto convertfrom convert connect '
        'complete compare clear checkpoint aggregate add').split()

    commenthelp = (
        'component description example externalhelp forwardhelpcategory '
        'forwardhelptargetname functionality inputs link '
        'notes outputs parameter remotehelprunspace role synopsis').split()

    tokens = {
        'root': [
            # we need to count pairs of parentheses for correct highlight
            # of '$(...)' blocks in strings
            (r'\(', Punctuation, 'child'),
            (r'\${', Punctuation, 'brace-exp'),
            (r'\s+', Text),
            (r'^(\s*#[#\s]*)(\.(?:%s))([^\n]*$)' % '|'.join(commenthelp),
             bygroups(Comment, String.Doc, Comment)),
            (r'#[^\n]*?$', Comment),
            (r'(&lt;|<)#', Comment.Multiline, 'multline'),
            (r'@"\n', String.Heredoc, 'heredoc-double'),
            (r"@'\n.*?\n'@", String.Heredoc),
            # escaped syntax
            (r'`[\'"$@-]', Punctuation),
            (r'"', String.Double, 'string'),
            (r"'([^']|'')*'", String.Single),
            (r'(\$|@@|@)((global|script|private|env):)?\w+',
             Name.Variable),
            (r'(Function|Variable):\\?\w+',
             Name.Variable),
            (r'env:\\?\w+',
             Name.Variable),
            (r'[a-zA-Z]+:\\[\w\.\\]+',
             Name.Variable),
            (r'(%s)\b' % '|'.join(keywords), Keyword),
            (r'-(%s)\b' % '|'.join(operators), Operator),
            (r'(%s)-[a-z_]\w*\b' % '|'.join(verbs), Name.Builtin),
            (r'\[[a-z_\[][\w. `,\[\]]*\]', Name.Constant),  # .net [type]s
            (r'-[a-z_]\w*', Name),
            (r'\w+', Name),
            (r'[.,;@{}\[\]$()=+*/\\&%!~?^`|<>-]|::', Punctuation),
            # :- of magick.exe info:-
            (r'[\w+-\.:]+', Keyword),
        ],
        'brace-exp': [
            (r'}', Punctuation, '#pop'),
            include('root'),
        ],
        'child': [
            (r'\)', Punctuation, '#pop'),
            include('root'),
        ],
        'multline': [
            (r'[^#&.]+', Comment.Multiline),
            (r'#(>|&gt;)', Comment.Multiline, '#pop'),
            (r'\.(%s)' % '|'.join(commenthelp), String.Doc),
            (r'[#&.]', Comment.Multiline),
        ],
        'string': [
            (r"`[0abfnrtv'\"$`]", String.Escape),
            (r'[^$`"]+', String.Double),
            (r'\$\(', Punctuation, 'child'),
            (r'""', String.Double),
            (r'[`$]', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'heredoc-double': [
            (r'\n"@', String.Heredoc, '#pop'),
            (r'\$\(', Punctuation, 'child'),
            (r'[^@\n]+"]', String.Heredoc),
            (r".", String.Heredoc),
        ]
    }
