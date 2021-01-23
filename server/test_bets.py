import pytest
import testing
import freezegun


@freezegun.freeze_time("2012-01-14")
@pytest.mark.asyncio
async def test_create_bet(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        await te.execute(
            """
    mutation {
        createBet(payload: {
            groupId: 2,
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
        )
    )
