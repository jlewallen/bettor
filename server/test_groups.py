import pytest
import testing
import freezegun


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
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


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_query_groups(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        await te.execute(
            """
    query {
        groups {
            name
            allBets {
                id
                title
                details
                createdAt
                expiresAt
                state
                expired
                author {
                    id
                    name
                    email
                }
                group {
                    id
                }
                positions {
                    id
                    title
                    userPositions {
                    user { id name email }
                        createdAt
                        state
                    }
                }
                messages {
                    id
                }
            }
        }
    }"""
        )
    )


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_group_chat_hello(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        await te.execute(
            """
    mutation {
        sayGroupChat(payload: { groupId: 2, message: "Hello, there" }) {
            message { id }
            ok
        }
    }"""
        )
    )


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_group_chat_hello_and_query(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        await te.execute(
            """
    mutation {
        sayGroupChat(payload: { groupId: 2, message: "Hello, there" }) {
            message { id }
            ok
        }
    }"""
        )
    )

    snapshot.assert_match(
        await te.execute(
            """
        query {
            groupChat(groupId: 2, page: 0) {
                id
                message
                author { id name picture }
            }
        }"""
        )
    )
