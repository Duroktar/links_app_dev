pyinstaller --noconsole --onefile --icon=icon.ico main.py
mshta "javascript:var sh=new ActiveXObject( 'WScript.Shell' ); sh.Popup( 'Build finsihed!', 0, 'PyInstaller - Build', 64 );close()"