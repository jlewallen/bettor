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
    session.add(models.create_examples())
    session.commit()

    jacob = session.query(models.User).get(1)
    stephen = session.query(models.User).get(2)

    g = gql.create()

    query = """
    mutation {
        createGroup(payload: { name: "Hello, world" }) {
            group { id }
            ok
        }
    }
    """

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
