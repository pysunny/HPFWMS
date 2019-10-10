# 使用celery
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HPFWMS.settings')
django.setup()

# 创建celery对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')

# 定义任务函数
@app.task
def send_email_active_email(to_email, username, token):
    # 发送激活邮件
    subject = 'HPFWMS邮箱激活'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_massage = '<h1>%s,欢迎你注册HPFWMS</h1>请点击一下链接激活你的账号<br/><a href="http://hufcor.xyz/user/emailactive/%s">点击激活</a>'%(username, token)
    send_mail(subject, message, sender, receiver, html_message=html_massage)
    
@app.task
def send_register_email(email, username, use_id):
    # 发送激活邮件
    subject = 'HPFWMS用户激活'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = ['sunnywu@hufcor.com']
    html_massage = '<h1>用户名：%s<br/>注册电邮：%s<br/>进行HPFWMS注册</h1>请添加权限,并请点击一下链接激活账号<br/><a href="http://hufcor.xyz/user/active/%s">点击激活</a>'%(username, email, use_id)
    send_mail(subject, message, sender, receiver, html_message=html_massage)
