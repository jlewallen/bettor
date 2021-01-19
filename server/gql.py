import graphene

import schema
import mutation


def create():
    return graphene.Schema(
        query=schema.Query,
        mutation=mutation.Mutation,
        types=[
            schema.User,
            schema.Group,
            schema.Bet,
            schema.Position,
            schema.UserPosition,
            schema.BetChat,
            schema.GroupChat,
        ],
    )
