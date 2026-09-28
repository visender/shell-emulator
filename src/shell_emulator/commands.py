"""Встроенные команды эмулятора."""

EXIT_SUCCESS = 0
EXIT_USAGE_ERROR = 2
MAX_CD_ARGS = 1
MAX_EXIT_ARGS = 1


class CommandError(Exception):
    """Ошибка выполнения команды: неверные аргументы и т.п."""


class ExitRequest(Exception):
    """Запрос на завершение работы эмулятора."""

    def __init__(self, code):
        """Сохранить код возврата ``code``."""
        super().__init__(code)
        self.code = code


def _format_stub(name, args):
    """Сформировать вывод команды-заглушки: имя и аргументы."""
    return f"{name}: args={args!r}"


def cmd_ls(args):
    """Заглушка ``ls``: выводит своё имя и аргументы."""
    return _format_stub("ls", args)


def cmd_cd(args):
    """Заглушка ``cd``: выводит своё имя и аргументы.

    :raises CommandError: если передано больше одного аргумента
    """
    if len(args) > MAX_CD_ARGS:
        raise CommandError("cd: too many arguments")
    return _format_stub("cd", args)


def cmd_exit(args):
    """Завершить работу эмулятора: ``exit [код]``.

    :raises CommandError: если аргументов больше одного или код
        не является целым числом
    :raises ExitRequest: всегда при корректных аргументах
    """
    if len(args) > MAX_EXIT_ARGS:
        raise CommandError("exit: too many arguments")
    if not args:
        raise ExitRequest(EXIT_SUCCESS)
    try:
        code = int(args[0])
    except ValueError:
        raise CommandError(
            f"exit: {args[0]}: numeric argument required"
        ) from None
    raise ExitRequest(code)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}
