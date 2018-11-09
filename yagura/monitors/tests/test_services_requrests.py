"""Test case for yagura.monitors.services.monitor_site_requests
"""
import logging
from unittest import mock

from requests.exceptions import ConnectionError
from requests_mock import Mocker

from yagura.monitors.services import monitor_site_requests


def test_monitor_site_requests__expected_request_200(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 200
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    with Mocker() as mocked:
        mocked.get(url, status_code=status_code)
        result, reason = event_loop.run_until_complete(
            monitor_site_requests(site))
        assert result == 'OK'
        assert reason == ''
        assert caplog.records[0].msg == 'Start to check: http://example.com/'


def test_monitor_site_requests__expected_request_404(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 404
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    with Mocker() as mocked:
        mocked.get(url, status_code=status_code)
        result, reason = event_loop.run_until_complete(
            monitor_site_requests(site))
        assert result == 'OK'
        assert reason == ''
        assert caplog.records[0].msg == 'Start to check: http://example.com/'


def test_monitor_site_requests__ng_response_with_reason(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 302
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    with Mocker() as mocked:
        mocked.get(url, status_code=200)
        result, reason = event_loop.run_until_complete(
            monitor_site_requests(site))
        assert result == 'NG'
        assert reason == 'HTTP status code is 200 (expected: 302)'
        assert caplog.records[0].msg == 'Start to check: http://example.com/'


def test_monitor_site_requests__ng_multiple(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with Mocker() as mocked:
        mocked.get(site.url, status_code=200)
        result, reason = event_loop.run_until_complete(
            monitor_site_requests(site, 3))
        assert result == 'NG'
        assert reason == 'HTTP status code is 200 (expected: 302)'
        assert len(mocked.request_history) == 3


def test_monitor_site_requests__ok_once_retry(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=200)
    with Mocker() as mocked:
        mocked.register_uri(
            'GET', site.url,
            [
                {'status_code': 503},
                {'status_code': 200},
                {'status_code': 200},
            ]
        )
        result, reason = event_loop.run_until_complete(
            monitor_site_requests(site, 3))
        assert result == 'OK'
        print(mocked.request_history[0])
        assert len(mocked.request_history) == 2


def test_monitor_site_requests__urlerror(event_loop):
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with Mocker() as mocked:
        mocked.get(site.url, exc=ConnectionError('Test error'))
        result, reason = event_loop.run_until_complete(
            monitor_site_requests(site))
        assert result == 'NG'
        assert reason == 'ConnectionError occurred: Test error'
