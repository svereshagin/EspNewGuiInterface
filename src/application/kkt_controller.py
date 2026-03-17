import os
import sys
from typing import List
from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from domain.kkt.entity import CashInfo, KktInfo
from src.network.kkt import KKTNetwork


class KKTCommand:
    def __init__(self):
        # Создаем ОДИН экземпляр сети на всё время работы
        self.KKT_NETWORK = KKTNetwork()
        self._cached_result = None

    def get_kkt_list(self) -> List[str]:
        try:
            print("🔍 KKTCommand.get_kkt_list() вызван")

            # Если есть кэш и он не пустой, возвращаем его
            if self._cached_result is not None:
                print("📦 Возвращаем кэшированные данные")
                return self._cached_result

            result = self.KKT_NETWORK.get_dkktList()
            print(f"📦 Получены данные: {result}")

            if result is None:
                print("❌ Получен None от API")
                return []

            kkt_names = []
            if hasattr(result, 'kkt') and result.kkt:
                for kkt in result.kkt:
                    kkt_name = f"{kkt.modelName} (с/н: {kkt.kktSerial})"
                    kkt_names.append(kkt_name)
                    print(f"  ✅ Добавлена: {kkt_name}")

            # Сохраняем в кэш
            self._cached_result = kkt_names
            print(f"📊 Итоговый список: {kkt_names}")
            return kkt_names

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            return []

    def clear_cache(self):
        """Очищает кэш"""
        self._cached_result = None

    def close(self):
        """Закрывает сетевые соединения"""
        self.KKT_NETWORK.close()


class KKTController(QObject):
    """
    Контроллер для управления кассами
    Связывает Python логику с QML интерфейсом
    """

    # Сигналы для обновления UI
    kktListChanged = Signal(list)  # Передаем список в сигнале
    selectedKktChanged = Signal()
    loadingChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        print("✅ KKTController инициализирован")
        self._kkt_list = []
        self._selected_kkt = ""
        self._is_loading = False
        self._kkt_command = KKTCommand()
        self._initial_load_done = False

        # Загружаем список при создании с задержкой
        QTimer.singleShot(500, self._initial_load)

    def _initial_load(self):
        """Первоначальная загрузка списка касс"""
        if not self._initial_load_done:
            print("🚀 Первоначальная загрузка списка касс")
            self.refresh_kkt_list()
            self._initial_load_done = True

    @Property(list, notify=kktListChanged)
    def kktList(self):
        """Возвращает список доступных касс"""
        current_list = self._kkt_list
        print(f"📋 kktList запрошен из QML, возвращает {len(current_list)} элементов")
        return current_list

    @Property(str, notify=selectedKktChanged)
    def selectedKkt(self):
        return self._selected_kkt

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        return self._is_loading

    @Slot()
    def refresh_kkt_list(self):
        """Обновляет список касс"""
        print("🔄 refresh_kkt_list вызван")

        if self._is_loading:
            print("⏳ Уже загружается, пропускаем")
            return

        self._is_loading = True
        self.loadingChanged.emit()

        try:
            new_kkt_list = self._kkt_command.get_kkt_list()

            # Обновляем список
            self._kkt_list = new_kkt_list

            print(f"✅ Список обновлен: {len(new_kkt_list)} элементов")
            print(f"📋 Новый список: {new_kkt_list}")

            # Отправляем сигнал с данными
            print("📢 Отправляем сигнал kktListChanged с данными")
            self.kktListChanged.emit(new_kkt_list)

            # Дополнительные сигналы для надежности
            QTimer.singleShot(100, lambda: self._emit_list_changed(new_kkt_list))
            QTimer.singleShot(200, lambda: self._emit_list_changed(new_kkt_list))

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            self._kkt_list = []
            self.kktListChanged.emit([])

        finally:
            self._is_loading = False
            self.loadingChanged.emit()

    def _emit_list_changed(self, kkt_list):
        """Вспомогательный метод для отправки сигнала"""
        print(f"📢 Повторная отправка сигнала kktListChanged, список: {kkt_list}")
        self.kktListChanged.emit(kkt_list)

    @Slot(str)
    def select_kkt(self, kkt_name: str):
        print(f"🎯 select_kkt({kkt_name})")
        if self._selected_kkt != kkt_name:
            self._selected_kkt = kkt_name
            self.selectedKktChanged.emit()
            print(f"✅ Выбрана касса: {kkt_name}")

    @Slot()
    def clear_selection(self):
        print("🧹 clear_selection()")
        self._selected_kkt = ""
        self.selectedKktChanged.emit()

    @Slot(str, result=str)
    def get_kkt_status(self, kkt_name: str) -> str:
        if kkt_name:
            return "🟢 Активна"
        return "⚪ Не выбрана"

    @Slot(result=str)
    def get_kkt_list_json(self) -> str:
        """Возвращает список касс в формате JSON"""
        import json
        return json.dumps(self._kkt_list, ensure_ascii=False)

kkt = KKTCommand().get_kkt_list()