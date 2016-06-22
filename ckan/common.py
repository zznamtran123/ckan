# encoding: utf-8

# This file contains commonly used parts of external libraries. The idea is
# to help in removing helpers from being used as a dependency by many files
# but at the same time making it easy to change for example the json lib
# used.
#
# NOTE:  This file is specificaly created for
# from ckan.common import x, y, z to be allowed

import flask
import pylons

from werkzeug.local import LocalProxy

from flask_babel import gettext as flask_gettext
from pylons.i18n import _ as pylons_gettext, ungettext

from pylons import g, response
import simplejson as json

try:
    from collections import OrderedDict  # from python 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict


def is_flask():
    '''
    A centralised way to determine whether to return flask versions of common
    functions, or Pylon versions.

    Currently using the presence of `flask.request`, though we may want to
    change that for something more robust.
    '''
    if flask.request:
        return True
    else:
        return False


def _(text):
    # TODO: As is this will only work in the context of a web request
    # Do we need something for non-web processes like paster commands?
    # Pylons have the translator object which we need to fake but maybe
    # that's not necessary at all
    if is_flask():
        # TODO: For some reasone the Flask gettext changes 'String %s' to
        # 'String {}' (maybe it's the babel version?)
        if '%s' in text:
            return flask_gettext(text).replace('{}', '%s')
        else:
            return flask_gettext(text)
    else:
        return pylons_gettext(text)


def _get_request():
    if is_flask():
        return flask.request
    else:
        return pylons.request


def _get_c():
    if is_flask():
        return flask.g
    else:
        return pylons.c


def _get_session():
    if is_flask():
        return flask.session
    else:
        return pylons.session


def _get_config():
        try:
            current_app = flask.current_app
            return current_app.config
        except RuntimeError:
            return pylons.config


c = LocalProxy(_get_c)
config = LocalProxy(_get_config)
session = LocalProxy(_get_session)
request = LocalProxy(_get_request)
