from app.models import SiteSettings

def get_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        from app import db
        db.session.add(settings)
        db.session.commit()
    return settings
