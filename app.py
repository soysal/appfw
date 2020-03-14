#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Application utilities

Created on   : 2019-12-11 ( Ergin Soysal )
Last modified: Mar 05, 2020, Thu 00:34:59 -0600
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import os.path

import json

import logging

LOG_FORMAT = '%(asctime)-15s %(levelname)-5s %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_SUFFIX = '%Y%m%d.log'


def _set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def write_json(fname, obj):
    print("Writing", fname)
    with open(fname, 'w') as fp:
        json.dump(obj, fp, indent=2, default=_set_default)


def configure(args):
    config = _get_conf(args.cfgfile)
    _configure_log(config, args.log_section)

    log.info('Using configuration file: %s', args.cfgfile)
    log.debug(args)

    return config


def _configure_log_file(filename, formatter, level, suffix=LOG_SUFFIX):
    from logging.handlers import TimedRotatingFileHandler
    fh = TimedRotatingFileHandler(filename=filename, when='midnight', interval=1)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    fh.suffix = suffix

    return fh


def _configure_log_console(formatter, level):
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level)

    return ch


def _configure_log(config, sec_name):
    global log
    
    if config and config.has_section(sec_name):
        log_conf = config[sec_name]
        appname = log_conf.get('name', None)
        level = log_conf.get('level', LOG_LEVEL)

        # format
        format = log_conf.get('format', LOG_FORMAT, raw=True)
        formatter = logging.Formatter(format)

        # the logger
        log = logging.getLogger(appname)
        log.setLevel(level)

        logfile = log_conf.get('filename', None)
        if logfile:
            suffix = log_conf.get('suffix', LOG_SUFFIX, raw=True)
            fh = _configure_log_file(logfile, formatter, level, suffix)
            log.addHandler(fh)
            log.info('Logging at level %s to file "%s"', level, logfile)

        ch_level = log_conf.get('con_level', None)
        if ch_level or not logfile:
            ch_level = ch_level or level
            ch = _configure_log_console(formatter, ch_level)
            log.addHandler(ch)

            log.info('Logging at level %s to console', ch_level)

        log.info('Log "%s" is configured using section "%s"', appname, sec_name)
    else:
        logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
        log = logging.getLogger()
        logging.debug("Configured logger at level %s to console", LOG_LEVEL)


def _get_conf(cfgfile):
    if os.path.exists(cfgfile):
        from configparser import ConfigParser, ExtendedInterpolation
        config = ConfigParser(os.environ, interpolation=ExtendedInterpolation())
        config.read(cfgfile)
        return config
    else:
        return None

