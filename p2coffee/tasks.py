from huey.contrib.djhuey import db_task

from p2coffee import slack
from p2coffee.models import SensorEvent, CoffeePotEvent


def on_new_meter(sensor_event):
    assert isinstance(sensor_event, SensorEvent)
    # FIXME values are guesstimates
    start_threshold = 1500
    finish_threshold = 100
    cpe = None

    # Get previous event
    change_events = SensorEvent.objects.filter(name=SensorEvent.NAME_METER_HAS_CHANGED)
    previous_event = change_events.exclude(uuid=sensor_event.uuid).order_by('created').last()

    # Compare current with previous and check if thresholds have been crossed
    if float(sensor_event.value) >= start_threshold > float(previous_event.value):
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_STARTED)
    elif float(sensor_event.value) <= finish_threshold < float(previous_event.value):
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_FINISHED)

    if cpe is not None:
        send_to_slack(cpe)


@db_task()
def send_to_slack(cpe):
    # Notify on Slack
    slack.send_msg(cpe.as_slack_text())
