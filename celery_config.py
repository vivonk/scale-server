from celery import Celery

app = Celery('upload_task', broker='redis://redis:6379/0',
             include=['src.runner.upload_task', 'src.runner.export_task', 'src.runner.import_task'],
             backend='redis://redis:6379/0')
# TODO :: localhost replace
