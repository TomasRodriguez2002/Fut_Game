# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['selectMain.py'],
    pathex=[],
    binaries=[],
    datas=[('Botones/botones de seleccion/*.jpg', 'Botones'), ('Botones/botones normales/*.jpg', 'Botones'), ('Fondos de pantalla/*.jpg', 'Fondos de pantalla'), ('Fondos de pantalla/*.png', 'Fondos de pantalla'), ('Strategies/*.py', 'Strategies'), ('players/*.py', 'players'), ('Sounds/*.wav', 'Sounds'), ('Sprites/*.png', 'Sprites'), ('Botones', 'Botones'), ('pelotaicon.ico', '.'), ('pelotaicon.png', '.'), ('ball.py', '.'), ('boton.py', '.'), ('constantes.py', '.'), ('cursor.py', '.'), ('game.py', '.'), ('mediator.py', '.'), ('README.md', '.')],
    hiddenimports=['hmac'],
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
    name='selectMain',
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
    icon=['pelotaicon.ico'],
)
