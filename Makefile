# Makefile для проекта EspNewGuiInterface

# Основные переменные
PYTHON := uv run python -m
PYRCC := uv run pyside6-rcc
PYUIC := uv run pyside6-uic   # если понадобится конвертировать .ui в .py

# Пути
SRC_DIR := src
RESOURCES_QRC := resources.qrc
RESOURCES_PY := $(SRC_DIR)/resources_rc.py

# Основные цели
.PHONY: all run dev compiled clean resources lint help

all: resources dev

# Запуск в режиме разработки (без компиляции ресурсов)
dev:
	@echo "🔧 Запуск в dev-режиме (без скомпилированных ресурсов)"
	$(PYTHON) $(SRC_DIR).main

# Запуск с скомпилированными ресурсами
compiled: resources
	@echo "🔧 Запуск в compiled-режиме (с ресурсами из qrc)"
	$(PYTHON) $(SRC_DIR).main --compiled

# Компиляция ресурсов Qt (pyrcc6 / pyside6-rcc)
resources:
	@echo "🔨 Компилируем ресурсы Qt..."
	uv run pyside6-rcc src/resources.qrc -o src/resources_rc.py
	@echo "✅ Ресурсы скомпилированы → src/resources_rc.py"

# Очистка сгенерированных файлов
clean:
	@echo "🧹 Очистка..."
	rm -f $(RESOURCES_PY)
	rm -rf __pycache__ */__pycache__ build/ dist/ *.spec
	@echo "✅ Очистка завершена"

# Запуск с логгированием (удобно для отладки)
debug:
	@echo "🐛 Запуск с подробным выводом"
	$(PYTHON) $(SRC_DIR)/main.py --compiled 2>&1 | tee debug.log

# Показать помощь
help:
	@echo "Доступные команды:"
	@echo "  make dev       → запуск в dev-режиме (без qrc)"
	@echo "  make compiled  → запуск с скомпилированными ресурсами"
	@echo "  make resources → скомпилировать resources.qrc → resources_rc.py"
	@echo "  make all       → скомпилировать ресурсы + запустить dev"
	@echo "  make clean     → удалить сгенерированные файлы"
	@echo "  make debug     → запуск с сохранением лога в debug.log"
