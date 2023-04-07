# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['QRdetector1.py'],
    pathex=[],
    binaries=[],
    datas=[('libiconv.dll', '.'), ('libzbar-64.dll', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QR식권처리기 v1.0',
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
    version='C:\\Users\\user\\AppData\\Local\\Temp\\7be48831-ddc6-4d28-9c43-68dbab0edf25',
    icon=['qr.ico'],
)
