from setuptools import setup

setup(
    name='aiio',
    version="0.1.1",
    author='Mario Balibrera',
    author_email='mario.balibrera@gmail.com',
    license='MIT License',
    description='english-speaking chat ai',
    long_description='A general-purpose conversational chat bot.',
    packages=[
        'aiio'
    ],
    zip_safe = False,
    install_requires = [
#        "ct >= 0.8.14",
        "wikipedia >= 1.4.0",
        "nltk >= 3.2.1",
        "pocketsphinx >= 0.1.3",
        "duckduckpy >= 0.2"
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
