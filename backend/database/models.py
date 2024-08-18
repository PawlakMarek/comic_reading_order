"""
This module defines SQLAlchemy models for representing comic book data.

It includes models for characters, comics, creators, events, series, and stories.
Many-to-many relationships between these entities are defined using association tables.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association tables for many-to-many relationships
character_comic_association = Table(
    "characters_comics",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id")),
    Column("comic_id", Integer, ForeignKey("comics.id")),
)

comic_creator_association = Table(
    "comics_creators",
    Base.metadata,
    Column("comic_id", Integer, ForeignKey("comics.id")),
    Column("creator_id", Integer, ForeignKey("creators.id")),
)

comic_event_association = Table(
    "comics_events",
    Base.metadata,
    Column("comic_id", Integer, ForeignKey("comics.id")),
    Column("event_id", Integer, ForeignKey("events.id")),
)


class Character(Base):
    """
    Represents a character in the comic book universe.
    """

    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, doc="Unique identifier for the character.")
    name = Column(String(255), nullable=False, doc="Name of the character.")
    description = Column(String, doc="Brief description of the character.")
    comics = relationship(
        "Comic", secondary=character_comic_association, back_populates="characters"
    )


class Comic(Base):
    """
    Represents a comic book issue.
    """

    __tablename__ = "comics"
    id = Column(Integer, primary_key=True, doc="Unique identifier for the comic.")
    title = Column(String(255), nullable=False, doc="Title of the comic issue.")
    description = Column(String, doc="Brief description of the comic issue.")
    issue_number = Column(Integer, doc="Issue number within the series.")
    series_id = Column(
        Integer,
        ForeignKey("series.id"),
        doc="Foreign key to the series this comic belongs to.",
    )
    series = relationship("Series", back_populates="comics")
    characters = relationship(
        "Character", secondary=character_comic_association, back_populates="comics"
    )
    creators = relationship(
        "Creator", secondary=comic_creator_association, back_populates="comics"
    )
    events = relationship(
        "Event", secondary=comic_event_association, back_populates="comics"
    )
    event_id = Column(Integer, ForeignKey("events.id"))
    stories = relationship("Story", back_populates="comic")


class Creator(Base):
    """
    Represents a creator (writer, artist, etc.) of comic books.
    """

    __tablename__ = "creators"
    id = Column(Integer, primary_key=True, doc="Unique identifier for the creator.")
    name = Column(String(255), nullable=False, doc="Name of the creator.")
    role = Column(String(255), doc="Role of the creator (e.g., writer, artist, etc.).")
    comics = relationship(
        "Comic", secondary=comic_creator_association, back_populates="creators"
    )


class Event(Base):
    """
    Represents a major event or storyline in the comic book universe.
    """

    __tablename__ = "events"
    id = Column(Integer, primary_key=True, doc="Unique identifier for the event.")
    title = Column(String(255), nullable=False, doc="Title of the event.")
    description = Column(String, doc="Brief description of the event.")
    comics = relationship(
        "Comic", secondary=comic_event_association, back_populates="event"
    )


class Series(Base):
    """
    Represents a series of comic book issues.
    """

    __tablename__ = "series"
    id = Column(Integer, primary_key=True, doc="Unique identifier for the series.")
    title = Column(String(255), nullable=False, doc="Title of the series.")
    description = Column(String, doc="Brief description of the series.")
    comics = relationship("Comic", back_populates="series")


class Story(Base):
    """
    Represents a story arc within a comic book issue.
    """

    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, doc="Unique identifier for the story.")
    title = Column(String(255), nullable=False, doc="Title of the story.")
    description = Column(String, doc="Brief description of the story.")
    comic_id = Column(
        Integer,
        ForeignKey("comics.id"),
        doc="Foreign key to the comic issue this story belongs to.",
    )
    comic = relationship("Comic", back_populates="stories")
