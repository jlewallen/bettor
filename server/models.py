from typing import List, Any, Union, Optional

from sqlalchemy import Column, Integer, String, Table, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

import datetime
import enum
import lorem
import random

from storage import Base

group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("joined", DateTime, nullable=False, default=datetime.datetime.utcnow),
)


bet_watchers = Table(
    "bet_watchers",
    Base.metadata,
    Column("bet_id", ForeignKey("bets.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("watched", DateTime, nullable=False, default=datetime.datetime.utcnow),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    sub = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    picture = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    activity_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    created_groups = relationship("Group", back_populates="owner")
    groups = relationship("Group", secondary=group_members, back_populates="members")
    authored_bets = relationship("Bet", back_populates="author")

    watched_bets = relationship(
        "Bet", secondary=bet_watchers, back_populates="watchers"
    )

    __mapper_args__ = {"order_by": activity_at.desc()}

    def touch(self):
        self.activity_at = datetime.datetime.utcnow()

    def __repr__(self) -> str:
        return "<User(id='%s', name='%s', picture='%s')>" % (
            self.id,
            self.name,
            self.picture,
        )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    picture = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    activity_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="created_groups")
    members = relationship("User", secondary=group_members, back_populates="groups")
    all_bets = relationship("Bet", back_populates="group")
    messages = relationship("GroupChat", back_populates="group")

    __mapper_args__ = {"order_by": activity_at.desc()}

    def touch(self):
        self.activity_at = datetime.datetime.utcnow()

    def invite(self, user: User) -> Union[User, None]:
        if user in self.members:
            return None
        self.members.append(user)
        return user

    def remove(self, user: User) -> Optional[User]:
        if user in self.members:
            self.members.remove(user)
        return user

    def __repr__(self):
        return "<Group(id='%s', name='%s', picture='%s')>" % (
            self.id,
            self.name,
            self.picture,
        )


class BetState(enum.Enum):
    OPEN = "OPEN"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    CLAIMED = "CLAIMED"
    DISPUTED = "DISPUTED"
    PAID = "PAID"


class GroupChat(Base):
    __tablename__ = "group_chat"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    message = Column(String, nullable=False)

    group = relationship("Group", back_populates="messages")
    author = relationship("User")

    __mapper_args__ = {"order_by": created_at.desc()}


class BetChat(Base):
    __tablename__ = "bet_chat"

    id = Column(Integer, primary_key=True)
    bet_id = Column(Integer, ForeignKey("bets.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    message = Column(String, nullable=False)

    bet = relationship("Bet", back_populates="messages")
    author = relationship("User")

    __mapper_args__ = {"order_by": created_at.desc()}


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    title = Column(String, nullable=False)
    details = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    activity_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    state = Column(Enum(BetState), nullable=False, default=BetState.OPEN)

    author = relationship("User", back_populates="authored_bets")
    group = relationship("Group", back_populates="all_bets")
    positions = relationship("Position", back_populates="bet")
    messages = relationship("BetChat", back_populates="bet")
    watchers = relationship(
        "User", secondary=bet_watchers, back_populates="watched_bets"
    )

    def touch(self):
        self.activity_at = datetime.datetime.utcnow()
        assert self.group
        if self.group:
            self.group.touch()

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
        myself = Position(title="Bettor", minimum=1, maximum=1)
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

    def is_expired(self) -> bool:
        return datetime.datetime.utcnow() > self.expires_at

    def can_take(self, user: User) -> bool:
        if self.state == BetState.CANCELLED:
            return False
        if self.has_position(user):
            return False
        return len(self.open_positions()) > 0

    def can_cancel(self, user: User) -> bool:
        if self.author.id == user.id:
            return self.state != BetState.CANCELLED
        return self.has_position(user)

    def open_positions(self) -> List["Position"]:
        return [p for p in self.positions if p.is_open()]

    def suggested(self, user: User) -> Optional[str]:
        op = self.open_positions()
        if len(op):
            return op[0].title
        return None

    def take(self, user: User, position: str = None):
        if self.state == BetState.CANCELLED:
            raise Exception("cancelled")
        if user in self.users_with_positions():
            raise Exception("already taken")
        for p in self.positions:
            if position:
                if p.title.lower() == position.lower():
                    if p.take(user):
                        self.touch()
                        self.watchers.append(user)
            else:
                if p.is_open():
                    if p.take(user):
                        self.touch()
                        self.watchers.append(user)

    def cancel(self, user: User):
        if self.state == BetState.CANCELLED:
            raise Exception("cancelled")
        self.position_by_user(user).cancel(user)
        if self.author == user:
            self.state = BetState.CANCELLED
        self.touch()

    def position_by_user(self, user: User) -> "UserPosition":
        found = [up for up in self.positions if up.has_user(user)]
        if len(found):
            return found[0]
        raise Exception("no position for user")

    def users_with_positions(self) -> List[User]:
        return flatten([p.valid_users() for p in self.positions])

    def all_users_with_positions(self) -> List[User]:
        return flatten([p.valid_users() for p in self.positions])

    def has_position(self, user: User) -> bool:
        return user in self.all_users_with_positions()

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

    def can_take(self, user: User) -> bool:
        return user not in self.valid_users()

    def can_cancel(self, user: User) -> bool:
        return user in self.valid_users()

    def is_open(self) -> bool:
        return len(self.valid_users()) < self.maximum

    def all_users(self) -> List[User]:
        return [up.user for up in self.user_positions]

    def valid_users(self) -> List[User]:
        return [up.user for up in self.user_positions if up.is_valid()]

    def has_user(self, user: User) -> bool:
        return user in self.valid_users()

    def take(self, user: User) -> bool:
        self.user_positions.append(UserPosition(position=self, user=user))
        return True

    def get_user_position(self, user: User) -> "UserPosition":
        return [up for up in self.user_positions if up.user_id == user.id][0]

    def cancel(self, user: User) -> bool:
        user_position = self.get_user_position(user)
        user_position.cancel()
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
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    state = Column(Enum(PositionState), nullable=False, default=PositionState.TAKEN)

    user = relationship("User")
    position = relationship("Position", back_populates="user_positions")

    def is_valid(self) -> bool:
        return self.state != PositionState.CANCELLED

    def cancel(self):
        assert self.state == PositionState.TAKEN
        self.state = PositionState.CANCELLED

    def __repr__(self):
        return "<UserPosition(id='%s', title='%s')>" % (
            self.id,
            self.title,
        )


def flatten(l):
    return [item for sl in l for item in sl]


def create_examples():
    jacob = User(
        sub="",
        name="Jacob",
        email="jlewalle@gmail.com",
        picture="https://lh3.googleusercontent.com/a-/AOh14Gjl9_87qIin3U2czS8qz9frvvSLvEkKoBwQfcvRcg=s96-c",
    )
    stephen = User(sub="", name="Stephen", email="stephen@example.com")
    jimmy = User(sub="", name="Jimmy", email="jimmy@example.com")
    derek = User(sub="", name="Derek", email="derek@example.com")
    zack = User(sub="", name="Zack", email="zack@example.com")
    scott = User(sub="", name="Scott", email="scott@example.com")

    standard_expiration = datetime.timedelta(minutes=60)
    group_epoch = datetime.datetime.utcnow()
    bet_time = group_epoch

    group = Group(
        name="Small Group",
        owner=jacob,
        members=[jacob, stephen, jimmy, derek, zack, scott],
    )

    bet_time += datetime.timedelta(seconds=random.randrange(30, 60))

    simple = Bet.coin_toss(
        created_at=bet_time,
        group=group,
        author=jacob,
        expires_at=bet_time + standard_expiration,
    )
    simple.take(jacob, position="heads")
    simple.take(stephen, position="tails")

    bet_time += datetime.timedelta(seconds=random.randrange(30, 60))

    jimmy_example = Bet.arbitrary(
        created_at=bet_time,
        title="Derrick Henry over 35 receptions",
        group=group,
        author=stephen,
        expires_at=group_epoch + standard_expiration,
    )
    jimmy_example.take(jimmy)

    bet_time += datetime.timedelta(seconds=random.randrange(30, 60))

    multiple_takers = Bet.arbitrary(
        created_at=bet_time,
        group=group,
        title="Daniel Jones has more fantasy points than Tom Brady at season end.",
        author=stephen,
        expires_at=group_epoch + standard_expiration,
    )
    multiple_takers.take(derek)
    multiple_takers.take(scott)

    chat_time = group_epoch - datetime.timedelta(seconds=200)
    for i in range(0, 10):
        for j in range(0, 2):
            user = random.choice(group.members)
            message = GroupChat(
                group=group, message=lorem.sentence(), author=user, created_at=chat_time
            )
            group.messages.append(message)
            chat_time += datetime.timedelta(seconds=random.randrange(30, 60))

    return group
