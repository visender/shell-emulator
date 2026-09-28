"""Разбор введённой строки на команду и аргументы."""

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
QUOTES = (SINGLE_QUOTE, DOUBLE_QUOTE)
ESCAPE = "\\"
ESCAPABLE_IN_DOUBLE = (DOUBLE_QUOTE, ESCAPE)


class ParseError(Exception):
    """Синтаксическая ошибка во введённой строке."""


class _Lexer:
    """Посимвольный разбор строки по правилам, близким к sh.

    Пробелы разделяют аргументы. Одинарные кавычки сохраняют текст
    как есть, двойные кавычки допускают экранирование ``\\"`` и
    ``\\\\``. Вне кавычек обратная косая черта экранирует любой
    следующий символ.
    """

    def __init__(self, line):
        """Подготовить разбор строки ``line``."""
        self._chars = iter(line)
        self._tokens = []
        self._current = []
        self._in_token = False
        self._quote = None

    def tokenize(self):
        """Выполнить разбор и вернуть список токенов.

        :raises ParseError: если кавычка не закрыта
        """
        for char in self._chars:
            if self._quote:
                self._read_quoted(char)
            else:
                self._read_plain(char)
        if self._quote:
            raise ParseError(
                f"unexpected EOF while looking for matching `{self._quote}'"
            )
        self._flush()
        return self._tokens

    def _read_plain(self, char):
        """Обработать символ вне кавычек."""
        if char in QUOTES:
            self._quote = char
            self._in_token = True
        elif char == ESCAPE:
            self._add(next(self._chars, ""))
        elif char.isspace():
            self._flush()
        else:
            self._add(char)

    def _read_quoted(self, char):
        """Обработать символ внутри кавычек."""
        if char == self._quote:
            self._quote = None
        elif char == ESCAPE and self._quote == DOUBLE_QUOTE:
            self._add(self._read_escape_in_double())
        else:
            self._add(char)

    def _read_escape_in_double(self):
        """Прочитать экранированную последовательность в ``"..."``."""
        char = next(self._chars, "")
        if char in ESCAPABLE_IN_DOUBLE:
            return char
        return ESCAPE + char

    def _add(self, text):
        """Добавить текст к текущему токену."""
        self._current.append(text)
        self._in_token = True

    def _flush(self):
        """Завершить текущий токен, если он начат."""
        if self._in_token:
            self._tokens.append("".join(self._current))
        self._current = []
        self._in_token = False


def split_line(line):
    """Разбить строку на токены с учётом кавычек и экранирования.

    >>> split_line('echo "hello world" \\'a b\\'')
    ['echo', 'hello world', 'a b']

    :param line: строка, введённая пользователем
    :return: список токенов
    :raises ParseError: если кавычка не закрыта
    """
    return _Lexer(line).tokenize()


def parse_command(line):
    """Разобрать строку на имя команды и список аргументов.

    :param line: строка, введённая пользователем
    :return: кортеж ``(имя, аргументы)`` или ``None`` для пустой строки
    :raises ParseError: если строка синтаксически неверна
    """
    tokens = split_line(line)
    if not tokens:
        return None
    return tokens[0], tokens[1:]
