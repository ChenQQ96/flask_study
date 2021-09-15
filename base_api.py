import flask
import sys
import os
import time

from werkzeug.wrappers import Request,Response
from werkzeug.serving import run_simple

from flask import Flask
#配置logging文件，简化logger = logging.getLogger(__name__)，使用logging.basicConfig定义默认接口，可以直接使用logging对象
import logging
logging.basicConfig(
    # filename='my.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s +%(lineno)s: %(levelname)-8s %(message)s'
    )

#配置当前文件夹的绝对路径
current_dir=os.path.dirname(os.path.abspath(__file__))