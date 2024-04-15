import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="format_print",
    version="1.0",
    author="taikooo",
    author_email="bbstufo@gmail.com",
    description="一个用于格式化输出的库，主要功能包括多行输出刷新、全半角字符混合对齐、秒数及字节大小格式化等",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taikoooo/format_print",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.8',
)