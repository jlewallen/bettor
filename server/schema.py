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


class Position(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.Position


class UserPosition(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.UserPosition


class BetChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.BetChat


class GroupChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.GroupChat


class Query(graphene.ObjectType):
    myself = graphene.Field(User)
    groups = graphene.List(Group)
    bets = graphene.List(Bet)

    def resolve_myself(self, info):
        return info.context["user"]

    def resolve_groups(self, info):
        query = Group.get_query(info)  # SQLAlchemy query
        return query.all()

    def resolve_bets(self, info):
        query = Bet.get_query(info)  # SQLAlchemy query
        return query.all()
