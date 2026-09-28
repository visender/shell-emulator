"""Тесты REPL и встроенных команд."""

import io
import unittest

from shell_emulator.commands import (
    CommandError,
    ExitRequest,
    cmd_cd,
    cmd_exit,
    cmd_ls,
)
from shell_emulator.shell import Shell


def make_shell(user_input=""):
    """Создать оболочку с подменёнными потоками ввода-вывода."""
    return Shell(
        stdin=io.StringIO(user_input),
        stdout=io.StringIO(),
        stderr=io.StringIO(),
    )


class StubCommandsTest(unittest.TestCase):
    """Проверки команд-заглушек и exit."""

    def test_ls_prints_name_and_args(self):
        """ls выводит своё имя и аргументы."""
        self.assertEqual(cmd_ls(["-l", "a b"]), "ls: args=['-l', 'a b']")

    def test_cd_prints_name_and_args(self):
        """cd выводит своё имя и аргументы."""
        self.assertEqual(cmd_cd(["/tmp"]), "cd: args=['/tmp']")

    def test_cd_too_many_args(self):
        """cd с двумя аргументами — ошибка."""
        with self.assertRaises(CommandError):
            cmd_cd(["a", "b"])

    def test_exit_default_code(self):
        """exit без аргументов завершает с кодом 0."""
        with self.assertRaises(ExitRequest) as ctx:
            cmd_exit([])
        self.assertEqual(ctx.exception.code, 0)

    def test_exit_with_code(self):
        """exit N завершает с кодом N."""
        with self.assertRaises(ExitRequest) as ctx:
            cmd_exit(["3"])
        self.assertEqual(ctx.exception.code, 3)

    def test_exit_non_numeric(self):
        """exit с нечисловым аргументом — ошибка."""
        with self.assertRaises(CommandError):
            cmd_exit(["abc"])

    def test_exit_too_many_args(self):
        """exit с двумя аргументами — ошибка."""
        with self.assertRaises(CommandError):
            cmd_exit(["1", "2"])


class ShellTest(unittest.TestCase):
    """Проверки класса Shell."""

    def test_prompt_format(self):
        """Приглашение имеет вид user@host:~$."""
        shell = make_shell()
        expected = f"{shell.username}@{shell.hostname}:~$ "
        self.assertEqual(shell.prompt(), expected)

    def test_unknown_command(self):
        """Неизвестная команда даёт ошибку и код 127."""
        shell = make_shell()
        self.assertEqual(shell.execute("foo bar"), 127)
        self.assertIn("foo: command not found", shell.stderr.getvalue())

    def test_syntax_error(self):
        """Незакрытая кавычка даёт синтаксическую ошибку."""
        shell = make_shell()
        self.assertEqual(shell.execute('ls "abc'), 2)
        self.assertIn("syntax error", shell.stderr.getvalue())

    def test_command_output(self):
        """Вывод команды попадает в stdout."""
        shell = make_shell()
        self.assertEqual(shell.execute('ls "my dir"'), 0)
        self.assertEqual(shell.stdout.getvalue(), "ls: args=['my dir']\n")

    def test_run_until_exit(self):
        """REPL выполняет команды до exit и возвращает его код."""
        shell = make_shell("ls\nexit 5\nls\n")
        self.assertEqual(shell.run(), 5)
        self.assertEqual(shell.stdout.getvalue().count("ls: args="), 1)

    def test_run_ignores_bom_and_crlf(self):
        """BOM в начале ввода и окончания строк CRLF игнорируются."""
        shell = make_shell("﻿ls\r\n")
        shell.run()
        self.assertEqual(shell.stdout.getvalue().count("ls: args=[]"), 1)

    def test_run_until_eof(self):
        """REPL завершается при конце ввода."""
        shell = make_shell("cd /\n")
        self.assertEqual(shell.run(), 0)


if __name__ == "__main__":
    unittest.main()
