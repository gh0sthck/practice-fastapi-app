"""
Configuration file. 

Contains database settings: Postgresql name, user, port, host and dsn; project settings and
tests settings: test database, base url to test.
You need to import `settings` variable, from end file, not Settings classes.
"""

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Database: PostgreSQL.
    Change `name`, `user` and `password` fields, other only of needs.
    `host`/`port` changes only if you start app in container or production.
    """

    name: str = "bakerydb"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "root"

    @property
    def dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class TestingSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings(
        name="bakerydb_test",
    )
    base_url: str = "http://127.0.0.1:8000"  # Change if you have another port/start into https


class Settings(BaseSettings):
    debug: bool = True  # Change to False if start into production

    db: DatabaseSettings = DatabaseSettings()
    tests: TestingSettings = TestingSettings()

    title: str = "Пекраня"
    description: str = "API приложения пекрани на FastAPI"
    docs_url: str = "/api/docs"


setting = Settings()  # import this, not <Settings>
