"""
# coding:utf-8
@Time    : 2021/01/03
@Author  : oriyao
@mail    : ylzhangyao@gmail.com
@File    : __init__.py
@Describe: main
"""

from flask import jsonify, render_template, redirect, request, url_for,current_app
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from oriyao import mongo, login_manager
from oriyao.base import blueprint
from oriyao.base.forms import LoginForm, CreateAccountForm, DayQuota,GamesForm,MortgageForm
from oriyao.base.models import Mongouser
import time




@blueprint.route('/main_page')
def main_page():
    return render_template('main/main_home.html')











@blueprint.route('/', methods=['GET', 'POST'])
def route_default():
    current_app.logger.warning('redirect to homepage')
    collection_statistics = mongo.db['statistics']
    condition = {'date':time.strftime("%Y-%m-%d", time.localtime())}
    visitstatistics = collection_statistics.find_one(condition)
    if visitstatistics is None:
        default_statistic = {
            "name":'oriyao',
            "date":time.strftime("%Y-%m-%d", time.localtime()),
            "visitstatistics": 1,
            "commentstatistics": 0,
            "likestatistics": 0
            }
        collection_statistics.insert_one(default_statistic)
    else:
        visitstatistics['visitstatistics'] += 1
        collection_statistics.update(condition,visitstatistics)

    if 'login' in request.form:
        fullname = request.form['fullname']
    return render_template('main.html')


@blueprint.route('/games-show')
def route_games_show():
    collection_games = mongo.db['games']
    games = collection_games.find().sort('update_time',-1)
    return render_template('games.html',games=games)

@blueprint.route('/games-add', methods=['GET', 'POST'])
@login_required
def route_gamesadd():
    games_form = GamesForm(request.form)
    if request.method == "GET":
        if current_user.is_authenticated:
            games_form.username.data = current_user.username
        return render_template('games_add.html', games_form=games_form)
    if games_form.validate_on_submit():
        username = games_form.username.data
        vendor = games_form.vendor.data
        quotadate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        current_app.logger.info('Games ADD:' + str(vendor))
        if mongo_save_games(games_form):
            return redirect(url_for('base_blueprint.route_games_show'))
        else:
            return render_template('games_add.html', games_form=games_form)
    return render_template('games_add.html', games_form=games_form)

@blueprint.route('/mortgage-add', methods=['GET', 'POST'])
@login_required
def route_mortgage_add():
    mortgage_form = MortgageForm(request.form)
    mortgage_collection = mongo.db['mortgage']
    laste = mortgage_collection.find().count()
    mortgage = mortgage_collection.find_one({'periods':laste})

    if request.method == "GET":
        mortgage_form.periods.data = mortgage['periods'] + 1
        mortgage_form.debt.data= mortgage['debt']
        mortgage_form.debt.data= mortgage['debt']
        mortgage_form.principal.data= mortgage['principal']
        mortgage_form.interest.data= mortgage['interest']
        return render_template('mortgage_add.html', mortgage_form=mortgage_form)
    if mortgage_form.validate_on_submit():
        if mongo_save_mortgage(mortgage_form):
            return redirect(url_for('base_blueprint.route_mortgage_add'))
        else:
            return render_template('mortgage_add.html', mortgage_form=mortgage_form)
    return render_template('mortgage_add.html', mortgage_form=mortgage_form)


@blueprint.route('/quota', methods=['GET', 'POST'])
def route_quota():
    DayQuota_form = DayQuota(request.form)
    quotas = get_quotas()
    if request.method == "GET":
        DayQuota_form.username.data = 'Anonymous'
        if current_user.is_authenticated:
            DayQuota_form.username.data = current_user.username
        return render_template('quota.html', DayQuota_form=DayQuota_form,quotas=quotas)
    if DayQuota_form.validate_on_submit():
        username = DayQuota_form.username.data
        content = DayQuota_form.content.data
        quota = DayQuota_form.quota.data
        quotadate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mongo_save_messages(quotadate, username, content, quota)
        return render_template('quota.html', DayQuota_form=DayQuota_form,quotas=quotas)
    return render_template('quota.html', DayQuota_form=DayQuota_form,quotas=quotas)

@blueprint.route('/quota-show')
def route_quota_show():
    collection_quotas = mongo.db['quota']
    quotas = collection_quotas.find().sort('quotadate',-1)
    return render_template('quota_show.html',quotas=quotas)

def mongo_save_games(games_form):
    current_app.logger.info('Add an new game in games collection')
    games_collection = mongo.db['games']
    game_content = {
            "username":games_form.username.data,
            "name_cn":games_form.name_cn.data,
            "name_en":games_form.name_en.data,
            "vendor":games_form.vendor.data,
            "grade":games_form.grade.data,
            "status":games_form.status.data,
            "floor_price":games_form.floor_price.data,
            "purchase_price":games_form.purchase_price.data,
            "publish_time":games_form.publish_time.data,
            "finishing_time":games_form.finishing_time.data,
            "purchase_time":games_form.purchase_time.data,
            "selling_time":games_form.selling_time.data
            }
    games_collection.insert_one(game_content)
    return True



def mongo_save_mortgage(mortgage_form):
    mortgage_collection = mongo.db['mortgage']
    mortgage_content = {"periods": mortgage_form.periods.data,
        "status": mortgage_form.status.data,
        "due_date": mortgage_form.due_date.data.strftime("%Y-%m-%d"),
        "payment": mortgage_form.payment.data,
        "principal": mortgage_form.principal.data,
        "interest": mortgage_form.interest.data,
        "actual-payment": mortgage_form.actual_payment.data,
        "debt": mortgage_form.debt.data,                        
        "notes": mortgage_form.notes.data,
        "update": mortgage_form.update.data.strftime("%Y-%m-%d")}
    mortgage_collection.insert_one(mortgage_content)
    return True


def mongo_save_messages(quotadate,username,content,quota):
    quota_collection = mongo.db['quota']
    quota_content = {"quotadate": quotadate, "username":username, "content": content, "quota": quota}
    quota_collection.insert_one(quota_content)
    return 'OK'
 

def get_quotas():
    collection_quotas = mongo.db['quota']
    quotas = collection_quotas.find().sort('quotadate',-1)
    return quotas




@blueprint.route('/<template>')
@login_required
def route_template(template):

    return render_template(template + '.html')


@blueprint.route('/fixed_<template>')
@login_required
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login & Registration
@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)

    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        current_app.logger.warning(username)
        current_app.logger.warning(password)
        collection_users = mongo.db['oriyao_users']
        users = collection_users.find_one({"name": username})
        current_app.logger.info('Mongodb user login')
        current_app.logger.info(users)
        if users and Mongouser.check_password(password, users['password']):
            user_obj = Mongouser(username=users['name'])
            current_app.logger.info(user_obj)
            current_app.logger.info('登录成功')
            login_user(user_obj)
            return redirect(url_for('home_blueprint.index'))
        return render_template('login/login.html',login_form=login_form,create_account_form=create_account_form,message='Wrong User or Password')
    if not current_user.is_authenticated:
        return render_template('login/login.html',login_form=login_form,create_account_form=create_account_form)
    return redirect(url_for('home_blueprint.index'))

# @blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm(request.form)
#     create_account_form = CreateAccountForm(request.form)
#     if 'login' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and checkpw(password.encode('utf8'), user.password):
#             login_user(user)
#             return redirect(url_for('base_blueprint.route_default'))
#         return render_template('errors/page_403.html')
#     if not current_user.is_authenticated:
#         return render_template(
#             'login/login.html',
#             login_form=login_form,
#             create_account_form=create_account_form
#         )
#     return redirect(url_for('home_blueprint.index'))


@blueprint.route('/create_user', methods=['POST'])
def create_user():
    user = User(**request.form)
    db.session.add(user)
    db.session.commit()
    return jsonify('success')


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.route_default'))


@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'





## Statistics
@blueprint.route('/loveme')
def loveme():
    collection_statistics = mongo.db['statistics']
    condition = {'date':time.strftime("%Y-%m-%d", time.localtime())}
    likestatistics = collection_statistics.find_one(condition)
    if likestatistics is None:
        default_statistic = {
            "name":'oriyao',
            "date":time.strftime("%Y-%m-%d", time.localtime()),
            "visitstatistics": 1,
            "commentstatistics": 0,
            "likestatistics": 0
        }
        collection_statistics.insert_one(default_statistic)
    else:
        likestatistics['likestatistics'] += 1
        collection_statistics.update(condition,likestatistics)
    return render_template('main.html')






## Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
