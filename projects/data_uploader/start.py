''''
Module: Main
Description: ....
Author: xxx
'''
# Import standard modules
import os

# Import own modules
from app import s3_utils
from core import core

print("*****"*10)
print("WELCOME TO DATA UPLOADER PROJECT")
print("*****"*10)


if __name__ == "__main__":
    print("My Module name is ", __name__)
    print("Project: Started")
    core.main_core()
