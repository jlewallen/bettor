#!env/bin/python3

import sys
import logging
import datetime
import jsonpickle

import storage
import models
import gql


def main():
    session = storage.create()

    jacob = models.User(sub="", name="Jacob", email="jacob@example.com")
    stephen = models.User(sub="", name="Stephen", email="stephen@example.com")
    jimmy = models.User(sub="", name="Jimmy", email="jimmy@example.com")
    derek = models.User(sub="", name="Derek", email="derek@example.com")
    zack = models.User(sub="", name="Zack", email="zack@example.com")
    scott = models.User(sub="", name="Scott", email="scott@example.com")

    group = models.Group(
        name="Small Group",
        owner=jacob,
        members=[jacob, stephen, jimmy, derek, zack, scott],
    )

    standard_expiration = datetime.timedelta(minutes=60)
    simple = models.Bet.coin_toss(
        group=group,
        author=jacob,
        expires_at=datetime.datetime.utcnow() + standard_expiration,
    )
    simple.take(jacob, position="heads")
    simple.take(stephen, position="tails")

    jimmy_example = models.Bet.arbitrary(
        title="Derrick Henry over 35 receptions",
        group=group,
        author=stephen,
        expires_at=datetime.datetime.utcnow() + standard_expiration,
    )
    jimmy_example.take(jimmy)

    multiple_takers = models.Bet.arbitrary(
        group=group,
        title="Daniel Jones has more fantasy points than Tom Brady at season end.",
        author=stephen,
        expires_at=datetime.datetime.utcnow() + standard_expiration,
    )
    multiple_takers.take(derek)
    multiple_takers.take(scott)

    session.add(group)
    session.commit()

    g = gql.create()

    query = """
    mutation {
        createGroup(payload: { name: "Hello, world" }) {
            group { id }
            ok
        }
    }
    """

    print(jacob)
    res = g.execute(query, context_value={"session": session, "user": jacob})
    print(jsonpickle.dumps(res, unpicklable=False, indent=4))
    assert res.errors is None

    query = """
    mutation {
        createBet(payload: { title: "New bet!", details: "", expiresIn: 60, groupId: 2 }) {
            bet { id }
            ok
        }
    }
    """
    res = g.execute(query, context_value={"session": session, "user": jacob})
    print(jsonpickle.dumps(res, unpicklable=False, indent=4))
    assert res.errors is None

    query = """
    mutation {
        takePosition(payload: { betId: 4, position: "Takers" }) {
            bet { id }
            ok
        }
        cancelPosition(payload: { betId: 4, position: "Takers" }) {
            bet { id }
            ok
        }
    }
    """
    res = g.execute(query, context_value={"session": session, "user": stephen})
    print(jsonpickle.dumps(res, unpicklable=False, indent=4))
    assert res.errors is None

    query = """
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
        }
    }
    """
    res = g.execute(query, context_value={"session": session, "user": jacob})
    print(jsonpickle.dumps(res, unpicklable=False, indent=4))
    assert res.errors is None

    query = """
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
    }
    """
    res = g.execute(query, context_value={"session": session, "user": jacob})
    print(jsonpickle.dumps(res, unpicklable=False, indent=4))
    assert res.errors is None

    query = """
    mutation {
        sayBetChat(payload: { betId: 4, message: "Hey" }) {
            message { id }
            ok
        }
        sayGroupChat(payload: { groupId: 2, message: "Takers" }) {
            message { id }
            ok
        }
        cancelBet(payload: { betId: 4 }) {
            ok
        }
        invite(payload: { groupId: 2, email: "stephen@example.com" }) {
            ok
        }
        remove(payload: { groupId: 2, userId: 2 }) {
            ok
        }
    }
    """
    res = g.execute(query, context_value={"session": session, "user": jacob})
    print(jsonpickle.dumps(res, unpicklable=False, indent=4))
    assert res.errors is None


if __name__ == "__main__":
    main()
