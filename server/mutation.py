import logging
import graphene
import datetime

import utils
import models
import schema_models as schema
import db

log = logging.getLogger("bettor")


class CreateGroupAttributes:
    name = graphene.String(required=True)
    members = graphene.List(graphene.NonNull(graphene.ID), required=True)


class CreateGroupPayload(graphene.InputObjectType, CreateGroupAttributes):
    pass


class CreateGroup(graphene.Mutation):
    group = graphene.Field(schema.Group)
    ok = graphene.Boolean()

    class Arguments:
        payload = CreateGroupPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        group = models.Group(owner=user, members=[user], name=payload.name)
        for id in payload.members:
            member = session.query(models.User).get(id)
            if member not in group.members:
                group.members.append(member)
        session.commit()
        return CreateGroup(group=group, ok=True)


class BetAttribute:
    title = graphene.String(required=True)
    details = graphene.String(required=True)
    expires_in = graphene.Int(required=True)
    group_id = graphene.ID(required=True)
    minimum_takers = graphene.Int(required=True)
    maximum_takers = graphene.Int(required=True)
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
        session = info.context["session"]
        user = info.context["user"]
        expires_in = datetime.timedelta(seconds=payload.expires_in)
        expires_at = datetime.datetime.utcnow() + expires_in
        group = session.query(models.Group).get(payload.group_id)
        bet = models.Bet.arbitrary(
            author=user,
            title=payload.title,
            group=group,
            expires_at=expires_at,
            minimum_takers=payload.minimum_takers,
            maximum_takers=payload.maximum_takers,
        )
        session.commit()
        return CreateBet(bet=bet, ok=True)


class CreateExamples(graphene.Mutation):
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info):
        session = info.context["session"]
        user = info.context["user"]
        session.add(models.create_examples())
        session.commit()
        return CreateExamples(ok=True)


class PositionAttributes:
    bet_id = graphene.ID(required=True)
    position = graphene.String()


class PositionPayload(graphene.InputObjectType, PositionAttributes):
    pass


class TakePosition(graphene.Mutation):
    bet = graphene.Field(schema.Bet)
    ok = graphene.Boolean()

    class Arguments:
        payload = PositionPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.take(user, payload.position)
        session.commit()
        return TakePosition(bet=bet, ok=True)


class CancelPosition(graphene.Mutation):
    bet = graphene.Field(schema.Bet)
    ok = graphene.Boolean()

    class Arguments:
        payload = PositionPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.cancel(user)
        session.commit()
        return CancelPosition(bet=bet, ok=True)


class GroupChatAttributes:
    group_id = graphene.ID(required=True)
    message = graphene.String()


class GroupChatPayload(graphene.InputObjectType, GroupChatAttributes):
    pass


class SayGroupChat(graphene.Mutation):
    message = graphene.Field(schema.GroupChat)
    ok = graphene.Boolean()

    class Arguments:
        payload = GroupChatPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        group = session.query(models.Group).get(payload.group_id)
        assert group
        group.touch()
        message = models.GroupChat(group=group, message=payload.message, author=user)
        session.add(message)
        session.commit()
        return SayGroupChat(message=message, ok=True)


class BetChatAttributes:
    bet_id = graphene.ID(required=True)
    message = graphene.String()


class BetChatPayload(graphene.InputObjectType, BetChatAttributes):
    pass


class SayBetChat(graphene.Mutation):
    message = graphene.Field(schema.BetChat)
    ok = graphene.Boolean()

    class Arguments:
        payload = BetChatPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.touch()
        message = models.BetChat(bet=bet, message=payload.message, author=user)
        session.add(message)
        session.commit()
        return SayBetChat(message=message, ok=True)


class RemindBetAttributes:
    bet_id = graphene.ID(required=True)


class RemindBetPayload(graphene.InputObjectType, RemindBetAttributes):
    pass


class RemindBet(graphene.Mutation):
    bet = graphene.Field(schema.Bet)
    ok = graphene.Boolean()

    class Arguments:
        payload = RemindBetPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.remind(user)
        bet.touch()
        session.commit()
        return CancelBet(bet=bet, ok=True)


class CancelBetAttributes:
    bet_id = graphene.ID(required=True)


class CancelBetPayload(graphene.InputObjectType, CancelBetAttributes):
    pass


class CancelBet(graphene.Mutation):
    bet = graphene.Field(schema.Bet)
    ok = graphene.Boolean()

    class Arguments:
        payload = CancelBetPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.cancel(user)
        bet.touch()
        session.commit()
        return CancelBet(bet=bet, ok=True)


class InviteAttributes:
    group_id = graphene.ID(required=True)
    email = graphene.String(required=True)


class InvitePayload(graphene.InputObjectType, InviteAttributes):
    pass


class Invite(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        payload = InvitePayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        inviting = (
            session.query(models.User)
            .filter(models.User.email == payload.email)
            .first()
        )
        if not inviting:
            return CancelBet(ok=False)
        group = session.query(models.Group).get(payload.group_id)
        group.invite(inviting)
        session.commit()
        return CancelBet(ok=True)


class RemoveAttributes:
    group_id = graphene.ID(required=True)
    user_id = graphene.ID(required=True)


class RemovePayload(graphene.InputObjectType, RemoveAttributes):
    pass


class Remove(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        payload = RemovePayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        session = info.context["session"]
        user = info.context["user"]
        removing = session.query(models.User).get(payload.user_id)
        group = session.query(models.Group).get(payload.group_id)
        group.remove(removing)
        session.commit()
        return CancelBet(ok=True)


class Mutation(graphene.ObjectType):
    createGroup = CreateGroup.Field()
    createBet = CreateBet.Field()
    createExamples = CreateExamples.Field()
    takePosition = TakePosition.Field()
    cancelPosition = CancelPosition.Field()
    sayGroupChat = SayGroupChat.Field()
    sayBetChat = SayBetChat.Field()
    cancelBet = CancelBet.Field()
    remindBet = RemindBet.Field()
    invite = Invite.Field()
    remove = Remove.Field()
