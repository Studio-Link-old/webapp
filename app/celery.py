from __future__ import absolute_import

from celery import Celery
from datetime import timedelta

celery = Celery('app.celery',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0',
                include=['app.tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TIMEZONE = 'UTC',
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
            'task': 'app.tasks.periodic_status_update',
            'schedule': timedelta(seconds=30)
            },
        }

)

if __name__ == '__main__':
    celery.start()  # pragma: no cover
