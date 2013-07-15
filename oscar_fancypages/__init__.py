from __future__ import absolute_import

import os

from fancypages import  get_fancypages_paths


__version__ = (0, 1, 0, 'dev', 0)


def get_oscar_fancypages_paths(path):
    return [
        os.path.join(os.path.dirname(
            os.path.abspath(__file__)),
            path
        ),
    ] + get_fancypages_paths(path)
