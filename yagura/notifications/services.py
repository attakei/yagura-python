from textwrap import dedent

from slackweb import Slack

from yagura.monitors.models import StateHistory
from yagura.notifications.models import SlackRecipient
from yagura.sites.models import Site


class SlackNotifier(object):
    def __init__(self, recipient: SlackRecipient):
        self.recipient: SlackRecipient = recipient
        self.slack = Slack(self.recipient.url)

    def send(
        self,
        current_state: StateHistory,
    ):
        # Build message
        site = self.recipient.site
        message = dedent(f"""\
            <!here> *Yagura notification: Site state is changed*
            
            - URL: {site.url}
            - Status: {current_state.state}
            - History: {site.get_absolute_url()}
        """)
        self.slack.notify(text=message)
