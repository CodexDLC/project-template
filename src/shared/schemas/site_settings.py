from pydantic import BaseModel, Field


class SiteSettingsSchema(BaseModel):
    """
    Pydantic-схема для настроек сайта.
    Обеспечивает типизацию и валидацию данных из Redis.
    """

    company_name: str = Field(default="My Project")
    site_base_url: str = Field(default="http://localhost:8000/")
    logo_url: str = Field(default="/static/img/logo.webp")

    # Контакты
    phone: str = Field(default="+1 234 567 890")
    email: str = Field(default="info@example.com")
    address: str = Field(default="")
    working_hours: str = Field(default="Mo-Fr: 09:00 - 18:00")

    # Соцсети & Мессенджеры
    instagram_url: str | None = None
    facebook_url: str | None = None
    telegram_channel_url: str | None = None
    telegram_client_bot_url: str | None = None
    whatsapp_url: str | None = None

    # SEO & Metadata
    meta_title: str = Field(default="")
    meta_description: str = Field(default="")
    favicon_url: str = Field(default="/static/img/favicon.ico")

    # Технические настройки Bot/Worker
    telegram_admin_channel_id: str | None = None
    telegram_technical_bot_username: str | None = None
    telegram_notification_topic_id: int | None = None
    telegram_topics: dict[str, int] = Field(default_factory=dict)

    # Пути для уведомлений (используются в Worker/Bot)
    url_path_confirm: str = Field(default="/booking/confirm/{token}/")
    url_path_cancel: str = Field(default="/booking/cancel/{token}/")
    url_path_reschedule: str = Field(default="/booking/reschedule/")
    url_path_contact_form: str = Field(default="/contacts/")
