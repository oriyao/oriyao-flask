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

def initial_games():
    current_app.logger.info('Initial my games.')
    mymongodb = current_app.config['MONGO_DATABASE']
    myclient = pymongo.MongoClient(current_app.config['MONGO_URI_WITHOUTDB'])
    my_mongo_db = myclient[mymongodb]
    collection_games = my_mongo_db["games"]
    default_games = {"name_en": 'CyberPunk 2077',
		     "name_cn": '赛博朋克2077',
		     "cover":'/app/cyber.png',
		     "platform":'PlayStation',
		     "link":'http://www.openstack.top',
		     "about":'夜之城',
		     "grade":'90',
	             "status":'hold',
		     "floor_price":'225',
		     "purchase_price":'347',
		     "purchase_time":'2020-12-13',
		     "purchase_channel":'淘宝上海彭彭',
		     "publish_time":'2020-12-07',
		     "finishing_time":'2021-01-10',
		     "selling_time":'2021-01-10',
                     "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                     "is_delete":'False'
                     }
    collection_games.insert_one(default_games)
    # games = collection_quota.find_one({"username": 'Anonymous'})
    games = collection_games.find()
    for game in games:
        print(game)
    return "OK"


