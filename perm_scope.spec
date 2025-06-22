# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from glob import glob
from PyInstaller.utils.hooks import collect_submodules

def encontrar_datos():
    datos = []
    carpetas = ['modulos', 'ventanas', 'docs']
    for carpeta in carpetas:
        for archivo in glob(f'{carpeta}/**/*', recursive=True):
            ruta = Path(archivo)
            if ruta.is_file():
                datos.append((str(ruta), str(ruta)))
    return datos

a = Analysis(
    ['perm_scope.py'],
    pathex=['.'],
    binaries=[],
    datas=encontrar_datos() + [
        ('banner.txt', '.'),
        ('Icono.ico', '.'),
    ],
    hiddenimports=collect_submodules('modulos') + collect_submodules('ventanas'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PermScope',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True para consola, False para modo ventana
    icon='Icono.ico'
)
