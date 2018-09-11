import random,logging

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from meiduo.libs.yuntongxun.sms import CCP
from . import constants


# 日志输出器
logger = logging.getLogger('django')


# 路径传参，正则匹配电话号码，省区校验 url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
class SMSCodeView(APIView):
    """短信验证码"""
    def get(self,request,mobile):
        # 生成验证码
        sms_code = "%06d"%random.randint(0,999999)
        logger.info(sms_code)
        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # save
        redis_conn.setex('sms_%s'%mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        # send_msg
        # CCP().send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES//60],1)
        # return
        return Response({'message':'OK'})