# -*- mode: python -*-

block_cipher = None
added_files = [
('..\\Assets\\Views\\Level1\\Level1.json', 'Assets\\Views\\Level1'),
('..\\Assets\\Views\\Level1\\Level1.png', 'Assets\\Views\\Level1'),
('..\\Assets\\Views\\Level2\\Level2.json', 'Assets\\Views\\Level2'),
('..\\Assets\\Views\\Level2\\Level2.png', 'Assets\\Views\\Level2'),
('..\\Assets\\Views\\Level2\\background.png', 'Assets\\Views\\Level2'),
('..\\Assets\\Views\\Level2\\config.json', 'Assets\\Views\\Level2'),
('..\\Assets\\Views\\View1\\view1.json', 'Assets\\Views\\view1'),
('..\\Assets\\Views\\View1\\view1.png', 'Assets\\Views\\view1'),
('..\\Assets\\Fonts\\InknutAntiqua-Light.ttf', 'Assets\\Fonts'),
('..\\Assets\\Sound\\m4rt3z_m4rt3z---Elemental-Energy-Oxy-320.mp3', 'Assets\\Sounds'),
('..\\Assets\\Sound\\m4rt3z_m4rt3z---Primal-Snap-320.mp3', 'Assets\\Sounds'),
('..\Assets\\Images\dog.ico', 'Assets\Images')
]

a = Analysis(['..\\Src\\Game.py'],
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
