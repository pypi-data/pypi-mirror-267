class TestEagerLoadingOnPG:
    def test_find_by_pk(self):
        from dataloom import (
            Loom,
            Model,
            Column,
            PrimaryKeyColumn,
            CreatedAtColumn,
            TableColumn,
            ForeignKeyColumn,
            ColumnValue,
            Include,
            Order,
        )
        from dataloom.keys import PgConfig

        pg_loom = Loom(
            dialect="postgres",
            database=PgConfig.database,
            password=PgConfig.password,
            user=PgConfig.user,
        )

        class User(Model):
            __tablename__: TableColumn = TableColumn(name="users")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")
            username = Column(type="varchar", unique=True, length=255)
            tokenVersion = Column(type="int", default=0)

        class Profile(Model):
            __tablename__: TableColumn = TableColumn(name="profiles")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            avatar = Column(type="text", nullable=False)
            userId = ForeignKeyColumn(
                User,
                maps_to="1-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Post(Model):
            __tablename__: TableColumn = TableColumn(name="posts")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            completed = Column(type="boolean", default=False)
            title = Column(type="varchar", length=255, nullable=False)
            # timestamps
            createdAt = CreatedAtColumn()
            # relations
            userId = ForeignKeyColumn(
                User,
                maps_to="1-N",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Category(Model):
            __tablename__: TableColumn = TableColumn(name="categories")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            type = Column(type="varchar", length=255, nullable=False)

            postId = ForeignKeyColumn(
                Post,
                maps_to="N-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        conn, tables = pg_loom.connect_and_sync(
            [User, Profile, Post, Category], drop=True, force=True
        )

        userId = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="@miller"),
        )

        userId2 = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="bob"),
        )

        profileId = pg_loom.insert_one(
            instance=Profile,
            values=[
                ColumnValue(name="userId", value=userId),
                ColumnValue(name="avatar", value="hello.jpg"),
            ],
        )
        for title in ["Hey", "Hello", "What are you doing", "Coding"]:
            pg_loom.insert_one(
                instance=Post,
                values=[
                    ColumnValue(name="userId", value=userId),
                    ColumnValue(name="title", value=title),
                ],
            )

        for cat in ["general", "education", "tech", "sport"]:
            pg_loom.insert_one(
                instance=Category,
                values=[
                    ColumnValue(name="postId", value=1),
                    ColumnValue(name="type", value=cat),
                ],
            )

        profile = pg_loom.find_by_pk(
            instance=Profile,
            pk=profileId,
            include=[
                Include(
                    model=User, select=["id", "username", "tokenVersion"], has="one"
                )
            ],
        )
        assert profile == {
            "avatar": "hello.jpg",
            "id": 1,
            "userId": 1,
            "user": {"id": 1, "username": "@miller", "tokenVersion": 0},
        }

        user = pg_loom.find_by_pk(
            instance=User,
            pk=userId,
            include=[Include(model=Profile, select=["id", "avatar"], has="one")],
        )
        assert user == {
            "id": 1,
            "name": "Bob",
            "tokenVersion": 0,
            "username": "@miller",
            "profile": {"id": 1, "avatar": "hello.jpg"},
        }

        user = pg_loom.find_by_pk(
            instance=User,
            pk=userId,
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    offset=0,
                    limit=2,
                    order=[
                        Order(column="createdAt", order="DESC"),
                        Order(column="id", order="DESC"),
                    ],
                ),
                Include(model=Profile, select=["id", "avatar"], has="one"),
            ],
        )
        assert user == {
            "id": 1,
            "name": "Bob",
            "tokenVersion": 0,
            "username": "@miller",
            "posts": [
                {"id": 4, "title": "Coding"},
                {"id": 3, "title": "What are you doing"},
            ],
            "profile": {"id": 1, "avatar": "hello.jpg"},
        }

        post = pg_loom.find_by_pk(
            instance=Post,
            pk=1,
            select=["title", "id"],
            include=[
                Include(
                    model=User,
                    select=["id", "username"],
                    has="one",
                    include=[
                        Include(model=Profile, select=["avatar", "id"], has="one")
                    ],
                ),
                Include(
                    model=Category,
                    select=["id", "type"],
                    has="many",
                    order=[Order(column="id", order="DESC")],
                ),
            ],
        )

        assert post == {
            "title": "Hey",
            "id": 1,
            "user": {
                "id": 1,
                "username": "@miller",
                "profile": {"avatar": "hello.jpg", "id": 1},
            },
            "categories": [
                {"id": 4, "type": "sport"},
                {"id": 3, "type": "tech"},
                {"id": 2, "type": "education"},
                {"id": 1, "type": "general"},
            ],
        }

        user = pg_loom.find_by_pk(
            instance=User,
            pk=userId2,
            select=["username", "id"],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    include=[
                        Include(
                            model=Category,
                            select=["type", "id"],
                            has="many",
                            order=[Order(column="id", order="DESC")],
                            limit=2,
                            offset=0,
                        )
                    ],
                ),
            ],
        )
        assert user == {"username": "bob", "id": 2, "posts": []}

        conn.close()

    def test_find_one(self):
        from dataloom import (
            Loom,
            Model,
            Column,
            PrimaryKeyColumn,
            CreatedAtColumn,
            TableColumn,
            ForeignKeyColumn,
            ColumnValue,
            Include,
            Order,
            Filter,
        )
        from dataloom.keys import PgConfig

        pg_loom = Loom(
            dialect="postgres",
            database=PgConfig.database,
            password=PgConfig.password,
            user=PgConfig.user,
        )

        class User(Model):
            __tablename__: TableColumn = TableColumn(name="users")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")
            username = Column(type="varchar", unique=True, length=255)
            tokenVersion = Column(type="int", default=0)

        class Profile(Model):
            __tablename__: TableColumn = TableColumn(name="profiles")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            avatar = Column(type="text", nullable=False)
            userId = ForeignKeyColumn(
                User,
                maps_to="1-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Post(Model):
            __tablename__: TableColumn = TableColumn(name="posts")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            completed = Column(type="boolean", default=False)
            title = Column(type="varchar", length=255, nullable=False)
            # timestamps
            createdAt = CreatedAtColumn()
            # relations
            userId = ForeignKeyColumn(
                User,
                maps_to="1-N",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Category(Model):
            __tablename__: TableColumn = TableColumn(name="categories")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            type = Column(type="varchar", length=255, nullable=False)

            postId = ForeignKeyColumn(
                Post,
                maps_to="N-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        conn, tables = pg_loom.connect_and_sync(
            [User, Profile, Post, Category], drop=True, force=True
        )

        userId = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="@miller"),
        )

        userId2 = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="bob"),
        )

        profileId = pg_loom.insert_one(
            instance=Profile,
            values=[
                ColumnValue(name="userId", value=userId),
                ColumnValue(name="avatar", value="hello.jpg"),
            ],
        )
        for title in ["Hey", "Hello", "What are you doing", "Coding"]:
            pg_loom.insert_one(
                instance=Post,
                values=[
                    ColumnValue(name="userId", value=userId),
                    ColumnValue(name="title", value=title),
                ],
            )

        for cat in ["general", "education", "tech", "sport"]:
            pg_loom.insert_one(
                instance=Category,
                values=[
                    ColumnValue(name="postId", value=1),
                    ColumnValue(name="type", value=cat),
                ],
            )

        profile = pg_loom.find_one(
            instance=Profile,
            filters=[Filter(column="userId", value=profileId)],
            include=[
                Include(
                    model=User, select=["id", "username", "tokenVersion"], has="one"
                )
            ],
        )
        assert profile == {
            "avatar": "hello.jpg",
            "id": 1,
            "userId": 1,
            "user": {"id": 1, "username": "@miller", "tokenVersion": 0},
        }

        user = pg_loom.find_one(
            instance=User,
            filters=[Filter(column="id", value=userId)],
            include=[Include(model=Profile, select=["id", "avatar"], has="one")],
        )
        assert user == {
            "id": 1,
            "name": "Bob",
            "tokenVersion": 0,
            "username": "@miller",
            "profile": {"id": 1, "avatar": "hello.jpg"},
        }

        user = pg_loom.find_one(
            instance=User,
            filters=[Filter(column="id", value=userId)],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    offset=0,
                    limit=2,
                    order=[
                        Order(column="createdAt", order="DESC"),
                        Order(column="id", order="DESC"),
                    ],
                ),
                Include(model=Profile, select=["id", "avatar"], has="one"),
            ],
        )
        assert user == {
            "id": 1,
            "name": "Bob",
            "tokenVersion": 0,
            "username": "@miller",
            "posts": [
                {"id": 4, "title": "Coding"},
                {"id": 3, "title": "What are you doing"},
            ],
            "profile": {"id": 1, "avatar": "hello.jpg"},
        }

        post = pg_loom.find_one(
            instance=Post,
            filters=[Filter(column="userId", value=userId)],
            select=["title", "id"],
            include=[
                Include(
                    model=User,
                    select=["id", "username"],
                    has="one",
                    include=[
                        Include(model=Profile, select=["avatar", "id"], has="one")
                    ],
                ),
                Include(
                    model=Category,
                    select=["id", "type"],
                    has="many",
                    order=[Order(column="id", order="DESC")],
                ),
            ],
        )
        assert post == {
            "title": "Hey",
            "id": 1,
            "user": {
                "id": 1,
                "username": "@miller",
                "profile": {"avatar": "hello.jpg", "id": 1},
            },
            "categories": [
                {"id": 4, "type": "sport"},
                {"id": 3, "type": "tech"},
                {"id": 2, "type": "education"},
                {"id": 1, "type": "general"},
            ],
        }
        user = pg_loom.find_one(
            instance=User,
            filters=[Filter(column="id", value=userId2)],
            select=["username", "id"],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    include=[
                        Include(
                            model=Category,
                            select=["type", "id"],
                            has="many",
                            order=[Order(column="id", order="DESC")],
                            limit=2,
                            offset=0,
                        )
                    ],
                ),
            ],
        )
        assert user == {"username": "bob", "id": 2, "posts": []}

        user = pg_loom.find_all(
            instance=User,
            select=["username", "id"],
            limit=1,
            offset=0,
            order=[Order(column="id", order="ASC")],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    limit=1,
                    offset=0,
                    order=[Order(column="id", order="ASC")],
                    include=[
                        Include(
                            model=Category,
                            select=["type", "id"],
                            has="many",
                            order=[Order(column="id", order="DESC")],
                            limit=2,
                            offset=0,
                        ),
                        Include(
                            model=User,
                            select=["username", "id"],
                            has="one",
                        ),
                    ],
                ),
            ],
        )
        assert user == [
            {
                "username": "@miller",
                "id": 1,
                "categories": [{"type": "sport", "id": 4}, {"type": "tech", "id": 3}],
                "user": {"username": "@miller", "id": 1},
                "posts": [
                    {
                        "id": 1,
                        "title": "Hey",
                        "categories": [
                            {"type": "sport", "id": 4},
                            {"type": "tech", "id": 3},
                        ],
                        "user": {"username": "@miller", "id": 1},
                    }
                ],
            }
        ]

        conn.close()

    def test_find_many(self):
        from dataloom import (
            Loom,
            Model,
            Column,
            PrimaryKeyColumn,
            CreatedAtColumn,
            TableColumn,
            ForeignKeyColumn,
            ColumnValue,
            Include,
            Order,
            Filter,
        )
        from dataloom.keys import PgConfig

        pg_loom = Loom(
            dialect="postgres",
            database=PgConfig.database,
            password=PgConfig.password,
            user=PgConfig.user,
        )

        class User(Model):
            __tablename__: TableColumn = TableColumn(name="users")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")
            username = Column(type="varchar", unique=True, length=255)
            tokenVersion = Column(type="int", default=0)

        class Profile(Model):
            __tablename__: TableColumn = TableColumn(name="profiles")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            avatar = Column(type="text", nullable=False)
            userId = ForeignKeyColumn(
                User,
                maps_to="1-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Post(Model):
            __tablename__: TableColumn = TableColumn(name="posts")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            completed = Column(type="boolean", default=False)
            title = Column(type="varchar", length=255, nullable=False)
            # timestamps
            createdAt = CreatedAtColumn()
            # relations
            userId = ForeignKeyColumn(
                User,
                maps_to="1-N",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Category(Model):
            __tablename__: TableColumn = TableColumn(name="categories")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            type = Column(type="varchar", length=255, nullable=False)

            postId = ForeignKeyColumn(
                Post,
                maps_to="N-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        conn, tables = pg_loom.connect_and_sync(
            [User, Profile, Post, Category], drop=True, force=True
        )

        userId = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="@miller"),
        )

        userId2 = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="bob"),
        )

        profileId = pg_loom.insert_one(
            instance=Profile,
            values=[
                ColumnValue(name="userId", value=userId),
                ColumnValue(name="avatar", value="hello.jpg"),
            ],
        )
        for title in ["Hey", "Hello", "What are you doing", "Coding"]:
            pg_loom.insert_one(
                instance=Post,
                values=[
                    ColumnValue(name="userId", value=userId),
                    ColumnValue(name="title", value=title),
                ],
            )

        for cat in ["general", "education", "tech", "sport"]:
            pg_loom.insert_one(
                instance=Category,
                values=[
                    ColumnValue(name="postId", value=profileId),
                    ColumnValue(name="type", value=cat),
                ],
            )

        profile = pg_loom.find_many(
            instance=Profile,
            filters=[Filter(column="userId", value=1)],
            include=[
                Include(
                    model=User, select=["id", "username", "tokenVersion"], has="one"
                )
            ],
        )

        assert profile == [
            {
                "avatar": "hello.jpg",
                "id": 1,
                "userId": 1,
                "user": {"id": 1, "username": "@miller", "tokenVersion": 0},
            }
        ]

        user = pg_loom.find_many(
            instance=User,
            filters=[Filter(column="id", value=userId)],
            include=[Include(model=Profile, select=["id", "avatar"], has="one")],
        )
        assert user == [
            {
                "id": 1,
                "name": "Bob",
                "tokenVersion": 0,
                "username": "@miller",
                "profile": {"id": 1, "avatar": "hello.jpg"},
            }
        ]

        user = pg_loom.find_many(
            instance=User,
            filters=[Filter(column="id", value=userId)],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    offset=0,
                    limit=2,
                    order=[
                        Order(column="createdAt", order="DESC"),
                        Order(column="id", order="DESC"),
                    ],
                ),
                Include(model=Profile, select=["id", "avatar"], has="one"),
            ],
        )
        assert user == [
            {
                "id": 1,
                "name": "Bob",
                "tokenVersion": 0,
                "username": "@miller",
                "posts": [
                    {"id": 4, "title": "Coding"},
                    {"id": 3, "title": "What are you doing"},
                ],
                "profile": {"id": 1, "avatar": "hello.jpg"},
            }
        ]
        post = pg_loom.find_many(
            instance=Post,
            filters=[Filter(column="userId", value=userId)],
            select=["title", "id"],
            limit=1,
            offset=0,
            order=[Order(column="id", order="DESC")],
            include=[
                Include(
                    model=User,
                    select=["id", "username"],
                    has="one",
                    include=[
                        Include(model=Profile, select=["avatar", "id"], has="one")
                    ],
                ),
                Include(
                    model=Category,
                    select=["id", "type"],
                    has="many",
                    order=[Order(column="id", order="DESC")],
                    limit=2,
                ),
            ],
        )

        assert post == [
            {
                "title": "Coding",
                "id": 4,
                "user": {
                    "id": 1,
                    "username": "@miller",
                    "profile": {"avatar": "hello.jpg", "id": 1},
                },
                "categories": [],
            }
        ]

        user = pg_loom.find_many(
            instance=User,
            filters=[Filter(column="id", value=userId2)],
            select=["username", "id"],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    include=[
                        Include(
                            model=Category,
                            select=["type", "id"],
                            has="many",
                            order=[Order(column="id", order="DESC")],
                            limit=2,
                            offset=0,
                        )
                    ],
                ),
            ],
        )

        assert user == [{"username": "bob", "id": 2, "posts": []}]

        posts = pg_loom.find_many(Post, select=["id", "completed"])
        assert posts == [
            {"id": 1, "completed": 0},
            {"id": 2, "completed": 0},
            {"id": 3, "completed": 0},
            {"id": 4, "completed": 0},
        ]

        user = pg_loom.find_all(
            instance=User,
            select=["username", "id"],
            limit=1,
            offset=0,
            order=[Order(column="id", order="ASC")],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    limit=1,
                    offset=0,
                    order=[Order(column="id", order="ASC")],
                    include=[
                        Include(
                            model=Category,
                            select=["type", "id"],
                            has="many",
                            order=[Order(column="id", order="DESC")],
                            limit=2,
                            offset=0,
                        ),
                        Include(
                            model=User,
                            select=["username", "id"],
                            has="one",
                        ),
                    ],
                ),
            ],
        )
        assert user == [
            {
                "username": "@miller",
                "id": 1,
                "categories": [{"type": "sport", "id": 4}, {"type": "tech", "id": 3}],
                "user": {"username": "@miller", "id": 1},
                "posts": [
                    {
                        "id": 1,
                        "title": "Hey",
                        "categories": [
                            {"type": "sport", "id": 4},
                            {"type": "tech", "id": 3},
                        ],
                        "user": {"username": "@miller", "id": 1},
                    }
                ],
            }
        ]
        user = pg_loom.find_many(
            instance=User,
            filters=[Filter(column="id", value=1)],
            select=["username", "id"],
            limit=1,
            offset=0,
            order=[Order(column="id", order="ASC")],
            include=[
                Include(
                    model=Post,
                    select=["id", "title"],
                    has="many",
                    limit=1,
                    offset=0,
                    order=[Order(column="id", order="ASC")],
                    include=[
                        Include(
                            model=Category,
                            select=["type", "id"],
                            has="many",
                            order=[Order(column="id", order="DESC")],
                            limit=2,
                            offset=0,
                        ),
                        Include(
                            model=User,
                            select=["username", "id"],
                            has="one",
                        ),
                    ],
                ),
            ],
        )
        assert user == [
            {
                "username": "@miller",
                "id": 1,
                "posts": [
                    {
                        "id": 1,
                        "title": "Hey",
                        "categories": [
                            {"type": "sport", "id": 4},
                            {"type": "tech", "id": 3},
                        ],
                        "user": {"username": "@miller", "id": 1},
                    }
                ],
            }
        ]

    def test_unknown_relations(self):
        from dataloom import (
            Loom,
            Model,
            Column,
            PrimaryKeyColumn,
            CreatedAtColumn,
            TableColumn,
            ForeignKeyColumn,
            ColumnValue,
            Include,
        )

        import pytest
        from dataloom.exceptions import UnknownRelationException

        from dataloom.keys import PgConfig

        pg_loom = Loom(
            dialect="postgres",
            database=PgConfig.database,
            password=PgConfig.password,
            user=PgConfig.user,
        )

        class User(Model):
            __tablename__: TableColumn = TableColumn(name="users")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")
            username = Column(type="varchar", unique=True, length=255)
            tokenVersion = Column(type="int", default=0)

        class Profile(Model):
            __tablename__: TableColumn = TableColumn(name="profiles")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            avatar = Column(type="text", nullable=False)
            userId = ForeignKeyColumn(
                User,
                maps_to="1-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Post(Model):
            __tablename__: TableColumn = TableColumn(name="posts")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            completed = Column(type="boolean", default=False)
            title = Column(type="varchar", length=255, nullable=False)
            # timestamps
            createdAt = CreatedAtColumn()
            # relations
            userId = ForeignKeyColumn(
                User,
                maps_to="1-N",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        class Category(Model):
            __tablename__: TableColumn = TableColumn(name="categories")
            id = PrimaryKeyColumn(
                type="int", auto_increment=True, nullable=False, unique=True
            )
            type = Column(type="varchar", length=255, nullable=False)

            postId = ForeignKeyColumn(
                Post,
                maps_to="N-1",
                type="int",
                required=True,
                onDelete="CASCADE",
                onUpdate="CASCADE",
            )

        conn, tables = pg_loom.connect_and_sync(
            [User, Profile, Post, Category], drop=True, force=True
        )

        userId = pg_loom.insert_one(
            instance=User,
            values=ColumnValue(name="username", value="@miller"),
        )

        profileId = pg_loom.insert_one(
            instance=Profile,
            values=[
                ColumnValue(name="userId", value=userId),
                ColumnValue(name="avatar", value="hello.jpg"),
            ],
        )
        for title in ["Hey", "Hello", "What are you doing", "Coding"]:
            pg_loom.insert_one(
                instance=Post,
                values=[
                    ColumnValue(name="userId", value=userId),
                    ColumnValue(name="title", value=title),
                ],
            )

        for cat in ["general", "education", "tech", "sport"]:
            pg_loom.insert_one(
                instance=Category,
                values=[
                    ColumnValue(name="postId", value=profileId),
                    ColumnValue(name="type", value=cat),
                ],
            )

        with pytest.raises(UnknownRelationException) as exec_info:
            pg_loom.find_by_pk(
                Profile,
                pk=1,
                select=["avatar", "id"],
                include=[
                    Include(
                        model=Category,
                    )
                ],
            )
        assert (
            str(exec_info.value)
            == 'The table "profiles" does not have relations "categories".'
        )
        with pytest.raises(UnknownRelationException) as exec_info:
            pg_loom.find_many(
                Profile,
                select=["avatar", "id"],
                include=[
                    Include(
                        model=Category,
                    )
                ],
            )
        assert (
            str(exec_info.value)
            == 'The table "profiles" does not have relations "categories".'
        )
        with pytest.raises(UnknownRelationException) as exec_info:
            pg_loom.find_by_pk(
                Profile,
                pk=1,
                select=["avatar", "id"],
                include=[
                    Include(
                        model=Category,
                    )
                ],
            )
        assert (
            str(exec_info.value)
            == 'The table "profiles" does not have relations "categories".'
        )
        with pytest.raises(UnknownRelationException) as exec_info:
            pg_loom.find_all(
                Profile,
                select=["avatar", "id"],
                include=[
                    Include(
                        model=Category,
                    )
                ],
            )
        assert (
            str(exec_info.value)
            == 'The table "profiles" does not have relations "categories".'
        )
        with pytest.raises(UnknownRelationException) as exec_info:
            pg_loom.find_one(
                Profile,
                select=["avatar", "id"],
                include=[
                    Include(
                        model=Category,
                    )
                ],
            )
        assert (
            str(exec_info.value)
            == 'The table "profiles" does not have relations "categories".'
        )

        with pytest.raises(UnknownRelationException) as exec_info:
            pg_loom.find_all(
                Profile,
                select=["avatar", "id"],
                include=[
                    Include(
                        model=User, has="many", include=[Include(model=Post, has="one")]
                    )
                ],
            )
        assert (
            str(exec_info.value)
            == 'The model "profiles" does not maps to "many" of "users".'
        )
        conn.close()

        conn.close()

    def test_self_relations_eager(self):
        from dataloom import (
            Loom,
            Model,
            Column,
            PrimaryKeyColumn,
            TableColumn,
            ForeignKeyColumn,
            ColumnValue,
            Include,
        )
        from dataloom.keys import PgConfig

        pg_loom = Loom(
            dialect="postgres",
            database=PgConfig.database,
            password=PgConfig.password,
            user=PgConfig.user,
        )

        class Employee(Model):
            __tablename__: TableColumn = TableColumn(name="employees")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")
            supervisorId = ForeignKeyColumn(
                "Employee", maps_to="1-1", type="int", required=False
            )

        conn, tables = pg_loom.connect_and_sync([Employee], force=True)

        empId = pg_loom.insert_one(
            instance=Employee, values=ColumnValue(name="name", value="John Doe")
        )

        _ = pg_loom.insert_bulk(
            instance=Employee,
            values=[
                [
                    ColumnValue(name="name", value="Michael Johnson"),
                    ColumnValue(name="supervisorId", value=empId),
                ],
                [
                    ColumnValue(name="name", value="Jane Smith"),
                    ColumnValue(name="supervisorId", value=empId),
                ],
            ],
        )

        emp_and_sup = pg_loom.find_by_pk(
            instance=Employee,
            pk=2,
            select=["id", "name", "supervisorId"],
            include=Include(
                model=Employee,
                has="one",
                select=["id", "name"],
                alias="supervisor",
            ),
        )

        assert emp_and_sup == {
            "id": 2,
            "name": "Michael Johnson",
            "supervisorId": 1,
            "supervisor": {"id": 1, "name": "John Doe"},
        }
        emp_and_sup = pg_loom.find_by_pk(
            instance=Employee,
            pk=1,
            select=["id", "name", "supervisorId"],
            include=Include(
                model=Employee,
                has="one",
                select=["id", "name"],
                alias="supervisor",
            ),
        )
        assert emp_and_sup == {
            "id": 1,
            "name": "John Doe",
            "supervisorId": None,
            "supervisor": None,
        }
        conn.close()

    def test_n2n_relations_eager(self):
        from dataloom import (
            Loom,
            Model,
            Column,
            PrimaryKeyColumn,
            TableColumn,
            ForeignKeyColumn,
            ColumnValue,
            Include,
        )
        from dataloom.keys import PgConfig

        pg_loom = Loom(
            dialect="postgres",
            database=PgConfig.database,
            password=PgConfig.password,
            user=PgConfig.user,
        )

        class Course(Model):
            __tablename__: TableColumn = TableColumn(name="courses")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")

        class Student(Model):
            __tablename__: TableColumn = TableColumn(name="students")
            id = PrimaryKeyColumn(type="int", auto_increment=True)
            name = Column(type="text", nullable=False, default="Bob")

        class StudentCourses(Model):
            __tablename__: TableColumn = TableColumn(name="students_courses")
            studentId = ForeignKeyColumn(table=Student, type="int")
            courseId = ForeignKeyColumn(table=Course, type="int")

        conn, tables = pg_loom.connect_and_sync(
            [Student, Course, StudentCourses], force=True
        )

        # insert the courses
        mathId = pg_loom.insert_one(
            instance=Course, values=ColumnValue(name="name", value="Mathematics")
        )
        engId = pg_loom.insert_one(
            instance=Course, values=ColumnValue(name="name", value="English")
        )
        phyId = pg_loom.insert_one(
            instance=Course, values=ColumnValue(name="name", value="Physics")
        )

        # create students

        stud1 = pg_loom.insert_one(
            instance=Student, values=ColumnValue(name="name", value="Alice")
        )
        stud2 = pg_loom.insert_one(
            instance=Student, values=ColumnValue(name="name", value="Bob")
        )
        stud3 = pg_loom.insert_one(
            instance=Student, values=ColumnValue(name="name", value="Lisa")
        )

        # enrolling students
        pg_loom.insert_bulk(
            instance=StudentCourses,
            values=[
                [
                    ColumnValue(name="studentId", value=stud1),
                    ColumnValue(name="courseId", value=mathId),
                ],  # enrolling Alice to mathematics
                [
                    ColumnValue(name="studentId", value=stud1),
                    ColumnValue(name="courseId", value=phyId),
                ],  # enrolling Alice to physics
                [
                    ColumnValue(name="studentId", value=stud1),
                    ColumnValue(name="courseId", value=engId),
                ],  # enrolling Alice to english
                [
                    ColumnValue(name="studentId", value=stud2),
                    ColumnValue(name="courseId", value=engId),
                ],  # enrolling Bob to english
                [
                    ColumnValue(name="studentId", value=stud3),
                    ColumnValue(name="courseId", value=phyId),
                ],  # enrolling Lisa to physics
                [
                    ColumnValue(name="studentId", value=stud3),
                    ColumnValue(name="courseId", value=engId),
                ],  # enrolling Lisa to english
            ],
        )

        alice = pg_loom.find_by_pk(
            Student,
            pk=stud1,
            select=["id", "name"],
            include=Include(model=Course, junction_table=StudentCourses, has="many"),
        )

        assert alice == {
            "id": 1,
            "name": "Alice",
            "courses": [
                {"id": 1, "name": "Mathematics"},
                {"id": 2, "name": "English"},
                {"id": 3, "name": "Physics"},
            ],
        }

        english = pg_loom.find_by_pk(
            Course,
            pk=engId,
            select=["id", "name"],
            include=Include(model=Student, junction_table=StudentCourses, has="many"),
        )

        assert english == {
            "id": 2,
            "name": "English",
            "students": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Lisa"},
            ],
        }
        conn.close()
