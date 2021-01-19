import graphene
import datetime

import utils

import models
import schema
import storage

session = storage.create()


class GroupAttribute:
    name = graphene.String(required=True)


class CreateGroupPayload(graphene.InputObjectType, GroupAttribute):
    pass


class CreateGroup(graphene.Mutation):
    group = graphene.Field(schema.Group)
    ok = graphene.Boolean()

    class Arguments:
        payload = CreateGroupPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        user = info.context["user"]
        data = utils.input_to_dictionary(payload)
        group = models.Group(owner=user, members=[user], **data)
        session.commit()
        return CreateGroup(group=group, ok=True)


class BetAttribute:
    title = graphene.String(required=True)
    details = graphene.String(required=True)
    expires_in = graphene.Int(required=True)
    group_id = graphene.Int(required=True)
    arbitrary = graphene.Boolean()


class CreateBetPayload(graphene.InputObjectType, BetAttribute):
    pass


class CreateBet(graphene.Mutation):
    bet = graphene.Field(schema.Bet)
    ok = graphene.Boolean()

    class Arguments:
        payload = CreateBetPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        user = info.context["user"]
        expires_in = datetime.timedelta(minutes=payload.expires_in)
        bet = models.Bet.arbitrary(
            author=user,
            title=payload.title,
            group_id=payload.group_id,
            expires_at=datetime.datetime.utcnow() + expires_in,
        )
        session.commit()
        return CreateBet(bet=bet, ok=False)


class Mutation(graphene.ObjectType):
    createGroup = CreateGroup.Field()
    createBet = CreateBet.Field()
