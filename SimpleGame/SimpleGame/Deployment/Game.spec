# -*- mode: python -*-

block_cipher = None
added_files = [

]

a = Analysis(['..\\Src\\SmallGame.py'],
             pathex=['.\\'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Game',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='..\\Assets\\Images\\dog.ico')
