# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:/Users/david/OneDrive/Documents/EliteSkins R6 Mod Installer for Dirt/installer/installer/main.py'],
             pathex=['C:\\Users\\david\\OneDrive\\Documents\\EliteSkins R6 Mod Installer for Dirt'],
             binaries=[],
             datas=[('C:/Users/david/OneDrive/Documents/EliteSkins R6 Mod Installer for Dirt/installer/installer/data/1.save', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , uac_admin=True, icon='C:\\Users\\david\\Downloads\\icons8-rainbow-six-siege-100.ico')
