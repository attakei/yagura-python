from textwrap import dedent

from slackweb import Slack

from yagura.monitors.models import StateHistory
from yagura.notifications.models import SlackRecipient


class SlackNotifier(object):
    def __init__(self, recipient: SlackRecipient):
        self.recipient: SlackRecipient = recipient
        self.slack = Slack(self.recipient.url)

    def send(
        self,
        current_state: StateHistory,
        base_url: str=None,
    ):
        # Build message
        site = self.recipient.site
        message = dedent(f"""\
            <!here> *Yagura notification: Site state is changed*
            - URL: {site.url}
            - Status: {current_state.state}
            - History: {base_url}{site.get_absolute_url()}
        """)
        if self.recipient.channel:
            self.slack.notify(text=message, channel=self.recipient.channel)
        else:
            self.slack.notify(text=message)
