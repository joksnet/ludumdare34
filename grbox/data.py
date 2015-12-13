
import os.path

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA = os.path.join(ROOT, 'data')

def datafile(filename):
    return os.path.join(DATA, filename)

def imagefile(filename):
    return datafile(os.path.join('images', filename))

def imagefruit(name, size):
    return imagefile(name + '-' + size + '.bmp')

def soundfile(filename):
    return datafile(os.path.join('sounds', filename))

