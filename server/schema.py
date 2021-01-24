import graphene

import schema_models as schema
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
            schema.GroupChat,
            schema.BetChat,
            schema.Action,
        ],
    )
