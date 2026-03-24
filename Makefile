# Makefile для проекта ТС-ПИоТ

# Основные переменные
PYTHON := uv run python -m
PYRCC := uv run pyside6-rcc
PYINSTALLER := uv run pyinstaller

# Пути
SRC_DIR := src
DIST_NAME := "ТС-ПИоТ"

# Основные цели
.PHONY: all dev compiled compile-resources clean check-deps help \
        build-linux build-linux-new \
        build-windows build-windows-debug \
        run-windows run-windows-debug

all: compile-resources dev

# ==================== РЕЖИМЫ ЗАПУСКА ====================

# Запуск в режиме разработки (без компиляции ресурсов)
dev:
	@echo "Запуск в dev-режиме (без скомпилированных ресурсов)"
	$(PYTHON) $(SRC_DIR).main

# Запуск с скомпилированными ресурсами
compiled: compile-resources
	@echo "🔧 Запуск в compiled-режиме (с ресурсами из qrc)"
	$(PYTHON) $(SRC_DIR).main --compiled

# ==================== РЕСУРСЫ ====================

# Компиляция ресурсов Qt (pyside6-rcc)
compile-resources:
	@echo "🔨 Компилируем ресурсы Qt..."
	uv run pyside6-rcc src/ui/resources.qrc -o src/ui/resources_rc.py
	@echo "✅ Ресурсы скомпилированы → src/ui/resources_rc.py"

# ==================== СБОРКА ====================

# Старый билд на Linux (без resources_rc, файлы с диска)
build-linux:
	@echo "📦 Сборка для Linux (старый способ, файлы с диска)..."
	uv run pyinstaller --onefile \
		--name $(DIST_NAME) \
		--add-data "src:src" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		src/main.py
	@echo "✅ Готово: dist/ТС-ПИоТ"

# Новый билд на Linux (с resources_rc, всё зашито)
build-linux-new: compile-resources
	@echo "📦 Сборка для Linux (с resources_rc)..."
	uv run pyinstaller --onefile \
		--name $(DIST_NAME) \
		--hidden-import ui.resources_rc \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		src/main.py
	@echo "✅ Готово: dist/ТС-ПИоТ"

# Билд на Windows (с resources_rc, без консоли)
build-windows: compile-resources
	@echo "📦 Сборка для Windows..."
	pyinstaller --onefile --windowed \
		--name $(DIST_NAME) \
		--hidden-import ui.resources_rc \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		src/main.py
	@echo "✅ Готово: dist/ТС-ПИоТ.exe"

# Билд на Windows с консолью (для отладки)
build-windows-debug: compile-resources
	@echo "📦 Сборка для Windows (debug, с консолью)..."
	pyinstaller --onefile \
		--name $(DIST_NAME)-debug \
		--hidden-import ui.resources_rc \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		--hidden-import PySide6.QtQuick \
		--hidden-import PySide6.QtQuickWidgets \
		--collect-data PySide6 \
		--paths . \
		src/main.py
	@echo "✅ Готово: dist/ТС-ПИоТ-debug.exe"

# ==================== ЗАПУСК СОБРАННОГО ====================

run-windows:
	@echo "🚀 Запуск..."
	.\dist\ТС-ПИоТ.exe

run-windows-debug:
	@echo "🚀 Запуск debug..."
	.\dist\ТС-ПИоТ-debug.exe

# ==================== УТИЛИТЫ ====================

# Очистка сгенерированных файлов
clean:
	@echo "🧹 Очистка..."
	rm -rf __pycache__ */__pycache__ build/ dist/ *.spec debug.log
	@echo "✅ Очистка завершена"

# Проверка зависимостей
check-deps:
	@echo "🔍 Проверка зависимостей..."
	uv pip list | grep PyInstaller || echo "⚠️  PyInstaller не установлен!"
	uv pip list | grep PySide6 || echo "⚠️  PySide6 не установлен!"

# Помощь
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "=== РЕЖИМЫ ЗАПУСКА ==="
	@echo "  make dev                → запуск в dev-режиме (без qrc, файлы с диска)"
	@echo "  make compiled           → запуск с скомпилированными ресурсами (qrc)"
	@echo ""
	@echo "=== РЕСУРСЫ ==="
	@echo "  make compile-resources  → скомпилировать resources.qrc → resources_rc.py"
	@echo "  make clean              → удалить build/, dist/, *.spec и кэши"
	@echo ""
	@echo "=== СБОРКА ==="
	@echo "  make build-linux        → Linux, старый способ (файлы src/ рядом с бинарём)"
	@echo "  make build-linux-new    → Linux, новый способ (ресурсы зашиты в бинарь)"
	@echo "  make build-windows      → Windows .exe без консоли (продакшн)"
	@echo "  make build-windows-debug → Windows .exe с консолью (для отладки)"
	@echo ""
	@echo "=== ЗАПУСК СОБРАННОГО (Windows) ==="
	@echo "  make run-windows        → запустить dist/ТС-ПИоТ.exe"
	@echo "  make run-windows-debug  → запустить dist/ТС-ПИоТ-debug.exe"
	@echo ""
	@echo "=== УТИЛИТЫ ==="
	@echo "  make check-deps         → проверить наличие PyInstaller и PySide6"