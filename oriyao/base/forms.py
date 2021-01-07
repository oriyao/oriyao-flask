from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,Regexp
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
