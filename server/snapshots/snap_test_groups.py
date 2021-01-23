# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_group 1'] = {
    'data': {
        'createGroup': {
            'group': {
                'id': '3',
                'members': [
                    {
                        'id': '13'
                    }
                ],
                'name': 'Group'
            },
            'ok': True
        }
    }
}

snapshots['test_group_chat_hello 1'] = {
    'data': {
        'sayGroupChat': {
            'message': {
                'id': '1'
            },
            'ok': True
        }
    }
}

snapshots['test_group_chat_hello_and_query 1'] = {
    'data': {
        'sayGroupChat': {
            'message': {
                'id': '2'
            },
            'ok': True
        }
    }
}

snapshots['test_group_chat_hello_and_query 2'] = {
    'data': {
        'groupChat': [
            {
                'author': {
                    'id': '46',
                    'name': 'Lori Singleton',
                    'picture': None
                },
                'createdAt': '2021-01-23T08:10:50.657115',
                'id': '2',
                'message': 'Hello, there'
            },
            {
                'author': {
                    'id': '35',
                    'name': 'Lori Singleton',
                    'picture': None
                },
                'createdAt': '2021-01-23T08:10:50.622349',
                'id': '1',
                'message': 'Hello, there'
            }
        ]
    }
}

snapshots['test_query_groups 1'] = {
    'data': {
        'groups': [
            {
                'allBets': [
                ],
                'name': 'Group'
            }
        ]
    }
}
