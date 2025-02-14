import readline


def text_parse_bind():
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind(r"'\C-a': beginning-of-line")
    readline.parse_and_bind(r"'\C-e': end-of-line")
    readline.parse_and_bind(r"'\C-r': reverse-search-history")
    readline.parse_and_bind(r"'\M-b': backward-word")
    readline.parse_and_bind(r"'\M-f': forward-word")
    readline.parse_and_bind(r"'\C-u': unix-line-discard")