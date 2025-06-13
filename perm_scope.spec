# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['perm_scope.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('banner.txt', '.'),                          # Archivos necesarios
        ('Foto CLI.png', '.'),
        ('Foto Gui Modo Claro.png', '.'),
        ('Foto Gui Modo Oscuro.png', '.'),
        ('Icono.png', '.'),
        ('Icono.ico', '.'),
        ('ventanas/**/*', 'ventanas'),                # Carpeta de interfaz
        ('modulos/**/*', 'modulos')                   # Carpeta de módulos
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='PermScope',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True = modo consola / False = oculta la consola (para GUI pura)
    icon='Icono.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PermScope'
)
