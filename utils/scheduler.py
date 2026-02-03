from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone
from db.tables.schedule import Schedule, ScheduleStatus
from utils.rabbitmq import RabbitMQManager
from utils.logger import get_logger

logger = get_logger("CronScheduler")
scheduler = AsyncIOScheduler()

async def check_and_dispatch_tasks():
    """
    The second-level cron job.
    Finds all active schedules where next_run_at <= now.
    """
    now = datetime.now(timezone.utc)
    
    # 1. Find schedules that are active and due
    due_schedules = await Schedule.find(
        Schedule.status == ScheduleStatus.ACTIVE,
        Schedule.next_run_at <= now
    ).fetch_links() # .fetch_links() is crucial to get Target and User data

    for schedule in due_schedules:
        try:
            # 2. Prepare payload for RabbitMQ
            payload = {
                "schedule_id": str(schedule.id),
                "url": schedule.target.url,
                "method": schedule.target.method,
                "headers": schedule.target.headers,
                "body_template": schedule.target.body_template
            }

            # 3. Push to RabbitMQ
            await RabbitMQManager.publish_task(payload)

            # 4. Calculate next run time and update DB
            # Example: simple interval update. You can use croniter for complex crons.
            schedule.last_run_at = now
            if schedule.interval_seconds:
                from datetime import timedelta
                schedule.next_run_at = now + timedelta(seconds=schedule.interval_seconds)
            
            await schedule.save()
            logger.info(f"Dispatched schedule: {schedule.name}")
            
        except Exception as e:
            logger.error(f"Failed to dispatch schedule {schedule.id}: {e}")

def start_scheduler():
    # Adding a job that runs every 5 seconds (Second-level precision)
    scheduler.add_job(check_and_dispatch_tasks, 'interval', seconds=5)
    scheduler.start()
    logger.info("APScheduler started with 5-second interval check.")