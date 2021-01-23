# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_cancel_bet 1'] = {
    'data': {
        'createBet': {
            'bet': {
                'id': '1'
            },
            'ok': True
        }
    }
}

snapshots['test_cancel_bet 2'] = {
    'data': {
        'cancelBet': {
            'bet': {
                'id': '1'
            },
            'ok': True
        }
    }
}

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

snapshots['test_create_bet 2'] = {
    'data': {
        'takePosition': {
            'bet': {
                'id': '1'
            },
            'ok': True
        }
    }
}

snapshots['test_say_bet 1'] = {
    'data': {
        'createBet': {
            'bet': {
                'id': '1'
            },
            'ok': True
        }
    }
}

snapshots['test_say_bet 2'] = {
    'data': {
        'sayBetChat': {
            'message': {
                'id': '1'
            },
            'ok': True
        }
    }
}
