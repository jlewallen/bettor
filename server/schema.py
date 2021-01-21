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


class Group(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Group


class Bet(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Bet

    expired = graphene.NonNull(graphene.Boolean)
    can_take = graphene.NonNull(graphene.Boolean)
    can_cancel = graphene.NonNull(graphene.Boolean)

    def resolve_expired(self, info):
        return self.is_expired()

    def resolve_can_take(self, info):
        return self.can_take(info.context["user"])

    def resolve_can_cancel(self, info):
        return self.can_cancel(info.context["user"])


class Position(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Position


class UserPosition(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.UserPosition


class GroupChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.GroupChat


class BetChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.BetChat


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
