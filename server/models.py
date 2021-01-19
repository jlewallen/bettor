from typing import List, Any
from sqlalchemy import Column, Integer, String, Table, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

import datetime
import enum

from storage import Base

group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("joined", DateTime, nullable=False, default=datetime.datetime.utcnow),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    sub = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    picture = Column(String)

    created_groups = relationship("Group", back_populates="owner")
    groups = relationship("Group", secondary=group_members, back_populates="members")
    authored_bets = relationship("Bet", back_populates="author")

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    picture = Column(String)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="created_groups")
    members = relationship("User", secondary=group_members, back_populates="groups")
    all_bets = relationship("Bet", back_populates="group")
    messages = relationship("GroupChat", back_populates="group")

    def __repr__(self):
        return "<Group(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )


class BetState(enum.Enum):
    OPEN = "OPEN"
    EXPIRED = "EXPIRED"
    CLAIMED = "CLAIMED"
    DISPUTED = "DISPUTED"
    PAID = "PAID"


class GroupChat(Base):
    __tablename__ = "group_chat"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", back_populates="messages")


class BetChat(Base):
    __tablename__ = "bet_chat"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    bet_id = Column(Integer, ForeignKey("bets.id"), nullable=False)
    bet = relationship("Bet", back_populates="messages")


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    title = Column(String, nullable=False)
    details = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    state = Column(Enum(BetState), nullable=False, default=BetState.OPEN)

    author = relationship("User", back_populates="authored_bets")
    group = relationship("Group", back_populates="all_bets")
    positions = relationship("Position", back_populates="bet")
    messages = relationship("BetChat", back_populates="bet")

    @classmethod
    def arbitrary(
        cls,
        title: str = None,
        details: str = None,
        author: User = None,
        minimum: int = 1,
        maximum: int = 10,
        **kwargs
    ) -> "Bet":
        assert title
        assert author
        details = details if details else title
        myself = Position(title="Myself", minimum=1, maximum=1)
        takers = Position(title="Takers", minimum=minimum, maximum=maximum)
        myself.take(author)
        return Bet(
            title=title,
            details=details,
            positions=[myself, takers],
            state=BetState.OPEN,
            author=author,
            **kwargs
        )

    @classmethod
    def coin_toss(cls, **kwargs) -> "Bet":
        heads = Position(title="Heads", minimum=1, maximum=10)
        tails = Position(title="Tails", minimum=1, maximum=10)
        return Bet(
            title="Coin toss!",
            details="Coin toss!",
            positions=[heads, tails],
            state=BetState.OPEN,
            **kwargs
        )

    def take(self, user: User, position: str = None):
        if user in self.users_with_positions():
            raise Exception("already taken")
        for p in self.positions:
            if position:
                if p.title.lower() == position.lower():
                    if p.take(user):
                        pass
            else:
                if p.is_open():
                    if p.take(user):
                        pass

    def users_with_positions(self) -> List[User]:
        return flatten([p.valid_users() for p in self.positions])

    def __repr__(self):
        return "<Bet(id='%s', state='%s', title='%s')>" % (
            self.id,
            self.state,
            self.title,
        )


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    bet_id = Column(Integer, ForeignKey("bets.id"), nullable=False)
    title = Column(String, nullable=False)
    minimum = Column(Integer, nullable=False)
    maximum = Column(Integer, nullable=False)

    bet = relationship("Bet", back_populates="positions")
    user_positions = relationship("UserPosition")

    def is_open(self) -> bool:
        return len(self.valid_users()) < self.maximum

    def valid_users(self) -> List[User]:
        return [up.user for up in self.user_positions if up.is_valid()]

    def take(self, user: User) -> bool:
        self.user_positions.append(UserPosition(position=self, user=user))
        return True

    def __repr__(self):
        return "<Position(id='%s', title='%s')>" % (
            self.id,
            self.title,
        )


class PositionState(enum.Enum):
    TAKEN = "TAKEN"
    CANCELLED = "CANCELLED"
    CLAIMED = "CLAIMED"


class UserPosition(Base):
    __tablename__ = "user_positions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    state = Column(Enum(PositionState), nullable=False, default=PositionState.TAKEN)

    user = relationship("User")
    position = relationship("Position", back_populates="user_positions")

    def is_valid(self) -> bool:
        return self.state != PositionState.CANCELLED

    def __repr__(self):
        return "<UserPosition(id='%s', title='%s')>" % (
            self.id,
            self.title,
        )


def flatten(l):
    return [item for sl in l for item in sl]
