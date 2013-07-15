from __future__ import absolute_import

import os
import fancypages as fp

__version__ = (0, 2, 0, 'dev', 0)


def get_oscar_fancypages_paths(path):
    return [
        os.path.join(os.path.dirname(
            os.path.abspath(__file__)),
            path
        ),
    ] + fp.get_fancypages_paths(path)


def get_required_apps():
    return fp.get_required_apps()


def get_oscar_fancypages_apps():
    ofp_apps = ('oscar_fancypages.fancypages',)
    app_labels = []
    for app_name in ofp_apps:
        app_label = app_name.rsplit('.', 1)[-1]
        if app_label:
            app_labels.append(app_label)
    fp_apps = []
    for app_name in fp.get_fancypages_apps():
        app_label = app_name.rsplit('.', 1)[-1]
        if app_label not in app_labels:
            fp_apps.append(app_name)
    return tuple(fp_apps) + ofp_apps
