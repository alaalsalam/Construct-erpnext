from construct_erpnext.notification_readiness.notification_utils import ensure_default_reminder_settings


def after_migrate():
	ensure_default_reminder_settings()
