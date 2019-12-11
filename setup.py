from setuptools import setup


setup(
    name='coverage-context-report',
    author='Pablo Garcia de los Salmones',
    version='0.0.0',
    keywords='coverage context unittest',
    packages=['app', 'code_demo', 'test'],
    description='Python project to include context into coverage html report',
    license='Apache Software License',
    install_requires=['coverage==5.0b1', 'pytest-cov==2.8.1']
)
