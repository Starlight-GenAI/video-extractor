import logging
import os
from google.cloud import pubsub_v1
from config.config import config
from adapter.pubsub_publisher import publish, publish_notification
from model.extract_video_event import ExtractVideoEvent
from model.generate_plan_event import GeneratePlanEvent
from model.notification_event import NotificationEvent
from adapter.youtube_api import get_video_subtitle, download,extract_video_id
from adapter.cloud_storage import create_and_upload, upload
from adapter.auth import init_credential

subscriber = pubsub_v1.SubscriberClient(credentials=init_credential(audience=config.pubsub.subscriber_audience))
subscription_path = subscriber.subscription_path(config.pubsub.project_id, config.pubsub.video_extraction_subscription_id)

FAIL = "failed"
PENDING = "pending"

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    logging.info("start consuming event")
    try:
        data = ExtractVideoEvent(message.data)
        message.ack()
        publish_notification(NotificationEvent(id=data.id, status=PENDING).to_byte())
        logging.info(f"event id {data.id} is processing")
        video_id = extract_video_id(data.video_url)
        subtitle = get_video_subtitle(video_id)
        if data.is_use_subtitle:
            logging.info(f"uploading ...")
            create_and_upload(subtitle=subtitle, object_name=f'{data.id}_{video_id}')
        else:
            logging.info(f"uploading ...")
            create_and_upload(subtitle=subtitle, object_name=f'{data.id}_{video_id}')
            filename = download(url=data.video_url, id=data.id)
            upload(filename)
        publish(GeneratePlanEvent(id=data.id, user_id=data.user_id, is_use_subtitle=data.is_use_subtitle, object_name=f'{data.id}_{video_id}').to_byte())
        logging.info(f"event id {data.id} done")
    except Exception as e:
        logging.error(f'error with {e}')
        publish_notification(NotificationEvent(id=data.id, status=FAIL).to_byte())

def run():
    logging.info("consumer running")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            logging.error("pull data failed")