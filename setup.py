import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idle_notifier",
    version="0.1",
    author="Zi Jian Yew",
    author_email="yewzijian@gmail.com",
    description="Notifies user when computer is idle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yewzijian/idle_notifier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "coloredlogs",
        "psutil"
        "urllib3"
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'idle_notifier_setup = idle_notifier:idle_notifier_setup',
            'idle_notifier_remove = idle_notifier:idle_notifier_remove',
        ]
    },
)