"""Цикл REPL (read-eval-print loop) эмулятора."""

import getpass
import socket
import sys

from shell_emulator.commands import (
    COMMANDS,
    EXIT_SUCCESS,
    EXIT_USAGE_ERROR,
    CommandError,
    ExitRequest,
)
from shell_emulator.parser import ParseError, parse_command

EXIT_NOT_FOUND = 127
EXIT_FAILURE = 1
HOME_DIR = "~"
BOM = "﻿"


def get_username():
    """Вернуть имя текущего пользователя ОС."""
    try:
        return getpass.getuser()
    except OSError:
        return "user"


def get_hostname():
    """Вернуть короткое имя компьютера."""
    return socket.gethostname().split(".")[0]


class Shell:
    """Интерактивная оболочка с приглашением ``user@host:dir$``."""

    def __init__(self, stdin=None, stdout=None, stderr=None):
        """Создать оболочку, работающую с указанными потоками.

        По умолчанию используются стандартные потоки процесса.
        """
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.username = get_username()
        self.hostname = get_hostname()
        self.cwd = HOME_DIR
        self.last_status = EXIT_SUCCESS

    def prompt(self):
        """Вернуть строку приглашения, например ``user@pc:~$ ``."""
        return f"{self.username}@{self.hostname}:{self.cwd}$ "

    def execute(self, line):
        """Выполнить одну строку и вернуть код возврата.

        :raises ExitRequest: если выполнена команда ``exit``
        """
        try:
            parsed = parse_command(line)
        except ParseError as error:
            return self._fail(f"syntax error: {error}", EXIT_USAGE_ERROR)
        if parsed is None:
            return self.last_status
        name, args = parsed
        handler = COMMANDS.get(name)
        if handler is None:
            return self._fail(f"{name}: command not found", EXIT_NOT_FOUND)
        try:
            output = handler(args)
        except CommandError as error:
            return self._fail(str(error), EXIT_FAILURE)
        self._write(output)
        self.last_status = EXIT_SUCCESS
        return self.last_status

    def run(self):
        """Запустить интерактивный цикл и вернуть код завершения."""
        while True:
            line = self._read_line()
            if line is None:
                return self.last_status
            try:
                self.execute(line)
            except ExitRequest as request:
                return request.code

    def _read_line(self):
        """Вывести приглашение и прочитать строку; ``None`` при EOF."""
        self.stdout.write(self.prompt())
        self.stdout.flush()
        try:
            line = self.stdin.readline()
        except KeyboardInterrupt:
            self.stdout.write("\n")
            return ""
        if not line:
            self.stdout.write("\n")
            return None
        return line.rstrip("\r\n").lstrip(BOM)

    def echo_input(self, line):
        """Вывести приглашение и строку, будто её ввёл пользователь."""
        self._write(self.prompt() + line)

    def report(self, message):
        """Вывести сообщение об ошибке в поток ошибок."""
        self.stderr.write(f"{message}\n")
        self.stderr.flush()

    def _write(self, text):
        """Вывести результат команды, если он не пустой."""
        if text:
            self.stdout.write(text + "\n")
            self.stdout.flush()

    def _fail(self, message, status):
        """Сообщить об ошибке и запомнить код возврата."""
        self.report(message)
        self.last_status = status
        return status
