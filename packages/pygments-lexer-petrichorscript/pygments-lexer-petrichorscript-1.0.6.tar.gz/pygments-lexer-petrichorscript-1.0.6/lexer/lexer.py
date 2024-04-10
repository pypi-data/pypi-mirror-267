from pygments.lexer import RegexLexer, bygroups
from pygments.token import *


__all__ = ('PetrichorScriptLexer')


class PetrichorScriptLexer(RegexLexer):
    name = 'PetrichorScript'
    aliases = ['petrichor','ptcr']
    filenames = ['*.petrichor','*.ptcr']

    tokens = {
        'root': [
            (r'\s+', Text), # whitespace
            (r'\\.', String.Escape), # escaped character
            (r'//.*\n', Comment.Single), # line comment
            (r',', Punctuation), # comma
            (r'[\{\}]', Operator), # token body boundaries
            (r'(?<!>)>>(?!>)', Operator), # text shortcut template divider operator
            (r'(^\s*[a-z]+(?:-[a-z0-9]+)*(?:-[a-z]+)?)(\s*)(:)', bygroups(Keyword.Reserved, Text, Operator)), # token name, whitespacae, token divider
            (r'\[[a-z\-]+\]', Name.Variable), # field
            (r'(?<!\\)"', String, 'string'), # string start
            (r'\b(-)?[0-9.]+\b', Number),
            (r'.', Text),
        ],
        'string': [
            (r'\\.', String.Escape),
            (r'"', String, '#pop'), # string end
            (r'[^\\"]+', String),
        ]
    }
