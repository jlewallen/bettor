# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_bet 1'] = {
    'data': {
        'createBet': {
            'bet': {
                'id': '1'
            },
            'ok': True
        }
    }
}
