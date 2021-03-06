import logging
import pytest
import testing
import freezegun


import models


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_create_group(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
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

    assert reply["data"]["createGroup"]["ok"] == True


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_query_groups(snapshot):
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

    snapshot.assert_match(
        reply := await te.execute(
            """
    query {
        groups {
            name
            allBets {
                id
                title
                details
                expiresAt
                canTake
                canCancel
                canPay
                canDispute
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
                    canTake
                    canCancel
                    canPay
                    canDispute
                    userPositions {
                        user { id name email }
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
        reply := await te.execute(
            """
    mutation {
        sayGroupChat(payload: { groupId: "%s", message: "Hello, there" }) {
            message { id }
            ok
        }
    }"""
            % (te.group.id,)
        )
    )

    assert reply["data"]["sayGroupChat"]["ok"] == True


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_group_chat_hello_and_query(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        sayGroupChat(payload: { groupId: "%s", message: "Hello, there" }) {
            message { id }
            ok
        }
    }"""
            % (te.group.id,)
        )
    )

    assert reply["data"]["sayGroupChat"]["ok"] == True

    snapshot.assert_match(
        reply := await te.execute(
            """
        query {
            groupChat(groupId: "%s", page: 0) {
                id
                message
                author { id name picture }
            }
        }"""
            % (te.group.id,)
        )
    )


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_invite_no_user(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        invite(payload: { groupId: "%s", email: "stephen@example.com" }) {
            ok
        }
    }"""
            % (te.group.id,)
        )
    )

    assert reply["data"]["invite"]["ok"] == False


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_invite_user(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        invite(payload: { groupId: "%s", email: "%s" }) {
            ok
        }
    }"""
            % (te.group.id, te.users[-1].email)
        )
    )

    assert reply["data"]["invite"]["ok"] == True


@pytest.mark.asyncio
@freezegun.freeze_time("2012-01-14")
async def test_create_examples(snapshot):
    te = testing.TestEnv()
    snapshot.assert_match(
        reply := await te.execute(
            """
    mutation {
        createExamples {
            ok
        }
    }"""
        )
    )

    assert reply["data"]["createExamples"]["ok"] == True
