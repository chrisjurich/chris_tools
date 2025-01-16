import json
import shutil
from pathlib import ( 
    Path
)


def safe_rm( fname ):

    fpath = Path(fname)
    if fpath.exists():
        fpath.unlink()

def safe_rmdir( dirname ):
    dpath=Path(dirname)
    if dpath.is_dir():
        shutil.rmtreet(dirname)
        

def safe_mkdir( dirname, parents=True, exist_ok=True ):
    dpath = Path(dirname)
    if not dpath.is_dir():
        dpath.mkdir(parents=parents, exist_ok=exist_ok)


def write_lines( fname, lines ):
    fh = open(fname, 'w')
    fh.write(
        '\n'.join(lines)
    )

    fh.close()

    return fname

def get_lines( fname ):
    fh = open(fname, 'r')
    lines = fh.read().splitlines()
    fh.close()

    return lines

def to_json(data, fname):
    json.dump(
        data,
        open(fname, 'w'),
        indent=4,
        sort_keys=True
    )

    return fname

def from_json(fname):
    return json.load(
        open(fname, 'r')
    )

