from django.core.management import call_command
from django.utils.six import StringIO


def run_command(command: str, *args):
    out = StringIO()
    err = StringIO()
    call_command(command, *args, stdout=out, stderr=err)
    return out, err
