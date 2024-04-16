from setuptools import setup
from pathlib import Path

dir = Path(__file__).parent
long_description = (dir / "README.md").read_text()

setup(
    name='cyg_mnt_point',
    url='https://github.com/Serhii5465/cyg_mnt_point',
    version="0.1",
    author='Serhii5465',
    description='Search for the mount point in Cygwin by UUID disk partition',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'' : 'src'},
    packages=['cyg_mnt_point'],
    python_requires='>=3.8',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ]
)