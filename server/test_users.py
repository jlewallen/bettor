import pytest
import testing


@pytest.mark.asyncio
async def test_myself(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        await te.execute(
            """
    query {
        myself {
            id
            authoredBets {
                id
            }
            groups {
                id
                allBets {
                    id
                    author { id }
                }
            }
            friends {
                id name
            }
        }
    }"""
        )
    )
