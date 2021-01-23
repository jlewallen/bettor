import logging
import pytest
import testing
import freezegun


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
