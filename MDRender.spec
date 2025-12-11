# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Get the absolute path to the project directory
project_dir = os.path.abspath(SPECPATH)

a = Analysis(
    ['main.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[
        ('resources', 'resources'),
    ],
    hiddenimports=[
        # Local packages
        'gui',
        'gui.main_window',
        'gui.editor',
        'gui.preview',
        'gui.toolbar',
        'core',
        'core.markdown_processor',
        'core.file_handler',
        'core.themes',
        'core.exporter',
        'utils',
        'utils.config_manager',
        'utils.shortcuts',
        'utils.helpers',
        'config',
        # Markdown extensions
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.nl2br',
        'pymdownx.superfences',
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
        'pymdownx.tasklist',
        'pymdownx.emoji',
        'pymdownx.magiclink',
        'pymdownx.mark',
        'pymdownx.tilde',
        'pymdownx.keys',
        # Pygments
        'pygments',
        'pygments.lexers',
        'pygments.formatters',
        'pygments.styles',
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
    [],
    exclude_binaries=True,
    name='MDRender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/favicon.ico',  # Add icon path here if you have one: 'resources/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MDRender',
)
