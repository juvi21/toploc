import os
import platform
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CppExtension

CSRC_DIR = os.path.join("toploc", "C", "csrc")

# Decide whether to build in dev (debug) mode or release mode
if os.getenv("DEV", "0") == "1":
    compile_args = ["-O0", "-g"]  # debug compile flags
    debug_mode = True
else:
    compile_args = ["-O3"]        # release compile flags
    debug_mode = False

link_args = []

if platform.system() == "Darwin":
    # Enable support for both Intel and Apple Silicon
    compile_args += ["-arch", "x86_64", "-arch", "arm64"] 
    link_args += ["-arch", "x86_64", "-arch", "arm64"]
    # Add minimum deployment target for macOS
    compile_args += ["-mmacosx-version-min=10.13"]
    link_args += ["-mmacosx-version-min=10.13"]

extensions = [
    CppExtension(
        name="toploc.C.csrc.ndd",
        sources=[os.path.join(CSRC_DIR, "ndd.cpp")],
        extra_compile_args=compile_args,
        extra_link_args=link_args,
    ),
    CppExtension(
        name="toploc.C.csrc.utils",
        sources=[os.path.join(CSRC_DIR, "utils.cpp")],
        extra_compile_args=compile_args,
        extra_link_args=link_args,
    ),
]

setup(
    name="toploc",
    ext_modules=extensions,
    packages=["toploc", "toploc.C", "toploc.C.csrc"],
    package_data={
        "toploc.C.csrc": ["*.pyi"],  # Include .pyi files 
    },
    cmdclass={
        "build_ext": BuildExtension.with_options(
            use_ninja=True,
            debug=debug_mode
        )
    },
)