# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('PySide6')


a = Analysis(
    ['src\\main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=['ui.resources_rc', 'PySide6.QtQml', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtQuick', 'PySide6.QtQuickWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
