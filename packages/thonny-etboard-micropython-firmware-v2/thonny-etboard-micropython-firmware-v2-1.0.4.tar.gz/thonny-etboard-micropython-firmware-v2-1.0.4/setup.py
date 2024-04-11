import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-etboard-micropython-firmware-v2",
    version="1.0.4",
    author="KETRi",
    author_email="ketri3000@gmail.com",
    description="이티보드 마이크로파이썬 펌웨어",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://et.ketri.re.kr/",
    project_urls={
        "Bug Tracker": "http://et.ketri.re.kr/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["thonnycontrib.thonny_etboard_firmware_v2"],
    package_data={"thonnycontrib.thonny_etboard_firmware_v2" : ["*", "*/*", "*/*/*", "*/*/*/*", "*/*/*/*/*"]},
    install_requires = ["thonny>=3.3.11"],
    python_requires=">=3.6",
)