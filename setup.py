# from distutils.core import setup
# import py2exe
# setup(windows=['gui_version.py'])
# # setup(windows=["gui_version.py"], options={"py2exe":{"includes":["sip"]}})

import py2exe
from distutils.core import setup
# setup( windows=[{"script": "gui_version.py"}] )

py2exe_opciones = {'py2exe': {"includes":["sip",'PyQt5.QtGui', 'PyQt5.QtCore']}}
script = [{"script":"gui_version.py"}]

setup(windows=script,options=py2exe_opciones)