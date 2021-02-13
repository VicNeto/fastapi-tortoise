aerich init -t src.db.TORTOISE_ORM
aerich init-db
aerich migrate --name add_column
aerich upgrade