from setuptools import setup, find_packages

setup(
    name='EasIlastik',
    version='0.0.1',
    author='Titouan Le Gourrierec',
    author_email='titouanlegourrierec@icloud.com',
    url='https://github.com/titouanlegourrierec/EasIlastik',
    description='This package provides seamless integration of pre-trained image segmentation models from Ilastik into Python workflows, empowering users with efficient and intuitive image segmentation capabilities for diverse applications.',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
)