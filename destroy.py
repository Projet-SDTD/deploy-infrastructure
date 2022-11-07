#!/bin/python3
import os
import platform
import subprocess

filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)

def destroyTerraform():
    os.chdir(os.path.join(dirpath, "terraform-resources"))
    subprocess.run(["terraform", "destroy", "-auto-approve"])

currentSystem = platform.system()
if currentSystem != 'Linux':
    print("## This script is intended for Linux only !")
    exit(1)

destroyTerraform()