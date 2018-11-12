"""Test case for yagura.monitors.services.monitor_site_aiohttp
"""
import logging
from unittest import mock

from aiohttp import ClientError
from aioresponses import aioresponses

from yagura.monitors.services import monitor_site_aiohttp


def _call_monitor_site_aiohttp(event_loop, site, mock_url, mock_status):
    with aioresponses() as mocked:
        mocked.get(mock_url, status=mock_status)
        result, reason = event_loop.run_until_complete(
            monitor_site_aiohttp(site))
    return result, reason


def test_monitor_site_aiohttp__expected_request_200(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 200
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    result, reason = _call_monitor_site_aiohttp(
        event_loop, site, url, status_code)
    assert result == 'OK'
    assert reason == ''
    assert caplog.records[0].msg == 'Start to check: http://example.com/'
    assert len(caplog.records) == 3


def test_monitor_site_aiohttp__expected_request_404(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 404
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    result, reason = _call_monitor_site_aiohttp(
        event_loop, site, url, status_code)
    assert result == 'OK'
    assert reason == ''
    assert caplog.records[0].msg == 'Start to check: http://example.com/'
    assert len(caplog.records) == 3


def test_monitor_site_aiohttp__ng_response_with_reason(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    result, reason = _call_monitor_site_aiohttp(
        event_loop, site, site.url, 200)
    assert result == 'NG'
    assert reason == 'HTTP status code is 200 (expected: 302)'
    assert caplog.records[0].msg == 'Start to check: http://example.com/'
    assert len(caplog.records) == 3


def test_monitor_site_aiohttp__ng_multiple(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with aioresponses() as mocked:
        mocked.get(site.url, status=200)
        mocked.get(site.url, status=200)
        mocked.get(site.url, status=200)
        result, reason = event_loop.run_until_complete(
            monitor_site_aiohttp(site, 3))
        assert result == 'NG'
        assert reason == 'HTTP status code is 200 (expected: 302)'
        assert len(mocked._responses) == 3


def test_monitor_site_aiohttp__ok_once_retry(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=200)
    with aioresponses() as mocked:
        mocked.get(site.url, status=503)
        mocked.get(site.url, status=200)
        mocked.get(site.url, status=200)
        result, reason = event_loop.run_until_complete(
            monitor_site_aiohttp(site, 3))
        assert result == 'OK'
        assert len(mocked._responses) == 2


def test_monitor_site_aiohttp__urlerror(event_loop):
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with aioresponses() as mocked:
        mocked.get(site.url, exception=ClientError('Test error'))
        result, reason = event_loop.run_until_complete(
            monitor_site_aiohttp(site))
        assert result == 'NG'
        assert reason == 'ClientError occurred: Test error'


def test_monitor_site_aiohttp__no_message_error(event_loop):
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with aioresponses() as mocked:
        mocked.get(site.url, exception=ClientError(None))
        result, reason = event_loop.run_until_complete(
            monitor_site_aiohttp(site))
        assert result == 'NG'
        assert reason == 'ClientError occurred:'


def test_monitor_site_aiohttp__error_name(event_loop):
    class CustomError(ClientError):
        pass
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with aioresponses() as mocked:
        mocked.get(site.url, exception=CustomError('test'))
        result, reason = event_loop.run_until_complete(
            monitor_site_aiohttp(site))
        assert result == 'NG'
        assert reason == 'CustomError occurred: test'
