"""Тесты разбора параметров командной строки."""

import contextlib
import io
import unittest

from shell_emulator.config import Config, format_config, parse_args


class ParseArgsTest(unittest.TestCase):
    """Проверки функции parse_args."""

    def test_no_arguments(self):
        """Без параметров все значения не заданы."""
        self.assertEqual(parse_args([]), Config())

    def test_all_arguments(self):
        """Оба параметра читаются из командной строки."""
        config = parse_args(["--vfs", "data/vfs", "--script", "s.txt"])
        self.assertEqual(config, Config("data/vfs", "s.txt"))

    def test_unknown_argument(self):
        """Неизвестный параметр приводит к ошибке argparse."""
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["--unknown"])

    def test_missing_value(self):
        """Параметр без значения приводит к ошибке argparse."""
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["--vfs"])


class FormatConfigTest(unittest.TestCase):
    """Проверки отладочного вывода параметров."""

    def test_shows_all_parameters(self):
        """В выводе есть каждый параметр и его значение."""
        text = "\n".join(format_config(Config("v", None)))
        self.assertIn("vfs_path    = v", text)
        self.assertIn("script_path = <not set>", text)


if __name__ == "__main__":
    unittest.main()
