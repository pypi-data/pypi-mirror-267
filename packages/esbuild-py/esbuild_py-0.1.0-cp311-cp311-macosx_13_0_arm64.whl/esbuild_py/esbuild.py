import ctypes
from distutils.sysconfig import get_config_var
from pathlib import Path
import os
import site


# Location of shared library
so_dir = site.getsitepackages()[0]
ext_suffix = get_config_var('EXT_SUFFIX')
so_filename = ('_esbuild' + ext_suffix)
so_filepath = os.path.join(so_dir, so_filename)

# Load functions from shared library set their signatures
so = ctypes.cdll.LoadLibrary(so_filepath)
transform_binding = so.transform
transform_binding.argtypes = [ctypes.c_char_p]
transform_binding.restype = ctypes.c_void_p
free = so.free
free.argtypes = [ctypes.c_void_p]


def transform(jsx):
    res = transform_binding(jsx.encode('utf-8'))
    if res is not None:
        msg = ctypes.string_at(res).decode('utf-8')
        free(res)
        return msg

