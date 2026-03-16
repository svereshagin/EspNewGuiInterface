import json
import os
import platform
from pathlib import Path
from typing import Optional, Dict, Any
from singleton_decorator import singleton
from dataclasses import dataclass



@dataclass(frozen=True)
class ApiSettings:
    timeout = 30
    tspiot_port: int = 51401
    orchestrator_port: int = 51077
    orchestrator_url: str = "http://127.0.0.1:"+str(orchestrator_port)




@singleton
class Settings:
    """
    Класс для управления всеми настройками приложения
    """

    def __init__(self):
        """Приватный конструктор (синглтон гарантирует единственный экземпляр)"""
        self._config_dir: str = self._get_config_dir()
        self._config_file: str = os.path.join(self._config_dir, "gui_settings.json")
        self._log_properties_file: str = os.path.join(self._config_dir, "gui_log.properties")
        self._log_dir: str = os.path.join(self._config_dir, "log")
        self._log_file: str = os.path.join(self._log_dir, "gui.log")


    def _get_config_dir(self) -> str:
        """
        Возвращает базовую директорию конфигурации в зависимости от ОС.
        """
        system = platform.system()
        home = str(Path.home())

        if system == "Linux":
            # Linux: ~/.esp/esm/esm-gui/
            return os.path.join(home, ".esp", "esm", "esm-gui")

        elif system == "Windows":
            # Windows: C:\ProgramData\esp\esm\esm-gui\
            program_data = os.environ.get('PROGRAMDATA', 'C:\\ProgramData')
            return os.path.join(program_data, "esp", "esm", "esm-gui")

        elif system == "Darwin":

            return os.path.join(home, ".esp", "esm-gui")

        else:
            raise RuntimeError(f"Неподдерживаемая ОС: {system}")

    # ===== Базовые геттеры путей =====

    def get_config_dir(self) -> str:
        """Возвращает путь к директории конфигурации"""
        return self._config_dir

    def get_settings_file(self) -> str:
        """Возвращает путь к файлу настроек"""
        return self._config_file

    def get_log_properties_file(self) -> str:
        """Возвращает путь к файлу конфигурации логирования"""
        return self._log_properties_file

    def get_log_dir(self) -> str:
        """Возвращает путь к директории логов"""
        return self._log_dir

    def get_log_file(self) -> str:
        """Возвращает путь к файлу лога"""
        return self._log_file

    # ===== Создание директорий и файлов =====

    def create_directories(self) -> None:
        """
        Создает все необходимые директории и файлы.
        """
        # Создаем основную директорию конфигурации
        os.makedirs(self._config_dir, exist_ok=True)

        # Создаем директорию для логов
        os.makedirs(self._log_dir, exist_ok=True)

        # Создаем файл конфигурации логирования, если его нет
        if not os.path.exists(self._log_properties_file):
            self._create_default_log_properties()

        # Создаем файл настроек, если его нет
        if not os.path.exists(self._config_file):
            self.create_default_config()

    def _create_default_log_properties(self) -> None:
        """
        Создает файл конфигурации логирования по умолчанию.
        """
        config_data = (
            "log4cpp.rootCategory=ERROR\n"
            "log4cpp.category.GUI=DEBUG, gui_file\n"
            "log4cpp.additivity.GUI=false\n"
            "\n"
            "log4cpp.appender.gui_file=DailyRollingFileAppender\n"
            f"log4cpp.appender.gui_file.fileName={self._log_file}\n"
            "log4cpp.appender.gui_file.maxDaysKeep=14\n"
            "log4cpp.appender.gui_file.layout=PatternLayout\n"
            "log4cpp.appender.gui_file.layout.ConversionPattern=%d{%Y.%m.%d %H:%M:%S.%l} %t %-5p [%c] %m%n\n"
        )

        with open(self._log_properties_file, 'w', encoding='utf-8') as f:
            f.write(config_data)

    # ===== Работа с JSON =====

    def _read_json(self, file_path: str) -> Dict[str, Any]:
        """
        Читает и парсит JSON файл.
        """
        if not os.path.exists(file_path):
            raise RuntimeError(f"Файл настроек не существует: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise RuntimeError("Неверный формат JSON: ожидается объект")

            return data

        except json.JSONDecodeError:
            raise RuntimeError("Ошибка парсинга JSON файла")
        except Exception as e:
            raise RuntimeError(f"Ошибка чтения файла настроек: {e}")

    def _save_json(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет JSON объект в файл настроек.
        """
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения файла настроек: {e}")

    # ===== Настройки по умолчанию =====

    def create_default_config(self) -> None:
        """
        Создает файл настроек со значениями по умолчанию.
        """
        default_config = {
            "port": 51077  # Порт оркестратора по умолчанию
        }

        self._save_json(default_config)

    def reset_to_defaults(self) -> None:
        """Сбрасывает настройки к значениям по умолчанию"""
        self._orchestrator_port = 51077
        self.save_config()

    # ===== Сохранение и загрузка =====

    def save_config(self) -> None:
        """
        Сохраняет текущие настройки в файл.
        """
        config = {
            "port": self._orchestrator_port
        }

        self._save_json(config)

    def load_config(self) -> None:
        """
        Загружает настройки из файла.
        """
        data = self._read_json(self._config_file)

        if "port" in data:
            self._orchestrator_port = int(data["port"])
        else:
            raise RuntimeError("Неверный формат файла настроек: отсутствует поле 'port'")

    # ===== Полная инициализация =====

    def initialize(self) -> bool:
        """
        Выполняет полную инициализацию: создает директории и загружает настройки.

        Returns:
            bool: True если инициализация успешна, False в случае ошибки
        """
        try:
            self.create_directories()
            self.load_config()
            print(f"✅ Настройки загружены: порт {self._orchestrator_port}")
            return True
        except Exception as e:
            print(f"❌ Ошибка инициализации настроек: {e}")
            return False

    # ===== Геттеры и сеттеры =====

    def get_host(self) -> str:
        """Возвращает хост (всегда localhost)"""
        return "127.0.0.1"

    def get_port(self) -> int:
        """Возвращает порт оркестратора"""
        return self._orchestrator_port

    def set_port(self, port: int) -> None:
        """Устанавливает порт оркестратора"""
        if not isinstance(port, int) or port <= 0 or port > 65535:
            raise ValueError(f"Некорректный порт: {port}. Допустимые значения: 1-65535")

        self._orchestrator_port = port
        print(f"🔧 Порт изменён на: {port}")

    def get_orchestrator_url(self) -> str:
        """Возвращает полный URL оркестратора"""
        return f"http://{self.get_host()}:{self.get_port()}"