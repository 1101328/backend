from common.messaging.celery import celery_app
from celery.result import AsyncResult

async_result = AsyncResult("34e43f07-e5af-4387-a422-fc4472a7a2bc", app=celery_app)
print(async_result.get())
