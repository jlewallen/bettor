# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_examples 1'] = {
    'data': {
        'createExamples': {
            'ok': True
        }
    }
}

snapshots['test_create_group 1'] = {
    'data': {
        'createGroup': {
            'group': {
                'id': '5',
                'members': [
                    {
                        'id': '35'
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
                    'id': '68',
                    'name': 'Lori Singleton',
                    'picture': None
                },
                'id': '2',
                'message': 'Hello, there'
            }
        ]
    }
}

snapshots['test_invite_no_user 1'] = {
    'data': {
        'invite': {
            'ok': False
        }
    }
}

snapshots['test_invite_user 1'] = {
    'data': {
        'invite': {
            'ok': True
        }
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
