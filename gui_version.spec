# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui_version.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[
                'PyQt5',
                'PyQt5.sip'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

import sys
# First, generate an executable file
# Notice that the icon is a .icns file - Apple's icon format
# Also note that console=True
if sys.platform == 'darwin':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='HeartAlgo-Analyzer',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True,
            icon='assets/icon.icns')
elif sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='HeartAlgo-Analyzer',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon='assets/icon.ico')

# Package the executable file into .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='SignalAnalyzer.app',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                },
                icon='assets/icon.icns')
else:
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='scriptname')
