# coding: utf-8

from __future__ import absolute_import
import logging

from .notification import Notification
from .response import Response

from hyper.tls import init_context
from hyper import HTTP20Connection
import ujson


log = logging.getLogger(u"apns2")


MODE_PROD = u"prod"
MODE_DEV = u"dev"


class APNSClient(object):

    def __init__(self, mode, client_cert, password=None):
        if mode == MODE_PROD:
            self.host = u"api.push.apple.com"
        elif mode == MODE_DEV:
            self.host = u"api.development.push.apple.com"
        else:
            raise ValueError(u"invalid mode: {}".format(mode))

        self.conn = HTTP20Connection(
            host=self.host,
            port=443,
            secure=True,
            ssl_context=init_context(cert=client_cert, cert_password=password),
        )

    def get_headers(self, n, topic = None):
        headers = {u"Content-Type": u"application/json; charset=utf-8"}
        if topic:
            headers[u"apns-topic"] = topic
        if n.apns_id:
            headers[u"apns-id"] = n.apns_id
        if n.collapse_id:
            headers[u"apns-collapse-id"] = n.collapse_id
        if n.priority:
            headers[u"apns-priority"] = n.priority
        if n.expiration:
            headers[u"apns-expiration"] = n.expiration
        return headers

    def push(self, n, device_token, topic = None):
        url = u"/3/device/{}".format(device_token)
        payload = n.payload.to_json()
        log.debug(u"Going to send payload: {}".format(payload))
        headers = self.get_headers(n, topic=topic)
        stream_id = self.conn.request(
            method=u"POST", url=url,
            body=payload, headers=headers,
        )
        apns_response = self.conn.get_response(stream_id=stream_id)

        apns_ids = apns_response.headers.get(u"apns-id")
        apns_id = apns_ids[0] if apns_ids else None

        response = Response(status_code=apns_response.status, apns_id=apns_id)

        if apns_response.status != 200:
            body = apns_response.read()
            apns_data = ujson.loads(body)
            response.timestamp = apns_data.get(u"timestamp")
            response.reason = apns_data[u"reason"]

        return response
