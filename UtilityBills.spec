# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/igi/Desktop/Projects/excelPDF/app.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/igi/Desktop/Projects/excelPDF/styles.qss', '.'), ('/Users/igi/Desktop/Projects/excelPDF/icon.svg', '.'), ('/Users/igi/Desktop/Projects/excelPDF/appLayout.ui', '.'), ('/Users/igi/Desktop/Projects/excelPDF/requirements.txt', '.'), ('/Users/igi/Desktop/Projects/excelPDF/README.md', '.')],
    hiddenimports=['PyQt5.sip', 'google.auth', 'google.oauth2', 'google_auth_httplib2', 'google_auth_oauthlib', 'openpyxl', 'pdfkit', 'requests', 'email.mime.multipart', 'email.mime.text', 'email.mime.base', 'smtplib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'test', 'tests', 'matplotlib', 'numpy', 'scipy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='UtilityBills',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/igi/Desktop/Projects/excelPDF/icon.svg'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UtilityBills',
)
app = BUNDLE(
    coll,
    name='UtilityBills.app',
    icon='/Users/igi/Desktop/Projects/excelPDF/icon.svg',
    bundle_identifier=None,
)
