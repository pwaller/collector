# -*- encoding: utf-8 -*-

from json import dumps

from datetime import datetime


def x(v):
    if isinstance(v, datetime):
        return "{0}-{1}-{2}".format(v.year, v.month, v.day)
        # return v.strftime("%Y-%m-%d")
    return v


def asdict(self):
    return {}
    ks = self.__mapper__.columns.keys()
    # ks = ["title"]
    return {k: k for k in ks if x(getattr(self, k))}
    # return {k: x(getattr(self, k)) for k in ks if x(getattr(self, k))}

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Float, Integer,
                        MetaData, Numeric, SmallInteger, String, ForeignKey)
from sqlalchemy import types

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
    CatDate = Column('CatDate', DateTime)

    music = relationship("Music", backref="cover")

    # Maybe unused fields
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
    AcqDateQ = Column('AcqDateQ', DateTime)
    CostQ = Column('CostQ', Numeric)
    ValueQ = Column('ValueQ', Numeric)
    CrysFlagC = Column('CrysFlagC', Boolean, nullable=False, default=False)


class KeySigString(types.TypeDecorator):
    impl = types.String

    def process_result_value(self, value, dialect):
        return sharp_flatify(value)


def sharp_flatify(text):
    if text is not None:
        if text.lower().endswith(" min"):
            # raise RuntimeError()
            text = text[:-len(" min")].lower()
        return text.replace(u"Þ", u"♭").replace(u"þ", u"♭").replace(u"#", u"♯")
    return ""


def nbspify(text):
    return text.replace(" ", "&nbsp;")


class Music(Base):
    __tablename__ = "Music"
    __table_args__ = {"extend_existing": True, "sqlite_autoincrement": True}

    def __repr__(self):
        return "<Music id={0} title={1}>".format(self.id, self.title)

    @property
    def json(self):
        return dumps(asdict(self))

    def soloists(self, request):
        x = [self.Solo1, self.Solo2, self.Solo3, self.Solo4]

        def reorder(x):
            x = [_.strip() for _ in x.split(",")]
            reordered = u"&nbsp;".join([x[-1]] + x[:-1])
            # TODO(pwaller): Add request.route_url('soloists')
            url = request.route_url("soloists", soloist=reordered)
            return u'<a href="{}">{}</a>'.format(url, reordered)

        x = [reorder(x) for x in x if x]
        if not x:
            return u""
        if len(x) == 1:
            (x,) = x
            return x
        return u" ".join(x)
        # return ", ".join(x[:-1]) + " and " + x[-1]

    @property
    def conductor(self):
        if self.Conductor:
            return self.Conductor.replace(u" ", "&nbsp;")
        return u""

    def ensemble(self, request):
        if self.Ensemble:
            return self.Ensemble.replace(u" ", "&nbsp;")
        return u""

    # Fields from Patrick's email:
    # Music: Composer, opus no, quantity, work type, instrument, number, key,
    # title of work, soloist (x4), conductor, chorus, ensemble, class of music.

    id = Column('MusicNo', Integer, primary_key=True, autoincrement=True)
    title = Column('FullTitle', KeySigString)

    CoverRef = Column('CoverRef', Integer, ForeignKey('Covers.CoverNo'))

    Composer = Column('Composer', String)
    OpusX = Column('OpusX', String)
    WorkQty = Column('WorkQty', SmallInteger)
    MusicType = Column('MusicType', String)
    Instrument = Column('Instrument', String)
    WorkNoX = Column('WorkNoX', String)
    KeySig = Column('KeySig', KeySigString)
    WorkName = Column('WorkName', String)
    Solo1 = Column('Solo1', String)
    Solo2 = Column('Solo2', String)
    Solo3 = Column('Solo3', String)
    Solo4 = Column('Solo4', String)
    Conductor = Column('Conductor', String)
    Chorus = Column('Chorus', String)
    Ensemble = Column('Ensemble', String)
    MusicClass = Column('MusicClass', String)

    # Possibly unused fields
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
