"""Точка входа: ``python -m shell_emulator [--vfs PATH] [--script PATH]``."""

import sys

from shell_emulator.commands import ExitRequest
from shell_emulator.config import format_config, parse_args
from shell_emulator.script import ScriptError, run_script
from shell_emulator.shell import EXIT_FAILURE, Shell


def main(argv=None):
    """Запустить эмулятор.

    Выводит заданные параметры, выполняет стартовый скрипт (если он
    указан) и переходит в интерактивный режим.

    :param argv: аргументы командной строки без имени программы
    :return: код завершения процесса
    """
    config = parse_args(argv)
    shell = Shell()
    for line in format_config(config):
        shell.stdout.write(line + "\n")
    shell.stdout.flush()
    if config.script_path:
        try:
            run_script(shell, config.script_path)
        except ScriptError as error:
            shell.report(f"shell-emulator: cannot run script: {error}")
            return EXIT_FAILURE
        except ExitRequest as request:
            return request.code
    return shell.run()


if __name__ == "__main__":
    sys.exit(main())
