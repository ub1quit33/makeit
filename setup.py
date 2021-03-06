import sys, os
from StringIO import StringIO
from setuptools import setup, Command
from tests.__main__ import main as testmain

try:
    import coverage
except ImportError:
    coverage = None

if coverage:
    class Coverage(Command):
        description  = 'Calculate code coverage of unit tests'
        user_options = []
        def run(self):
            cover  = coverage.Coverage()
            buffer = StringIO()
            cover.start()
            testmain()
            cover.stop()
            cover.save()
            cover.html_report()
            cover.report(file=buffer)
            buffer.seek(0)
            for line in buffer.readlines():
                columns = line.split()
                # Exclude coverage reports on external modules
                if os.path.abspath(columns[0]).startswith(sys.prefix):
                    continue
                # The total is not accurate since we're filtering out entries
                if columns[0] == 'TOTAL':
                    continue
                sys.stdout.write(line)
        def initialize_options(self):
            pass
        def finalize_options(self):
            pass
else:
    class Coverage(Command):
        def run(self):
            pass
        def initialize_options(self):
            pass
        def finalize_options(self):
            pass

setup(
    name='makeit',
    version='0.1',
    description='A reimagined task loader for doit',
    author='James Lott',
    author_email='james@lottspot.com',
    license='MIT',
    keywords='doit build automation',
    packages=['makeit'],
    install_requires=['doit>=0.28'],
    test_suite='tests',
    cmdclass={
        'coverage': Coverage,
    },
    entry_points={
        'console_scripts': ['makeit = makeit.__main__:main']
    }
)
