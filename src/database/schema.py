from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.dialects.postgresql import UUID

#
# *** Best Practice: Use SQLAlchemy for DB models, Pydantic for I/O models *** 
# You should not use Pydantic to define your models.py ORM layer. Pydantic is designed for 
# validation and serialization of input/output data—not for managing database schemas, relationships,
# or querying behavior. SQLAlchemy is purpose-built for that.
#

metadata = MetaData()

BookTable = Table(
    "book",
    metadata, # add table to sqlalchemy metadata collection
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("category", String, nullable=True),
    schema="play_pen"
)


AuthorTable = Table(
    "author",
    metadata, # add table to sqlalchemy metadata collection
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String, nullable=False),
    schema="play_pen"
)
