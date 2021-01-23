# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_group 1'] = {
    'data': {
        'createGroup': {
            'group': {
                'id': '1',
                'name': 'Group'
            },
            'ok': True
        }
    }
}
