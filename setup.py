import cx_Freeze
from cx_Freeze import *


setup(
    name = "Brickshooter",
    options = {"build_exe":{"packages":['pygame']}},
    executables=[
        Executable(
            "main.py",
        )
    ]
)