"""Celery worker application."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "rfp_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.autodiscover_tasks(["app.ingestion", "app.knowledge_base", "app.rag", "app.export"])
