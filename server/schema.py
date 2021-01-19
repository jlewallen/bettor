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


class GroupChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.GroupChat


class BetChat(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.BetChat


class Query(graphene.ObjectType):
    myself = graphene.Field(User)
    groups = graphene.List(Group)
    bets = graphene.List(Bet)

    def resolve_myself(self, info):
        return info.context["user"]

    def resolve_groups(self, info):
        user = info.context["user"]
        query = Group.get_query(info)  # SQLAlchemy query
        return query.filter(
            models.Group.members.any(models.User.id.in_([user.id])),
            models.Group.deleted_at == None,
        ).all()

    def resolve_bets(self, info):
        user = info.context["user"]
        query = Bet.get_query(info)  # SQLAlchemy query
        return query.filter(
            models.Bet.watchers.any(models.User.id.in_([user.id])),
            models.Bet.deleted_at == None,
        ).all()
