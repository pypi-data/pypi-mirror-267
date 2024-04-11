from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# TESTS
setup(
    name='Helix-Engine-TEST',
    version='1.0.0',
    description='Helix [ more than developers ]',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TheDotBat/Helix',
    author='Izaiyah Stokes',
    author_email='setoichi.dev@gmail.com',
    license='Apache-2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.png', '*.jpg', '*.jpeg', '*.gif'],
        'my_package': ['assets/*'],
    },
    install_requires=[
        'Numpy', 'PyGLM', 'pygame-ce',
        'Numba', 'ModernGL', 'OpenSimplex'],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: pygame',
        'Operating System :: Microsoft :: Windows :: Windows 11',
    ],
    # entry_points={
    #     'console_scripts': [
    #         'PyForge -t=PyForge.scripts.test:main',
    #         'PyForge -T=PyForge.scripts.test:main',
    #         'PyForge -test=PyForge.scripts.test:main',
    #         'PyForge -Test=PyForge.scripts.test:main',
    #     ]
    # },
)