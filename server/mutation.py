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
        return CreateBet(bet=bet, ok=True)


class CreateExamples(graphene.Mutation):
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info):
        user = info.context["user"]
        session.add(models.create_examples())
        session.commit()
        return CreateExamples(ok=True)


class PositionAttributes:
    bet_id = graphene.Int(required=True)
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
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.cancel(user)
        session.commit()
        return CancelPosition(bet=bet, ok=True)


class GroupChatAttributes:
    group_id = graphene.Int(required=True)
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
        user = info.context["user"]
        group = session.query(models.Group).get(payload.group_id)
        group.touch()
        message = models.GroupChat(group=group, message=payload.message, author=user)
        session.add(message)
        session.commit()
        return SayGroupChat(message=message, ok=True)


class BetChatAttributes:
    bet_id = graphene.Int(required=True)
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
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.touch()
        message = models.BetChat(bet=bet, message=payload.message, author=user)
        session.add(message)
        session.commit()
        return SayBetChat(message=message, ok=True)


class CancelBetAttributes:
    bet_id = graphene.Int(required=True)


class CancelBetPayload(graphene.InputObjectType, CancelBetAttributes):
    pass


class CancelBet(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        payload = CancelBetPayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        user = info.context["user"]
        bet = session.query(models.Bet).get(payload.bet_id)
        bet.cancel(user)
        bet.touch()
        session.commit()
        return CancelBet(ok=True)


class InviteAttributes:
    group_id = graphene.Int(required=True)
    email = graphene.String(required=True)


class InvitePayload(graphene.InputObjectType, InviteAttributes):
    pass


class Invite(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        payload = InvitePayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
        user = info.context["user"]
        inviting = (
            session.query(models.User)
            .filter(models.User.email == payload.email)
            .first()
        )
        group = session.query(models.Group).get(payload.group_id)
        group.invite(inviting)
        session.commit()
        return CancelBet(ok=True)


class RemoveAttributes:
    group_id = graphene.Int(required=True)
    user_id = graphene.Int(required=True)


class RemovePayload(graphene.InputObjectType, RemoveAttributes):
    pass


class Remove(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        payload = RemovePayload(required=True)

    @staticmethod
    def mutate(self, info, payload):
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
    invite = Invite.Field()
    remove = Remove.Field()
