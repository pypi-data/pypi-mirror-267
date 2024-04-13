"""File used to compile the cython modules.

It needs to be called manually with python3 cython_build.py build_ext --inplace.
"""

from __future__ import annotations

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup

__copyright__ = "Copyright 2024, Molara"

# Modules to be compiled and include_dirs when necessary
extensions = [
    Extension(
        "molara.Rendering.cylinder",
        sources=["src/molara/Rendering/cylinder.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "molara.Rendering.sphere",
        sources=["src/molara/Rendering/sphere.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "molara.Rendering.matrices",
        sources=["src/molara/Rendering/matrices.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "molara.Tools.mathtools",
        sources=["src/molara/Tools/mathtools.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "molara.Tools.raycasting",
        sources=["src/molara/Tools/raycasting.pyx"],
        include_dirs=[np.get_include()],
    ),
]


# This is the function that is executed
setup(
    name="Molara",  # Required
    # A list of compiler Directives is available at
    # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-directives
    # external to be compiled
    ext_modules=cythonize(extensions, compiler_directives={"language_level": 3}),
    include_dirs=[np.get_include()],
)
