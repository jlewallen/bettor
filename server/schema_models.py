from typing import Union

import graphene
import graphene_sqlalchemy


import models


class ActiveSQLAlchemyObjectType(graphene_sqlalchemy.SQLAlchemyObjectType):
    class Meta:
        abstract = True


class User(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.User

    friends = graphene.List(graphene.NonNull(lambda: User))


class Group(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Group

    members = graphene.List(graphene.NonNull(lambda: User))
    all_bets = graphene.List(graphene.NonNull(lambda: Bet))
    messages = graphene.List(graphene.NonNull(lambda: GroupChat))


class Bet(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Bet

    positions = graphene.List(graphene.NonNull(lambda: Position))
    messages = graphene.List(graphene.NonNull(lambda: BetChat))
    watchers = graphene.List(graphene.NonNull(lambda: User))
    expired = graphene.NonNull(graphene.Boolean)
    involved = graphene.NonNull(graphene.Boolean)
    cancelled = graphene.NonNull(graphene.Boolean)
    suggested = graphene.String()
    modifier = graphene.NonNull(User)
    can_take = graphene.NonNull(graphene.Boolean)
    can_cancel = graphene.NonNull(graphene.Boolean)
    can_dispute = graphene.NonNull(graphene.Boolean)
    can_pay = graphene.NonNull(graphene.Boolean)
    action = graphene.NonNull(lambda: Action)

    def resolve_expired(self, info):
        return self.is_expired()

    def resolve_involved(self, info):
        return self.is_involved(info.context["user"])

    def resolve_cancelled(self, info):
        return self.is_cancelled()

    def resolve_suggested(self, info):
        return self.suggested(info.context["user"])

    def resolve_modifier(self, info):
        return self.modifier()

    def resolve_can_take(self, info):
        return self.can_take(info.context["user"])

    def resolve_can_cancel(self, info):
        return self.can_cancel(info.context["user"])

    def resolve_can_pay(self, info):
        return self.can_pay(info.context["user"])

    def resolve_can_dispute(self, info):
        return self.can_dispute(info.context["user"])


class Position(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Position

    user_positions = graphene.List(graphene.NonNull(lambda: UserPosition))
    can_take = graphene.NonNull(graphene.Boolean)
    can_cancel = graphene.NonNull(graphene.Boolean)
    can_pay = graphene.NonNull(graphene.Boolean)
    can_dispute = graphene.NonNull(graphene.Boolean)

    def resolve_can_take(self, info):
        return self.can_take(info.context["user"])

    def resolve_can_cancel(self, info):
        return self.can_cancel(info.context["user"])

    def resolve_can_pay(self, info):
        return self.can_pay(info.context["user"])

    def resolve_can_dispute(self, info):
        return self.can_dispute(info.context["user"])


class UserPosition(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.UserPosition


class GroupChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.GroupChat


class BetChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.BetChat


class Action(graphene.ObjectType):
    name = graphene.String()


class Query(graphene.ObjectType):
    myself = graphene.Field(User)
    groups = graphene.List(
        graphene.NonNull(Group),
        group_id=graphene.Argument(type=graphene.ID, required=False),
    )
    bets = graphene.List(
        graphene.NonNull(Bet),
        bet_id=graphene.Argument(type=graphene.ID, required=False),
    )
    group_chat = graphene.List(
        graphene.NonNull(GroupChat),
        group_id=graphene.Argument(type=graphene.ID, required=True),
        page=graphene.Argument(type=graphene.Int, required=True),
    )
    bet_chat = graphene.List(
        graphene.NonNull(BetChat),
        bet_id=graphene.Argument(type=graphene.ID, required=True),
        page=graphene.Argument(type=graphene.Int, required=True),
    )

    def resolve_myself(self, info):
        return info.context["user"]

    def resolve_groups(self, info, group_id: Union[str, None] = None):
        user = info.context["user"]
        query = Group.get_query(info)  # SQLAlchemy query
        if group_id:
            return query.filter(models.Group.id == group_id).all()
        return query.filter(
            models.Group.members.any(models.User.id.in_([user.id])),
            models.Group.deleted_at == None,
        ).all()

    def resolve_bets(self, info, bet_id: Union[str, None] = None):
        user = info.context["user"]
        query = Bet.get_query(info)  # SQLAlchemy query
        if bet_id:
            return query.filter(models.Bet.id == bet_id).all()
        return query.filter(
            models.Bet.watchers.any(models.User.id.in_([user.id])),
            models.Bet.deleted_at == None,
        ).all()

    def resolve_group_chat(self, info, group_id: str, page: int):
        user = info.context["user"]
        query = GroupChat.get_query(info)  # SQLAlchemy query
        return (
            query.filter(models.GroupChat.group_id == group_id)
            .limit(20)
            .offset(page * 20)
            .all()
        )

    def resolve_bet_chat(self, info, bet_id: str, page: int):
        user = info.context["user"]
        query = BetChat.get_query(info)  # SQLAlchemy query
        return (
            query.filter(
                models.BetChat.bet_id == bet_id,
            )
            .limit(20)
            .offset(page * 20)
            .all()
        )
