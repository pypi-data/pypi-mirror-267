from setuptools import setup, find_packages

setup(
    name='AMDV_VIDEO_EDITING',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv'
    ],
    extras_require={
        'full': open('requirements.txt').read().splitlines(),
    },
    entry_points={
        'console_scripts': [
            'fetch_stickers=giphy_sticker_fetcher:main'
        ]
    },
    author='AMDV',
    author_email='info@aifats.com',
    description='AMDV_VIDEO_EDITING is a Python package for video editing tasks, such as trimming, splitting, merging, and applying various effects to videos. This package aims to provide a simple and efficient interface for performing common video editing operations using the AMDV (Advanced Multimedia Data Visualization) library.',
    url='https://github.com/AIFATS/AMDV_VIDEO_EDITHING.git',
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
