"""Тесты выполнения стартового скрипта."""

import io
import os
import tempfile
import unittest

from shell_emulator.commands import ExitRequest
from shell_emulator.script import ScriptError, is_skipped, run_script
from shell_emulator.shell import Shell


def make_shell():
    """Создать оболочку с подменёнными потоками вывода."""
    return Shell(stdin=io.StringIO(), stdout=io.StringIO(),
                 stderr=io.StringIO())


class ScriptTest(unittest.TestCase):
    """Проверки функции run_script."""

    def setUp(self):
        """Создать временный каталог для файлов скриптов."""
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)

    def write_script(self, text):
        """Записать скрипт во временный файл и вернуть путь к нему."""
        path = os.path.join(self._tmp.name, "start.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return path

    def test_echoes_input_and_output(self):
        """Команда выводится после приглашения, затем её результат."""
        shell = make_shell()
        run_script(shell, self.write_script("ls a\n"))
        expected = f"{shell.prompt()}ls a\nls: args=['a']\n"
        self.assertEqual(shell.stdout.getvalue(), expected)

    def test_skips_failed_lines(self):
        """Ошибочная строка пропускается, выполнение продолжается."""
        shell = make_shell()
        path = self.write_script("foo\ncd a b\nls\n")
        self.assertEqual(run_script(shell, path), 2)
        self.assertIn("ls: args=[]", shell.stdout.getvalue())
        errors = shell.stderr.getvalue()
        self.assertIn(f"{path}:1: line skipped (exit status 127)", errors)
        self.assertIn(f"{path}:2: line skipped (exit status 1)", errors)

    def test_skips_comments_and_empty_lines(self):
        """Комментарии и пустые строки не выполняются и не выводятся."""
        shell = make_shell()
        run_script(shell, self.write_script("# comment\n\n   \nls\n"))
        self.assertEqual(shell.stdout.getvalue().count(shell.prompt()), 1)

    def test_exit_stops_script(self):
        """Команда exit прерывает скрипт."""
        shell = make_shell()
        with self.assertRaises(ExitRequest) as ctx:
            run_script(shell, self.write_script("exit 4\nls\n"))
        self.assertEqual(ctx.exception.code, 4)
        self.assertNotIn("ls: args", shell.stdout.getvalue())

    def test_missing_file(self):
        """Отсутствующий файл скрипта — ошибка ScriptError."""
        missing = os.path.join(self._tmp.name, "missing.txt")
        with self.assertRaises(ScriptError):
            run_script(make_shell(), missing)

    def test_is_skipped(self):
        """Пустые строки и комментарии пропускаются."""
        self.assertTrue(is_skipped("  # note"))
        self.assertTrue(is_skipped(""))
        self.assertFalse(is_skipped("ls"))


if __name__ == "__main__":
    unittest.main()
