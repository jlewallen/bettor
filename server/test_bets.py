import logging
import pytest
import testing
import datetime
import freezegun

import models

log = logging.getLogger("bettor")


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_create_bet(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        createBet(payload: {
            groupId: "%s",
            title: "New bet!",
            details: "No details.",
            expiresIn: 60,
            minimumTakers: 0,
            maximumTakers: 3 }) {
            bet {
                id
            }
            ok
        }
    }"""
            % (te.group.id,)
        )
    )

    bet_id = reply["data"]["createBet"]["bet"]["id"]

    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        takePosition(payload: {
            betId: "%s",
            position: "Takers" }) {
            bet {
                id
            }
            ok
        }
    }"""
            % (bet_id,),
            user=te.users[1],
        )
    )


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_cancel_bet(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        createBet(payload: {
            groupId: "%s",
            title: "New bet!",
            details: "No details.",
            expiresIn: 60,
            minimumTakers: 0,
            maximumTakers: 3 }) {
            bet {
                id
            }
            ok
        }
    }"""
            % (te.group.id,)
        )
    )

    bet_id = reply["data"]["createBet"]["bet"]["id"]

    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        cancelBet(payload: { betId: "%s" }) {
            bet {
                id
            }
            ok
        }
    }"""
            % (bet_id,)
        )
    )


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_say_bet(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        createBet(payload: {
            groupId: "%s",
            title: "New bet!",
            details: "No details.",
            expiresIn: 60,
            minimumTakers: 0,
            maximumTakers: 3 }) {
            bet {
                id
            }
            ok
        }
    }"""
            % (te.group.id,)
        )
    )

    bet_id = reply["data"]["createBet"]["bet"]["id"]

    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        sayBetChat(payload: { betId: "%s", message: "Hello, world!" }) {
            message {
                id
            }
            ok
        }
    }"""
            % (bet_id,)
        )
    )


@pytest.mark.asyncio
async def test_bet_last_action(snapshot):
    jacob = models.User(name="Jacob")
    stephen = models.User(name="Stephen")
    carla = models.User(name="Carla")
    group = models.Group(name="Group", members=[jacob, stephen, carla])
    bet = models.Bet.arbitrary(
        title="Bet",
        author=jacob,
        group=group,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
    )
    assert isinstance(bet.action(), models.CreatedAction)

    bet.take(stephen, position="Takers")
    assert isinstance(bet.action(), models.TakeAction)

    bet.take(carla, position="Takers")
    assert isinstance(bet.action(), models.TakeAction)

    bet.cancel(stephen)
    assert isinstance(bet.action(), models.CancelAction)

    bet.pay(carla)
    assert isinstance(bet.action(), models.PaidAction)


@pytest.mark.asyncio
async def test_bet_dispute(snapshot):
    jacob = models.User(name="Jacob")
    stephen = models.User(name="Stephen")
    carla = models.User(name="Carla")
    group = models.Group(name="Group", members=[jacob, stephen, carla])
    bet = models.Bet.arbitrary(
        title="Bet",
        author=jacob,
        group=group,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
    )
    assert isinstance(bet.action(), models.CreatedAction)

    bet.take(stephen, position="Takers")
    assert isinstance(bet.action(), models.TakeAction)

    bet.take(carla, position="Takers")
    assert isinstance(bet.action(), models.TakeAction)

    bet.dispute(carla)
    assert isinstance(bet.action(), models.DisputedAction)

    assert bet.state == models.BetState.DISPUTED


@pytest.mark.asyncio
async def test_bet_paid(snapshot):
    jacob = models.User(name="Jacob")
    stephen = models.User(name="Stephen")
    carla = models.User(name="Carla")
    group = models.Group(name="Group", members=[jacob, stephen, carla])
    bet = models.Bet.arbitrary(
        title="Bet",
        author=jacob,
        group=group,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
    )
    assert isinstance(bet.action(), models.CreatedAction)

    bet.take(stephen, position="Takers")
    assert isinstance(bet.action(), models.TakeAction)

    bet.take(carla, position="Takers")
    assert isinstance(bet.action(), models.TakeAction)

    bet.pay(carla)
    assert isinstance(bet.action(), models.PaidAction)

    assert bet.state == models.BetState.COLLECTING

    bet.pay(stephen)
    assert isinstance(bet.action(), models.PaidAction)

    assert bet.state == models.BetState.PAID
