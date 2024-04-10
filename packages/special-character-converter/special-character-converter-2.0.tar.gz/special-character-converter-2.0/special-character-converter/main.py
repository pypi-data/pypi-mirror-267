import re

special_replacements = {
    'star': '*',
    'open bracket': '(',
    'close bracket': ')',
    'exclamation mark': '!',
    'at symbol': '@',
    'hash symbol': '#',
    'dollar sign': '$',
    'percent sign': '%',
    'caret': '^',
    'ampersand': '&',
    'asterisk': '*',
    'hyphen': '-',
    'underscore': '_',
    'plus sign': '+',
    'equal sign': '=',
    'curly brackets': '{ }',
    'square brackets': '\[ \]',
    'vertical bar': '|',
    'backslash': '\\\\',
    'colon': ':',
    'semicolon': ';',
    'double quotation marks': '"',
    'single quotation marks': "'",
    'less than symbol': '<',
    'greater than symbol': '>',
    'comma': ',',
    'period': '\.',
    'forward slash': '/',
    'question mark': '\?',
    'tilde': '~',
    'grave accent': '`',
    'degree symbol': '°',
    'cent symbol': '¢',
    'registered trademark symbol': '®',
    'trademark symbol': '™',
    'copyright symbol': '©',
    'oblique':'/'
}

def convert_to_special(text):
    for word, special_char in special_replacements.items():
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        text = pattern.sub(special_char, text)
    return text


