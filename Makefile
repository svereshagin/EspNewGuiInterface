# Makefile для Linux

# Основные переменные
PYTHON := uv run python
PYINSTALLER := uv run pyinstaller

# Пути
SRC_DIR := src
UI_DIR := $(SRC_DIR)/ui
DIST_NAME := ТС-ПИоТ

.PHONY: all build clean run dev

# Запуск в режиме разработки
dev:
	@echo "🔧 Запуск в dev-режиме"
	cd $(SRC_DIR) && $(PYTHON) main.py

# Сборка для Linux
build:
	@echo "📦 Сборка приложения для Linux..."

	# Создаем spec файл для лучшего контроля
	$(PYINSTALLER) --onefile \
		--name $(DIST_NAME) \
		--add-data "$(SRC_DIR)/infrastructure:infrastructure" \
		--add-data "$(SRC_DIR)/ui:ui" \
		--add-data "$(SRC_DIR)/main.py:." \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths $(SRC_DIR) \
		--workpath build \
		--distpath dist \
		--specpath . \
		$(SRC_DIR)/main.py

	@echo "✅ Сборка завершена!"
	@echo "📁 Исполняемый файл: dist/$(DIST_NAME)"
	@ls -la dist/

# Альтернативная сборка с явным указанием всех модулей
build-verbose:
	@echo "📦 Сборка с подробным выводом..."
	$(PYINSTALLER) --onefile \
		--name $(DIST_NAME) \
		--add-data "$(SRC_DIR):." \
		--hidden-import PySide6 \
		--hidden-import infrastructure.utils.common \
		--hidden-import infrastructure.utils.qml_loader \
		--collect-all PySide6 \
		--log-level DEBUG \
		$(SRC_DIR)/main.py 2>&1 | tee build.log
	@echo "✅ Сборка завершена!"

# Очистка
clean:
	@echo "🧹 Очистка..."
	rm -rf build dist *.spec
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Очистка завершена"

# Запуск собранного приложения с отладкой
run:
	@echo "🚀 Запуск собранного приложения..."
	@if [ -f dist/$(DIST_NAME) ]; then \
		cd dist && ./$(DIST_NAME) 2>&1; \
	else \
		echo "❌ Файл не найден. Сначала выполните сборку: make build"; \
	fi

# Запуск с отладкой
run-debug:
	@echo "🐛 Запуск с отладкой..."
	@if [ -f dist/$(DIST_NAME) ]; then \
		cd dist && strace -e openat ./$(DIST_NAME) 2>&1 | grep -E "(openat|ENOENT)"; \
	else \
		echo "❌ Файл не найден. Сначала выполните сборку: make build"; \
	fi

# Полная пересборка
rebuild: clean build

help:
	@echo "Доступные команды:"
	@echo "  make dev          - запуск в режиме разработки"
	@echo "  make build        - сборка приложения"
	@echo "  make build-verbose - сборка с подробным выводом"
	@echo "  make run          - запуск собранного приложения"
	@echo "  make run-debug    - запуск с трассировкой открытия файлов"
	@echo "  make clean        - очистка"
	@echo "  make rebuild      - полная пересборка"