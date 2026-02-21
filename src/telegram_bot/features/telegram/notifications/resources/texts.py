from html import escape
from typing import cast

from aiogram_i18n import I18nContext

from src.shared.utils.text import sanitize_for_sms, transliterate


class NotificationsTexts:
    """
    Текстовые константы для фичи Notifications.
    """

    @staticmethod
    def get_i18n():
        return cast("I18nContext", I18nContext.get_current())

    # === Тексты для Telegram (динамические) ===
    @classmethod
    def title(cls):
        return cls.get_i18n().notifications.title()

    @classmethod
    def description(cls):
        return cls.get_i18n().notifications.description()

    @classmethod
    def status_approved(cls):
        return cls.get_i18n().notifications.status.approved()

    @classmethod
    def status_rejected(cls):
        return cls.get_i18n().notifications.status.rejected()

    @classmethod
    def prompt_select_reason(cls):
        return cls.get_i18n().notifications.prompt.select.reason()

    @classmethod
    def alert_approved(cls):
        return cls.get_i18n().notifications.alert.approved()

    @classmethod
    def alert_rejected(cls):
        return cls.get_i18n().notifications.alert.rejected()

    @classmethod
    def alert_cancelled(cls):
        return cls.get_i18n().notifications.alert.cancelled()

    @classmethod
    def alert_deleted(cls):
        return cls.get_i18n().notifications.alert.deleted()

    @classmethod
    def error_api(cls):
        return cls.get_i18n().notifications.error.api()

    @classmethod
    def error_contact_not_found(cls):
        # Исправлено: прямой доступ к contact_notfound, чтобы избежать конфликта с ключевым словом 'not'
        return cls.get_i18n().notifications.error.contact_notfound()

    # === Тексты для Email-уведомлений (Base) ===
    # Эти тексты можно переопределить через локализацию или настройки
    EMAIL_REJECT_REASON_BUSY = "Unfortunately, the requested time is already taken. Please choose another time."
    EMAIL_REJECT_REASON_ILL = "Unfortunately, the appointment must be rescheduled."
    EMAIL_REJECT_REASON_MATERIALS = "Unfortunately, we are currently missing necessary materials for this service."
    EMAIL_REJECT_REASON_BLACKLIST = "Unfortunately, we cannot accept your request at this time."

    @staticmethod
    def get_sms_confirm_text(first_name: str, date: str, time: str, site_name: str = "Our Team") -> str:
        """
        Универсальный текст для SMS/WhatsApp уведомления.
        """
        clean_name = sanitize_for_sms(first_name, max_length=30)
        clean_name = transliterate(clean_name)

        clean_date = sanitize_for_sms(date, max_length=10)
        clean_time = sanitize_for_sms(time, max_length=5)

        return f"Hello {clean_name}, your appointment on {clean_date} at {clean_time} at {site_name} is confirmed. We look forward to seeing you!"

    EMAIL_CONFIRM_TAG = "CONFIRMATION"
    EMAIL_CONFIRM_SUBJECT = "Appointment Confirmation - {site_name}"
    EMAIL_CONFIRM_BODY = "Thank you for your booking. Your appointment has been successfully confirmed."

    EMAIL_CANCEL_TAG = "CANCELLATION"
    EMAIL_CANCEL_SUBJECT = "Appointment Cancellation - {site_name}"
    EMAIL_CANCEL_BODY = "Unfortunately, we have to cancel your appointment. We apologize for the inconvenience."

    @staticmethod
    def get_email_greeting(first_name: str, last_name: str, visits_count: int | str) -> str:
        try:
            v_count = int(visits_count)
        except (ValueError, TypeError):
            v_count = 0

        if v_count == 0:
            full_name = f"{first_name} {last_name}".strip()
            return f"Sehr geehrte/r {escape(full_name)},"
        elif 1 <= v_count <= 4:
            return f"Liebe/r {escape(first_name)},"
        else:
            return f"Hallo {escape(first_name)},"
