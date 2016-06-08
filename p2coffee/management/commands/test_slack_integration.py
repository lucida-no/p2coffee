import json
import time
from django.core.management import BaseCommand, CommandError
from p2coffee import slack


class Command(BaseCommand):
    def handle(self, **kwargs):
        channels = slack.channels_list()['channels']

        for channel in channels:
            if 'im-a-coffeepot' == channel['name']:
                channel_id = channel['id']
                break
        else:  # no break
            raise CommandError("Couldn't find the coffee channel :(")

        text = "Hei, jeg er den nye kaffetrakterboten! Jeg håper at jeg ikke vekker noen med mine beskjeder :)"

        post_response = slack.chat_post_message(channel_id, text)
        print(json.dumps(post_response, indent=4))
        msg_ts = post_response['ts']

        time.sleep(15)
        update_response = slack.chat_update(channel_id, msg_ts, 'Ignorer meg, men...'+text)
        print(json.dumps(update_response, indent=4))

        time.sleep(15)
        delete_response = slack.chat_delete(channel_id, msg_ts)
        print(json.dumps(delete_response, indent=4))

