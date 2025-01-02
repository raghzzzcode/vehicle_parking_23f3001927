from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",  # Replace with your Redis URL
        backend="redis://localhost:6379/0",  # Store task results (optional)
    )
    celery.conf.update(app.config)
    return celery
