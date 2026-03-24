# Makefile для проекта EspNewGuiInterface

# Основные переменные
PYTHON := uv run python -m
PYRCC := uv run pyside6-rcc
PYINSTALLER := uv run pyinstaller

# Пути
SRC_DIR := src
UI_DIR := $(SRC_DIR)/ui
DIST_NAME := "ТС-ПИоТ"

.PHONY: all build clean run

# Запуск в режиме разработки
dev:
	@echo "🔧 Запуск в dev-режиме"
	$(PYTHON) $(SRC_DIR).main

# Сборка для Linux (все ресурсы копируются рядом с .exe)
build:
	@echo "📦 Сборка приложения для Linux..."

	# Компилируем ресурсы Qt (если нужно)
	@echo "🔨 Компилируем ресурсы Qt..."
	@mkdir -p $(UI_DIR)
	@uv run pyside6-rcc $(UI_DIR)/resources.qrc -o $(UI_DIR)/resources_rc.py 2>/dev/null || true

	# Сборка с PyInstaller
	$(PYINSTALLER) --onefile \
		--name $(DIST_NAME) \
		--add-data "$(UI_DIR):ui" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		$(SRC_DIR)/main.py

	@echo "✅ Сборка завершена!"
	@echo "📁 Исполняемый файл: dist/$(DIST_NAME)"
	@echo "📁 Ресурсы: dist/ui/"

# Очистка
clean:
	@echo "🧹 Очистка..."
	rm -rf build dist *.spec
	rm -f $(UI_DIR)/resources_rc.py
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Очистка завершена"

# Запуск собранного приложения
run:
	@echo "🚀 Запуск собранного приложения..."
	./dist/$(DIST_NAME)

# Полная пересборка и запуск
all: clean build run

help:
	@echo "Доступные команды:"
	@echo "  make dev    - запуск в режиме разработки"
	@echo "  make build  - сборка приложения"
	@echo "  make run    - запуск собранного приложения"
	@echo "  make clean  - очистка"
	@echo "  make all    - полная пересборка и запуск"