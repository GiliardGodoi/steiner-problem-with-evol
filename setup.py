from setuptools import setup, find_packages

setup(
    name='ga4stpg',
    version='0.0.0',
    description='Genetic Algorithms for Steiner Tree Problem in Graphs',
    long_description=open('README.md').read(),
    author='Giliard Almeida de Godoi',
    author_email='giliardgodoi@alunos.utfpr.edu.br',
    keywords=['genetic', 'algorithms', 'steiner', 'graph'],
    url='https://github.com/GiliardGodoi/ppgi-stpg-gpx',
    license='MIT License',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence']
)