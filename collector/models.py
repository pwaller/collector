from json import dumps

from datetime import datetime

def x(v):
    if isinstance(v, datetime):
        return "{0}-{1}-{2}".format(v.year, v.month, v.day)
        # return v.strftime("%Y-%m-%d")
    return v

def asdict(self):
    return {k: x(getattr(self, k)) for k in self.__mapper__.columns.keys() if x(getattr(self, k))}

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Float, Integer,
                        MetaData, Numeric, SmallInteger, String, ForeignKey)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)

#     def __init__(self, name, value):
#         self.name = name
#         self.value = value

# Index('my_index', MyModel.name, unique=True, mysql_length=255)
class Cover(Base):
    __tablename__ = "Covers"
    __table_args__ = {"extend_existing": True, "sqlite_autoincrement": True}

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Cover id={0} title={1}>".format(self.id, self.title)

    id = Column('CoverNo', Integer, primary_key=True, autoincrement=True)
    title = Column('CoverTitle', String)
    Format = Column('Format', String)
    CoverSet = Column('CoverSet', SmallInteger)
    Label = Column('Label', String)
    CatNo = Column('CatNo', String)
    AnDig = Column('AnDig', String)
    MonSter = Column('MonSter', String)
    PreRec = Column('PreRec', String)
    NR = Column('NR', String)
    RecSource = Column('RecSource', String)
    AcqDateX = Column('AcqDateX', String)
    CostX = Column('CostX', String)
    ValueX = Column('ValueX', String)
    Acquisition = Column('Acquisition', String)
    IndexAlpha = Column('IndexAlpha', String)
    IndexNumeric = Column('IndexNumeric', Integer)
    Loc1 = Column('Loc1', String)
    Loc2 = Column('Loc2', String)
    Condition = Column('Condition', String)
    Review = Column('Review', String)
    Loan = Column('Loan', String)
    UserDefC = Column('UserDefC', String)
    CommentsC = Column('CommentsC', String)
    FlagC = Column('FlagC', Boolean, nullable=False, default=False)
    IconNo = Column('IconNo', SmallInteger)
    CatDate = Column('CatDate', DateTime)
    AcqDateQ = Column('AcqDateQ', DateTime)
    CostQ = Column('CostQ', Numeric)
    ValueQ = Column('ValueQ', Numeric)
    CrysFlagC = Column('CrysFlagC', Boolean, nullable=False, default=False)

    music = relationship("Music")


class Music(Base):
    __tablename__ = "Music"
    __table_args__ = {"extend_existing": True, "sqlite_autoincrement": True}

    def __repr__(self):
        return "<Music id={0} title={1}>".format(self.id, self.title)

    @property
    def json(self):
        return dumps(asdict(self))

    id = Column('MusicNo', Integer, primary_key=True, autoincrement=True)
    title = Column('FullTitle', String)

    CoverRef = Column('CoverRef', Integer, ForeignKey('Covers.CoverNo'))
    Composer = Column('Composer', String)
    OpusX = Column('OpusX', String)
    WorkQty = Column('WorkQty', SmallInteger)
    MusicType = Column('MusicType', String)
    Instrument = Column('Instrument', String)
    WorkNoX = Column('WorkNoX', String)
    KeySig = Column('KeySig', String)
    WorkName = Column('WorkName', String)
    Solo1 = Column('Solo1', String)
    Solo2 = Column('Solo2', String)
    Solo3 = Column('Solo3', String)
    Solo4 = Column('Solo4', String)
    Conductor = Column('Conductor', String)
    Chorus = Column('Chorus', String)
    Ensemble = Column('Ensemble', String)
    MusicClass = Column('MusicClass', String)
    CompDateX = Column('CompDateX', String)
    PerfDateX = Column('PerfDateX', String)
    DurationX = Column('DurationX', String)
    TrackNo = Column('TrackNo', String)
    UserDefM = Column('UserDefM', String)
    CommentsM = Column('CommentsM', String)
    FlagM = Column('FlagM', Boolean, nullable=False, default=False)
    OpusQ = Column('OpusQ', Float)
    WorkNoQ = Column('WorkNoQ', Float)
    CompDateQ = Column('CompDateQ', DateTime)
    PerfDateQ = Column('PerfDateQ', DateTime)
    DurationQ = Column('DurationQ', DateTime)
    CrysFlagM = Column('CrysFlagM', Boolean, nullable=False, default=False)
