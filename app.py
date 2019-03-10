# app.py cara penulisannya
from flask import Flask, request    #cara import sebuah package
from flask_restful import Resource, Api, reqparse, abort       #ini semua adalah package
from time import strftime
import json, logging, sys
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy   #import db
from flask_migrate import Migrate          #import untuk migrate db
from blueprints import app, manager

if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes=10000, backupCount=20)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)
    try:
        if sys.argv[1] == 'db':
            manager.run()
        else:
            app.run(debug=False, host='0.0.0.0', port=5000)
    except IndexError as e:
        app.run(debug=True, host='0.0.0.0', port=5000)
    