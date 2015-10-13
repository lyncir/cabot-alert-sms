# -*- coding: utf8 -*-
import logging
from logging import handlers
import requests
from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
from cabot.cabotapp.models import UserProfile
from django.conf import settings
from django.template import Context, Template


handler = handlers.TimedRotatingFileHandler('/var/log/cabot_alert_sms.log')
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger('cabot_alert_sms')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sms_template = "Service {{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}is back to normal{% else %}reporting {{ service.overall_status }} status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}"


def send_sms(mobile, message):
    # a http sms api
    url = 'http://sms.example.com/api/send'

    data = {
        'username': 'username',
        'password': 'password',
        'mobiles': mobile,
        'message': message
        }

    requests.post(url, data=data)


class SmsAlert(AlertPlugin):
    name = "SMS"
    author = "Lyncir"

    def send_alert(self, service, users, duty_officers):
        try:
            mobiles = [u.profile.mobile_number for u in users if u.profile.mobile_number]
            if not mobiles:
                return

            c = Context({
                'service': service,
                'host': settings.WWW_HTTP_HOST,
                'scheme': settings.WWW_SCHEME,
            })
            message = Template(sms_template).render(c)
            for mobile in mobiles:
                try:
                    logger.info('Send sms to: %s' % mobile)
                    send_sms(mobile, message)
                except Exception, e:
                    logger.error('Error sending sms: %s' % e)
        except Exception, e:
            logger.error(e)
