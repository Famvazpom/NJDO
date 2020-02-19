from distutils.core import setup
import py2exe

setup(
    windows=['busqueda.py'],
    options = {
        'py2exe': {
            'packages': ['Py2PDF2']
        }
    }
)