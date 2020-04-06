#!/usr/bin/env python3
"""Setup file for mcycle"""
USE_CYTHON = 'auto'

import os
from setuptools import setup
from setuptools import find_packages
#from distutils.core import setup
#from distutils.extension import Extension
from setuptools.extension import Extension
import numpy

# Generate constants.py and _constants.pxd modules
with open("mcycle/_constants.pyx", 'r') as f:
    warning_message = "# THIS FILE IS AUTOMATICALLY GENERATED: DO NOT EDIT!\n"
    wl_py = [
        warning_message,
    ]
    wl_pxd = [
        warning_message,
    ]
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#'):
            wl_py.append(line + '\n')
            wl_pxd.append(line + '\n')
        else:
            try:
                elems = line.split(' ')
                eq_id = elems.index('=')
                wl_py.append(' '.join(elems[eq_id - 1:eq_id + 2]) + '\n')
                wl_pxd.append(' '.join(elems[:eq_id]) + '\n')
            except:
                continue
    try:
        constants_py = open("mcycle/constants.py", 'w')
    except:
        constants_py = open("mcycle/constants.py", 'x')
    finally:
        constants_py.writelines(wl_py)
        constants_py.close()
    try:
        constants_pxd = open("mcycle/_constants.pxd", 'r')
        readlines = constants_pxd.readlines()
        try:
            readlines.remove('\n')
        except:
            pass
        try:
            readlines.remove(' \n')
        except:
            pass
        if readlines == wl_pxd:
            constants_pxd.close()
            print("mcycle/_constants.pxd found and up to date")
        else:
            constants_pxd.close()
            raise ValueError("mcycle/_constants.pyx has changed")
    except FileNotFoundError:
        print("Building mcycle/_constants.pxd")
        constants_pxd = open("mcycle/_constants.pxd", 'x')
        constants_pxd.writelines(wl_pxd)
        constants_pxd.close()
    except Exception as exc:
        print("Rebuilding mcycle/_constants.pxd: ", exc)
        constants_pxd = open("mcycle/_constants.pxd", 'w')
        constants_pxd.writelines(wl_pxd)
        constants_pxd.close()

try:
    import Cython
    v = Cython.__version__.split(".")
    if int(v[0]) == 0 and int(v[1]) < 27:
        raise ImportError(
            "Exiting installation - Please upgrade Cython to at least v0.28. Try running the command: pip3 install --upgrade Cython"
        )
    else:
        USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
    '''raise ImportError(
        "Exiting installation - Could not import Cython. Try running the command: pip3 install Cython"
    )'''

if USE_CYTHON:
    try:
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
    except ImportError as exc:
        if USE_CYTHON == 'auto':
            USE_CYTHON = False
        else:
            raise ImportError(
                """Exiting installation - Importing Cython unexpectedly failed due to: {}
Try re-installing Cython by running the commands:
pip3 uninstall Cython
pip3 install Cython""".format(exc))

cmdclass = {}
ext_modules = []
include_dirs = [numpy.get_include()]
compiler_directives = {
    'embedsignature': True,
    "language_level": 3,
    "boundscheck": False,
    "wraparound": False
}


def scanForExtension(directory, extension, files=[]):
    "Find all files with extension in directory and any subdirectories, modified from https://github.com/cython/cython/wiki/PackageHierarchy"
    length = len(extension)
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isfile(path) and path.endswith(extension):
            files.append(path[:-length])
        elif os.path.isdir(path):
            scanForExtension(path, extension, files)
    return files


if USE_CYTHON:
    pyx_exts = scanForExtension("mcycle", ".pyx")
    for ext in pyx_exts:
        ext_modules += cythonize(
            "{}.pyx".format(ext),
            nthreads=4,
            compiler_directives=compiler_directives)
    cmdclass.update({'build_ext': build_ext})
else:
    c_exts = scanForExtension("mcycle", ".c")
    for ext in c_exts:
        ext_modules += [Extension(ext, ['{}.c'.format(ext)])]

# Get metadata
meta = {}
with open('mcycle/__meta__.py') as fp:
    exec (fp.read(), meta)  # get variables from mcycle/__meta__
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='mcycle',
    version=meta['version'],
    description=meta['description'],
    long_description=long_description,
    url=meta['url'],
    author=meta['author'],
    author_email=meta['author_email'],
    license=meta['license'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords=meta['keywords'],
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'matplotlib', 'Cython', 'CoolProp'],
    dependency_links=['https://github.com/CoolProp/CoolProp.git'],
    extras_require={},
    python_requires='>=3',
    include_package_data=True,
    package_data={
        'mcycle': ['*.pxd', '*.pyx'],
        'mcycle/*': ['*.pxd', '*.pyx'],
        'mcycle/*/*': ['*.pxd', '*.pyx'],
        'mcycle/*/*/*': ['*.pxd', '*.pyx']
    },
    data_files=[],
    entry_points={},
    cmdclass=cmdclass,
    include_dirs=include_dirs,
    ext_modules=ext_modules,
    zip_safe=False,
)
