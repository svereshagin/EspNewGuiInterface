#!/bin/bash

echo "📦 Сборка приложения"

# Очистка
rm -rf build dist

# Сборка
uv run pyinstaller --onefile \
    --name "ТС-ПИоТ" \
    --add-data "src/ui:ui" \
    --hidden-import PySide6.QtQml \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtQuick \
    --hidden-import PySide6.QtQuickWidgets \
    --collect-data PySide6 \
    src/main.py

echo ""
echo "✅ Готово!"
echo "📁 Исполняемый файл: dist/ТС-ПИоТ"
echo "📁 Ресурсы: dist/ui/"
echo ""
echo "🚀 Запуск: ./dist/ТС-ПИоТ"