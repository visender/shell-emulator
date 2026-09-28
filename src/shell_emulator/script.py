"""Выполнение стартового скрипта эмулятора."""

from shell_emulator.commands import EXIT_SUCCESS

COMMENT_PREFIX = "#"


class ScriptError(Exception):
    """Стартовый скрипт не удалось прочитать."""


def read_script(path):
    """Прочитать строки скрипта из файла в кодировке UTF-8.

    :param path: путь к файлу скрипта
    :return: список строк без символов перевода строки
    :raises ScriptError: если файл не найден или не читается
    """
    try:
        with open(path, encoding="utf-8-sig") as file:
            return file.read().splitlines()
    except OSError as error:
        raise ScriptError(f"{path}: {error.strerror}") from None
    except UnicodeDecodeError:
        raise ScriptError(f"{path}: not a UTF-8 text file") from None


def is_skipped(line):
    """Проверить, что строка пустая или является комментарием."""
    stripped = line.strip()
    return not stripped or stripped.startswith(COMMENT_PREFIX)


def run_script(shell, path):
    """Выполнить команды скрипта по очереди в оболочке ``shell``.

    Каждая команда выводится после приглашения, как если бы её ввёл
    пользователь. Ошибочные строки пропускаются с сообщением о номере
    строки, выполнение продолжается.

    :param shell: объект :class:`~shell_emulator.shell.Shell`
    :param path: путь к файлу скрипта
    :return: количество строк, завершившихся ошибкой
    :raises ScriptError: если файл скрипта не читается
    :raises ExitRequest: если в скрипте выполнена команда ``exit``
    """
    failed = 0
    for number, line in enumerate(read_script(path), start=1):
        if is_skipped(line):
            continue
        shell.echo_input(line)
        status = shell.execute(line)
        if status != EXIT_SUCCESS:
            failed += 1
            shell.report(
                f"{path}:{number}: line skipped (exit status {status})"
            )
    return failed
