import graphene.test
import lorem
import faker

import models
import storage
import gql


class TestEnv:
    def __init__(self):
        self.faker = faker.Faker()
        self.faker.seed_instance(823124)
        self.schema = gql.create()
        self.session = storage.create()
        self.user = models.User(
            sub="user-main", name=self.faker.name(), email=self.faker.email()
        )
        self.users = [
            models.User(
                sub="user-%d" % i, name=self.faker.name(), email=self.faker.email()
            )
            for i in range(0, 10)
        ]
        for user in self.users:
            self.session.add(user)
        self.session.add(self.user)
        self.session.commit()
        self.cl = graphene.test.Client(self.schema)
        self.context = {"session": self.session, "user": self.user}

    async def execute(self, query, **kwargs):
        return self.cl.execute(query, context_value=self.context)
