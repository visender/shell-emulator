"""Параметры запуска эмулятора из командной строки."""

import argparse
from dataclasses import dataclass, fields

NOT_SET = "<not set>"


@dataclass(frozen=True)
class Config:
    """Настройки эмулятора.

    :ivar vfs_path: путь к физическому расположению VFS
    :ivar script_path: путь к стартовому скрипту
    """

    vfs_path: str = None
    script_path: str = None


def build_arg_parser():
    """Создать парсер параметров командной строки."""
    parser = argparse.ArgumentParser(
        prog="shell-emulator",
        description="Эмулятор командной оболочки UNIX-подобной ОС.",
    )
    parser.add_argument(
        "--vfs",
        dest="vfs_path",
        metavar="PATH",
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        dest="script_path",
        metavar="PATH",
        help="путь к стартовому скрипту с командами эмулятора",
    )
    return parser


def parse_args(argv=None):
    """Разобрать параметры командной строки.

    :param argv: список аргументов; ``None`` — взять из ``sys.argv``
    :return: объект :class:`Config`
    """
    namespace = build_arg_parser().parse_args(argv)
    return Config(
        vfs_path=namespace.vfs_path,
        script_path=namespace.script_path,
    )


def format_config(config):
    """Сформировать отладочный вывод параметров в виде строк.

    :param config: объект :class:`Config`
    :return: список строк ``ключ = значение``
    """
    names = [field.name for field in fields(config)]
    width = max(len(name) for name in names)
    lines = ["[debug] emulator parameters:"]
    for name in names:
        value = getattr(config, name)
        shown = NOT_SET if value is None else value
        lines.append(f"[debug]   {name.ljust(width)} = {shown}")
    return lines
