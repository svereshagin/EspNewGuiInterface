# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['src'],  # Важно: добавляем src в путь поиска
    binaries=[],
    datas=[
        ('src/infrastructure', 'infrastructure'),  # Копируем infrastructure
        ('src/ui', 'ui'),                         # Копируем ui
    ],
    hiddenimports=[
        'PySide6.QtQml',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtQuick',
        'PySide6.QtQuickWidgets',
        'infrastructure.utils.common',
        'infrastructure.utils.qml_loader',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ТС-ПИоТ',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Ставим True для отладки, потом можно сменить на False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)