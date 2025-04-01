# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add all your Python files to the datas list
added_files = [
    ('run_search_process.py', '.'),
    ('search0.py', '.'),
    ('run_main1.py', '.'),
    ('run_main_all.py', '.'),
    ('revise_document.py', '.'),
    ('main4.py', '.'),
    ('search1.py', '.'),
    ('search1_create_folder.py', '.'),
    ('search2.py', '.'),
    ('search3.py', '.'),
    ('search4.py', '.')
]

a = Analysis(
    ['main_GUI.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('search1.py', '.'),
        ('search1_create_folder.py', '.'),
        ('search2.py', '.'),
        ('search3.py', '.'),
        ('search4.py', '.'),
        ('run_search_process.py', '.'),
        # Add any other required files here
    ],
    hiddenimports=[
        'bs4',
        'requests',
        'urllib3',
        'lxml',
        'socket',
        '_socket',
        'encodings',
        'chardet',
        'certifi',
        'idna',
        'urllib3.packages.ssl_match_hostname'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['fake_useragent'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main_GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 