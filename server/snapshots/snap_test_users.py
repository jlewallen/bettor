# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_myself 1'] = {
    'data': {
        'myself': {
            'authoredBets': [
            ],
            'friends': [
            ],
            'groups': [
                {
                    'allBets': [
                    ],
                    'id': '11'
                }
            ],
            'id': '101'
        }
    }
}
