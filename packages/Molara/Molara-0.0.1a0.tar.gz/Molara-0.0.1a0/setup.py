"""Setup file for Cython compilation of the project."""

from __future__ import annotations

from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules = cythonize(
        "./src/molara/Tools/raycasting.pyx",
        "./src/molara/Tools/mathtools.pyx",
        "./src/molara/Rendering/sphere.pyx",
        "./src/molara/Rendering/matrices.pyx",
        "./src/molara/Rendering/cylinder.pyx.pyx",
    ),
)
