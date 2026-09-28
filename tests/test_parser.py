"""Тесты разбора командной строки."""

import unittest

from shell_emulator.parser import ParseError, parse_command, split_line


class SplitLineTest(unittest.TestCase):
    """Проверки функции split_line."""

    def test_splits_by_whitespace(self):
        """Аргументы разделяются любым количеством пробелов."""
        self.assertEqual(split_line("ls  -l\t/home"), ["ls", "-l", "/home"])

    def test_double_quotes_group_words(self):
        """Текст в двойных кавычках становится одним аргументом."""
        self.assertEqual(
            split_line('cd "My Documents"'), ["cd", "My Documents"]
        )

    def test_single_quotes_group_words(self):
        """Текст в одинарных кавычках становится одним аргументом."""
        self.assertEqual(split_line("ls 'a b' c"), ["ls", "a b", "c"])

    def test_quotes_inside_word(self):
        """Кавычки внутри слова склеиваются с соседним текстом."""
        self.assertEqual(split_line('ab"c d"e'), ["abc de"])

    def test_empty_quotes_give_empty_argument(self):
        """Пустые кавычки дают пустой аргумент."""
        self.assertEqual(split_line('ls ""'), ["ls", ""])

    def test_other_quote_inside_quotes(self):
        """Кавычка другого типа внутри кавычек — обычный символ."""
        self.assertEqual(split_line("\"it's\""), ["it's"])

    def test_escape_outside_quotes(self):
        """Обратная косая черта экранирует пробел."""
        self.assertEqual(split_line("cd a\\ b"), ["cd", "a b"])

    def test_escape_inside_double_quotes(self):
        """В двойных кавычках экранируются только \\" и \\\\."""
        self.assertEqual(split_line('"a\\"b\\\\c\\n"'), ['a"b\\c\\n'])

    def test_no_escape_inside_single_quotes(self):
        """В одинарных кавычках обратная косая черта не действует."""
        self.assertEqual(split_line("'a\\b'"), ["a\\b"])

    def test_unclosed_double_quote(self):
        """Незакрытая двойная кавычка — синтаксическая ошибка."""
        with self.assertRaises(ParseError):
            split_line('ls "abc')

    def test_unclosed_single_quote(self):
        """Незакрытая одинарная кавычка — синтаксическая ошибка."""
        with self.assertRaises(ParseError):
            split_line("ls 'abc")


class ParseCommandTest(unittest.TestCase):
    """Проверки функции parse_command."""

    def test_empty_line(self):
        """Пустая строка не является командой."""
        self.assertIsNone(parse_command("   "))

    def test_command_with_args(self):
        """Первый токен — имя команды, остальные — аргументы."""
        self.assertEqual(
            parse_command('ls -l "x y"'), ("ls", ["-l", "x y"])
        )


if __name__ == "__main__":
    unittest.main()
