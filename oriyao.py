"""
# coding:utf-8
@Time    : 2021/01/03
@Author  : oriyao
@mail    : ylzhangyao@gmail.com
@File    : oriyao.py
@Describe: for flask container initial
"""
from oriyao import create_app

# Two default type of app : development or production

app = create_app('development')
