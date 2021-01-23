import graphene.test
import lorem
import faker

import models
import schema as schema_factory
import db


class TestEnv:
    def __init__(self):
        self.faker = faker.Faker()
        self.faker.seed_instance(823124)
        self.schema = schema_factory.create()
        self.session = db.create()
        self.user = models.User(
            sub="user-main", name=self.faker.name(), email=self.faker.email()
        )
        self.users = [
            models.User(
                sub="user-%d" % i, name=self.faker.name(), email=self.faker.email()
            )
            for i in range(0, 10)
        ]
        self.group = models.Group(
            name="Group",
            owner=self.user,
            members=[
                self.user,
                self.users[0],
                self.users[1],
                self.users[2],
                self.users[3],
                self.users[4],
            ],
        )
        for user in self.users:
            self.session.add(user)
        self.session.add(self.user)
        self.session.commit()
        self.cl = graphene.test.Client(self.schema)
        self.context = {"session": self.session, "user": self.user}

    async def execute(self, query, **kwargs):
        return self.cl.execute(query, context_value=self.context)
