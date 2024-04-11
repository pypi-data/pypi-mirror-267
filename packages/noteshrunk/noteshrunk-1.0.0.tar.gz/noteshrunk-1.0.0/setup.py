from setuptools import setup

setup(
    name='noteshrunk',
    version='1.0.0',
    description='Document Color Palette Compression',
    author='suuuehgi',
    author_email='euaoadcioa@gmail.com',
    py_modules=['noteshrunk'],
    entry_points={
        'console_scripts': [
            'noteshrunk = noteshrunk:main'
        ]
    },
    install_requires=[
        'numpy',
        'Pillow',
        'scipy',
        'scikit-image',
        'scikit-learn',
        'argcomplete'
    ]
)
