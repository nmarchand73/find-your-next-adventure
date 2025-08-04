"""
Find Your Next Adventure - A travel destination parser and generator.
"""

__version__ = "1.0.0"
__author__ = "Nicolas Marchand"
__description__ = "Extract and generate structured JSON data from adventure travel guides"

from . import models, parsers, utils

__all__ = ['models', 'parsers', 'utils']
