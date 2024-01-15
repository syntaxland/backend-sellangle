from celery import shared_task

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"

@shared_task(bind=True)
def send_mail_func(self):
    x = 1
    x += 1
    print("Calculating...")
    return "x += 1: " + str(x)



 
"""
celery -A backend_drf.celery worker --pool=solo -l info 
(Windows)
celery -A backend_drf.celery worker --loglevel=info 
(Unix) 
celery -A backend_drf.celery beat --loglevel=info
"""

