# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Get all Python files in the current directory
import os
python_files = [(f, '.') for f in os.listdir('.') if f.endswith('.py')]

a = Analysis(
    ['main_GUI.py'],
    pathex=[],
    binaries=[],
    datas=python_files,  # Include all Python files
    hiddenimports=[
        'tkinter',
        'subprocess',
        'logging',
        'socket',
        'scrolledtext',
        'tkinter.font',
        'tkinter.messagebox',
        'sys',
        'os',
        'json',
        'requests',
        'urllib3',
        'deepseek',
        'docx',
        'python-docx',
        'docx.oxml.ns',
        'docx.shared',
        'docx.oxml',
        'lxml',
        'run_main1',
        'main1',
        'run_search_initial',
        'run_search_process',
        'run_main_all',
        'revise_document',
        'main3',
        'main4',
        'run_main_all',
        'main2',
        'requests',
        'urllib3',
        'certifi',
        'idna',
        'chardet',
        'charset_normalizer',
        'bs4',
        'fake_useragent',
        'beautifulsoup4',
        'soupsieve',
        'html.parser',
    ],
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
    name='CaseGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep True for debugging
    icon='abc.ico' if os.path.exists('abc.ico') else None
) 