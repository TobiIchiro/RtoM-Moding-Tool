# ModTool_onefile.spec
import os
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE

# Ruta base del proyecto
base_path = os.path.abspath(".")

# Archivos y carpetas que deseas incluir
datas = [
    ("Data", "Data"),
    ("Icon", "Icon"),
]

a = Analysis(
    ["PythonFiles/main.py"],
    pathex=[base_path],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules('PySide6'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="ModToolTool",
    debug=False,
    strip=False,
    upx=True,
    console=False,  # Cambia a False para ocultar la consola
    icon=os.path.join(base_path,"Icon","ToolIcon.ico"),
    bootloader_ignore_signals=False,
    onefile=True,
)
