# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/4/8 16:17
# @Author  : jerry.zzw 
# @Email   : jerry.zzw@antgroup.com
# @FileName: setup.py

import setuptools

with open("README_PYPI.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agentUniverse",
    version="0.0.1.beta1",
    author="AntGroup",
    author_email="jerry.zzw@antgroup.com",
    description="AgentUniverse is a framework for developing applications powered "
                "by multi-agent base on large language model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
            '': ['*.yaml'],
        },
    classifiers=[
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
