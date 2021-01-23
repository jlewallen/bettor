import pytest
import testing


@pytest.mark.asyncio
async def test_create_group(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        await te.execute(
            """
    mutation {
        createGroup(payload: { name: "Group", members: [] }) {
            group {
                id
                name
                members { id }
            }
            ok
        }
    }"""
        )
    )
