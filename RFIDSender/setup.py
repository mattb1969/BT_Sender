#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages

setup(name="RFIDSender",
      packages = find_packages(),
      version="0.2",
      description="Bostin Technology RFID Sender Module",
      author="Matthew Bennett",
      author_email="matthew.bennett@bostintechnology.com",
      url="http://www.BostinTechnology.com",
      install_requires=["WiringPi2", "Boto3"],
      scripts=["CognIoTRFID125kHz"],
      )



