Cabot SMS Plugin
=====
This is an alert plugin for the cabot service monitoring tool. It allows you to alert users by sms.

### Usage
1. Append cabot_alert_sms to the variable CABOT_PLUGINS_ENABLED in your conf/production.env

2. Edit cabot/settings.py,add a line:
    INSTALLED_APPS = (
	    ...
		'cabot_alert_sms',
		...
		)

3. Add some SQL:
	SELECT * FROM django_content_type WHERE app_label='cabot_alert_sms';
	INSERT INTO cabotapp_alertplugin(polymorphic_ctype_id,title,enabled) VALUE(9,'SMS',1);
	INSERT INTO cabot_alert_sms_smsalert(alertplugin_ptr_id) VALUE(5);
