from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,StringField,TextAreaField,SubmitField,RadioField,IntegerField,SelectField,DateField,FloatField,DateTimeField
from wtforms.validators import DataRequired,Length,Regexp,NumberRange,EqualTo
import datetime
import time
## login and registration


class LoginForm(FlaskForm):
    username = TextField('Username', id='username_login')
    password = PasswordField('Password', id='pwd_login')


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create')
    email = TextField('Email')
    password = PasswordField('Password', id='pwd_create')

class DayQuota(FlaskForm):
    # username = TextField('Username', id='username_login')
    username = StringField(u'用户名',
                            validators=[DataRequired(message='用户名不能为空'),
                                        Length(min=1, max=16, message='用户名长度限定在1-16位之间'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='用户名只能包含数字、字母以及下划线.')],
                            render_kw={'placeholder': '请输入用户名长度1-8之间'})
    content = TextAreaField(u'每日一句',
                            validators=[
                                Length(min=3, max=200, message='3到200位之间')],
                            render_kw={'class': 'form-control','placeholder': '不超过200个字符'}
                            )
    quota = TextAreaField(u'感悟',
                          validators=[Length(min=3, max=200, message='3到200位之间')],
                          render_kw={'class': 'form-control','placeholder': '不超过200个字符'})
    submit = SubmitField(u'发布', render_kw={'class': 'btn btn-secondary'})

class GamesForm(FlaskForm):
    username = StringField(u'用户名',validators=[DataRequired()],render_kw={'placeholder': '请输入用户名长度1-8之间'})
    name_cn = StringField(u'中文名',validators=[DataRequired()],render_kw={'placeholder': '请输入中文名'})
    name_en = StringField(u'English Name',validators=[DataRequired()],render_kw={'placeholder': 'Input English Name'})    
    # 平台
    vendor = RadioField('Platform',choices=[('NS','Nintendo Switch'),('PS','PlayStation'),('XBOX','Xbox Seres')],validators=[DataRequired()],default='NS')
    # 评分
    grade = IntegerField('评分',validators=[NumberRange(min=0,max=100)],default=60)
    # 状态
    status = SelectField('状态',choices=[('hold','已购'),('wish','待购')],default='wish')

    # 价格
    floor_price = FloatField('史低价格',default=300)
    purchase_price = FloatField('购买价格',default=300)

    # 发布时间
    deftime=datetime.datetime.today()
    publish_time =DateTimeField('发布时间',format='%Y-%m-%d',default=deftime)
    finishing_time =DateTimeField('结束时间',format='%Y-%m-%d',default=deftime)
    purchase_time =DateTimeField('买入时间',format='%Y-%m-%d',default=deftime)
    finishing_time =DateTimeField('结束时间',format='%Y-%m-%d',default=deftime)
    selling_time =DateTimeField('卖出时间',format='%Y-%m-%d',default=deftime)
    submit = SubmitField(u'添加', render_kw={'class': 'btn btn-secondary'})

