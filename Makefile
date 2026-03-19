# Makefile для проекта EspNewGuiInterface

# Основные переменные
PYTHON := uv run python -m
PYRCC := uv run pyside6-rcc
PYUIC := uv run pyside6-uic
PYINSTALLER := uv run pyinstaller

# Пути
SRC_DIR := src
RESOURCES_QRC := resources.qrc
RESOURCES_PY := $(SRC_DIR)/resources_rc.py
DIST_NAME := "ТС-ПИоТ"
SPEC_FILE := $(DIST_NAME).spec

# Основные цели
.PHONY: all run dev compiled resources clean lint help build build-onefile build-debug run-build

all: resources dev

# Запуск в режиме разработки (без компиляции ресурсов)
dev:
	@echo "🔧 Запуск в dev-режиме (без скомпилированных ресурсов)"
	$(PYTHON) $(SRC_DIR).main

# Запуск с скомпилированными ресурсами
compiled: resources
	@echo "🔧 Запуск в compiled-режиме (с ресурсами из qrc)"
	$(PYTHON) $(SRC_DIR).main --compiled

# Компиляция ресурсов Qt (pyside6-rcc)
resources:
	@echo "🔨 Компилируем ресурсы Qt..."
	uv run pyside6-rcc src/resources.qrc -o src/resources_rc.py
	@echo "✅ Ресурсы скомпилированы → src/resources_rc.py"

# Очистка сгенерированных файлов
clean:
	@echo "🧹 Очистка..."
	rm -f $(RESOURCES_PY)
	rm -rf __pycache__ */__pycache__ build/ dist/ *.spec debug.log
	@echo "✅ Очистка завершена"

# Запуск с логгированием (удобно для отладки)
debug:
	@echo "🐛 Запуск с подробным выводом"
	$(PYTHON) $(SRC_DIR)/main.py --compiled 2>&1 | tee debug.log

# ==================== ЦЕЛИ ДЛЯ PYINSTALLER ====================

# Сборка onefile исполняемого файла
build-onefile: resources
	@echo "📦 Сборка onefile исполняемого файла..."
	$(PYINSTALLER) --onefile --windowed \
		--name $(DIST_NAME) \
		--add-data "$(SRC_DIR):$(SRC_DIR)" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		$(SRC_DIR)/main.py
	@echo "✅ Сборка завершена! Исполняемый файл в dist/$(DIST_NAME).exe"

# Сборка в режиме с папкой (быстрее, удобно для отладки)
build-dir: resources
	@echo "📦 Сборка в режиме папки (для отладки)..."
	$(PYINSTALLER) --windowed \
		--name $(DIST_NAME) \
		--add-data "$(SRC_DIR):$(SRC_DIR)" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		$(SRC_DIR)/main.py
	@echo "✅ Сборка завершена! Папка с файлами в dist/$(DIST_NAME)/"

# Сборка с созданием spec файла для последующей настройки
build-spec: resources
	@echo "📝 Создание spec файла для кастомной сборки..."
	$(PYINSTALLER) --onefile --windowed \
		--name $(DIST_NAME) \
		--add-data "$(SRC_DIR):$(SRC_DIR)" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		--specpath . \
		$(SRC_DIR)/main.py
	@echo "✅ Spec файл создан: $(SPEC_FILE)"
	@echo "📝 Для кастомной сборки отредактируйте $(SPEC_FILE) и запустите:"
	@echo "    $(PYINSTALLER) $(SPEC_FILE)"

# Сборка с иконкой (если есть файл иконки)
build-with-icon: resources
	@echo "📦 Сборка с иконкой..."
	$(PYINSTALLER) --onefile --windowed \
		--name $(DIST_NAME) \
		--icon "$(SRC_DIR)/ui/assets/icon.ico" \
		--add-data "$(SRC_DIR):$(SRC_DIR)" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		$(SRC_DIR)/main.py
	@echo "✅ Сборка с иконкой завершена!"

# Запуск собранного приложения (onefile версии)
run-build:
	@echo "🚀 Запуск собранного приложения..."
	./dist/$(DIST_NAME).exe

# Запуск собранного приложения (папка версии)
run-build-dir:
	@echo "🚀 Запуск собранного приложения из папки..."
	./dist/$(DIST_NAME)/$(DIST_NAME).exe

# Полная пересборка и запуск
build-and-run: clean build-onefile run-build
	@echo "✅ Сборка и запуск выполнены"

# Сборка с дополнительной отладочной информацией
build-debug: resources
	@echo "🔧 Сборка с отладочной информацией..."
	$(PYINSTALLER) --onefile --windowed \
		--name $(DIST_NAME)-debug \
		--add-data "$(SRC_DIR):$(SRC_DIR)" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		--log-level DEBUG \
		$(SRC_DIR)/main.py
	@echo "✅ Отладочная сборка завершена!"

# Проверка зависимостей перед сборкой
check-deps:
	@echo "🔍 Проверка зависимостей..."
	uv pip list | grep PyInstaller || echo "⚠️ PyInstaller не установлен! Установите: uv pip install pyinstaller"
	uv pip list | grep PySide6 || echo "⚠️ PySide6 не установлен!"

# Показать помощь
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "=== РЕЖИМЫ ЗАПУСКА ==="
	@echo "  make dev          → запуск в dev-режиме (без qrc)"
	@echo "  make compiled     → запуск с скомпилированными ресурсами"
	@echo "  make debug        → запуск с сохранением лога в debug.log"
	@echo ""
	@echo "=== РЕСУРСЫ ==="
	@echo "  make resources    → скомпилировать resources.qrc → resources_rc.py"
	@echo "  make all          → скомпилировать ресурсы + запустить dev"
	@echo "  make clean        → удалить сгенерированные файлы"
	@echo ""
	@echo "=== СБОРКА PYINSTALLER ==="
	@echo "  make build-onefile    → сборка одного exe файла"
	@echo "  make build-dir        → сборка в папку (для отладки)"
	@echo "  make build-spec       → создать spec файл для кастомной настройки"
	@echo "  make build-with-icon  → сборка с иконкой (если есть icon.ico)"
	@echo "  make build-debug      → сборка с отладочной информацией"
	@echo "  make check-deps       → проверить зависимости для сборки"
	@echo ""
	@echo "=== ЗАПУСК СОБРАННОГО ==="
	@echo "  make run-build        → запустить собранный .exe"
	@echo "  make run-build-dir    → запустить из папки"
	@echo "  make build-and-run    → пересобрать и сразу запустить"