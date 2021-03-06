# -*- coding: utf-8 -*-
# @COPYRIGHT_begin
#
# Copyright [2015] Michał Szczygieł, M4GiK Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @COPYRIGHT_end

import logging
import os

from core.settings import config

# Set of active loggers - ones currently writing to logs.
active_loggers = set([])
logging.basicConfig()


def get_logger(logger_id):
    """
    Returns logger.
    - If no logger_id is provided, then logger is anonymus. His logs go to the file
    intended for storing anonimous logs.
    - Otherwise user is added to active loggers. Function creates unique file
    handler for his logs.
    This way actions may be analyzed per user.
    """
    if logger_id:
        log_name = 'user_%d' % logger_id
    else:
        log_name = 'no_user'
        logger_id = 0
    if logger_id in active_loggers:
        return logging.getLogger(log_name)

    active_loggers.add(logger_id)
    logger = logging.getLogger(log_name)
    hdlr = logging.FileHandler(os.path.join(config.LOG_DIR, '%s.log' % log_name))
    formatter = logging.Formatter(config.LOG_FORMAT)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(config.LOG_LEVEL)

    return logger


def debug(logger_id, text):
    """
    @parameter{logger_id,int} optional, id of the logger. If no id is provided,
    logs are anonymous.
    @parameter{text,string} content of the log.
    Prints debug log with @prm{content} to log file of the user @prm{id}.
    """
    get_logger(logger_id).debug(text)


def info(logger_id, text):
    """
    @parameter{logger_id,int} optional, id of the logger. If no id is provided,
    logs are anonymous.
    @parameter{text,string} content of the log.
    Prints info log with @prm{text} content to log file of the user @prm{logger_id}.
    """
    get_logger(logger_id).info(text)


def warning(logger_id, text):
    """
    @parameter{logger_id,int} optional, id of the logger. If no logger_id is provided,
    logs are anonymous.
    @parameter{text,string} content of the log.
    Prints warning log with @prm{text} content to log file of the user @prm{logger_id}.
    """
    get_logger(logger_id).warning(text)


def exception(logger_id, text):
    """
    @parameter{logger_id,int} optional, id of the logger. If no id is provided,
    logs are anonymous.
    @parameter{text,string} content of the log.
    Prints exception log with @prm{text} content to log file of the user @prm{logger_id}.
    """
    get_logger(logger_id).exception(text)


def error(logger_id, text):
    """
    @parameter{logger_id,int} optional, id of the logger. If no id is provided,
    logs are anonymous.
    @parameter{text,string} content of the log.
    Prints error log with @prm{text} content to log file of the user @prm{logger_id}.
    """
    get_logger(logger_id).error(text)
