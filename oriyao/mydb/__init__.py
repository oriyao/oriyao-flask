"""
# coding:utf-8
@Time    : 2021/01/03
@Author  : oriyao
@mail    : ylzhangyao@gmail.com
@File    : __init__.py
@Describe: for mongodb initial command
"""

import time
import pymongo
from flask import current_app


def initial_mongodb():
    current_app.logger.info('Initial my mongodb.')

    # app.logger.info(app.config["MONGO_URI_WITHOUTDB"])
    myclient = pymongo.MongoClient(current_app.config['MONGO_URI_WITHOUTDB'])
    dblist = myclient.list_database_names()
    current_app.logger.info(dblist)
    #
    mymongodb = current_app.config['MONGO_DATABASE']

    if mymongodb in dblist:
        print("DB already exist!")
        print("Delete DB First:" + mymongodb)
        myclient.drop_database(mymongodb)
    else:
        print("Create new database!")
        # ADD user to admin, for new database connection
    print("Create new admin user!")
    myclient.admin.add_user(str(current_app.config['MONGO_DATABASE_ADMIN_USER']),str(current_app.config['MONGO_DATABASE_PASSWD']), roles=[{'role': 'readWrite', 'db': mymongodb}])
    # myclient.admin.add_user('oriyaoflask',
    #                         'changeme_123', roles=[{'role': 'readWrite', 'db': mymongodb}])
    # Connect to new databse
    my_mongo_db = myclient[mymongodb]
    # Create collection for users
    collection_users = my_mongo_db["oriyao_users"]
    # Create default admin user document
    default_admin = {"name": current_app.config['MONGO_DATABASE_USER'],
                     "email": current_app.config['MONGO_DATABASE_EMAIL'],
                     "password": current_app.config['MONGO_DATABASE_PASSWD'],
                     "is_admin": 'True',
                     "is_locked": 'False',
                     "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                     "last_login_time": ''
                     }
    collection_users.insert_one(default_admin)
    collection_list = my_mongo_db.list_collection_names()
    users = collection_users.find_one({"name": current_app.config['MONGO_DATABASE_USER']})
    print(dblist)
    print(collection_list)
    print(users)

def initial_quota():
    current_app.logger.info('Initial my quota.')
    mymongodb = current_app.config['MONGO_DATABASE']
    myclient = pymongo.MongoClient(current_app.config['MONGO_URI_WITHOUTDB'])
    my_mongo_db = myclient[mymongodb]
    collection_quota = my_mongo_db["quota"]
    default_quota = {"username": 'Anonymous',
                     "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                     "quota": 'Some ideas!',
                     "description":'Some description!',
                     "is_delete":'False'
                     }
    collection_quota.insert_one(default_quota)
    quotas = collection_quota.find_one({"username": 'Anonymous'})
    print(quotas)
