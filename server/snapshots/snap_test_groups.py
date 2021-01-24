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
                'id': '2',
                'members': [
                    {
                        'id': '2'
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
                'id': '1'
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
                    'id': '2',
                    'name': 'Lori Singleton',
                    'picture': None
                },
                'id': '1',
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
        'createBet': {
            'bet': {
                'id': '1'
            },
            'ok': True
        }
    }
}

snapshots['test_query_groups 2'] = {
    'data': {
        'groups': [
            {
                'allBets': [
                    {
                        'author': {
                            'email': 'marktaylor@gmail.com',
                            'id': '2',
                            'name': 'Lori Singleton'
                        },
                        'canCancel': True,
                        'canDispute': True,
                        'canPay': True,
                        'canTake': False,
                        'details': 'New bet!',
                        'expired': False,
                        'expiresAt': '2012-01-14T00:01:00',
                        'group': {
                            'id': '1'
                        },
                        'id': '1',
                        'messages': [
                        ],
                        'positions': [
                            {
                                'canCancel': True,
                                'canDispute': True,
                                'canPay': True,
                                'canTake': False,
                                'id': '1',
                                'title': 'Bettor',
                                'userPositions': [
                                    {
                                        'state': 'TAKEN',
                                        'user': {
                                            'email': 'marktaylor@gmail.com',
                                            'id': '2',
                                            'name': 'Lori Singleton'
                                        }
                                    }
                                ]
                            },
                            {
                                'canCancel': False,
                                'canDispute': False,
                                'canPay': False,
                                'canTake': True,
                                'id': '2',
                                'title': 'Takers',
                                'userPositions': [
                                ]
                            }
                        ],
                        'state': 'OPEN',
                        'title': 'New bet!'
                    }
                ],
                'name': 'Group'
            }
        ]
    }
}
