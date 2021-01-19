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
        author=jacob, expires_at=datetime.datetime.utcnow() + standard_expiration
    )
    simple.take(jacob, position="heads")
    simple.take(stephen, position="tails")

    jimmy_example = models.Bet.arbitrary(
        title="Derrick Henry over 35 receptions",
        author=stephen,
        expires_at=datetime.datetime.utcnow() + standard_expiration,
    )
    jimmy_example.take(jimmy)

    multiple_takers = models.Bet.arbitrary(
        title="Daniel Jones has more fantasy points than Tom Brady at season end.",
        author=stephen,
        expires_at=datetime.datetime.utcnow() + standard_expiration,
    )
    multiple_takers.take(derek)
    multiple_takers.take(scott)

    group.all_bets = [simple, jimmy_example, multiple_takers]

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


if __name__ == "__main__":
    main()
