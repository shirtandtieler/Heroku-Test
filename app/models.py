# coding: utf-8
# Attempted to be generated from Tyler's local postgresql db based on his proposed data dictionary
# BUT that didn't work so I simplified it
from sqlalchemy import Boolean, CheckConstraint, Column, Date, Enum, ForeignKey, Integer, SmallInteger, String, Sequence, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from app import db

Base = declarative_base()
metadata = Base.metadata


class Attitude(db.Model, Base):
    __tablename__ = 'attitude'
    __table_args__ = (
        CheckConstraint('id > 0'),
    )

    id = Column(Integer, Sequence('attitude_seq'), primary_key=True)
    title = Column(String(191), nullable=False, unique=True)

    seekers = relationship('Seekerprofile', secondary='seekerattitude')


class Skill(db.Model, Base):
    __tablename__ = 'skill'
    __table_args__ = (
        CheckConstraint('id > 0'),
    )

    id = Column(Integer, Sequence('skill_seq'), primary_key=True)
    title = Column(String(191), nullable=False, unique=True)
    type = Column(Enum('tech', 'biz', name='skill_types'), nullable=False)


class Useraccount(db.Model, Base):
    __tablename__ = 'useraccount'
    __table_args__ = (
        CheckConstraint('id > 0'),
    )

    id = Column(Integer, Sequence('useraccount_seq'), primary_key=True)
    account_type = Column(Enum('Seeker', 'Company', 'Admin', name='account_types'), nullable=False)
    email = Column(String(191), nullable=False, unique=True, comment='login email')
    password = Column(String(191), nullable=False)


t_companyprofile = Table(
    'companyprofile', metadata,
    Column('company_id', ForeignKey('useraccount.id'), nullable=False, unique=True),
    Column('company_name', String(191), server_default=text("NULL::character varying")),
    Column('city', String(191), server_default=text("NULL::character varying")),
    Column('state_abbv', String(2), server_default=text("NULL::character varying")),
    Column('zip_code', String(5), server_default=text("NULL::character varying")),
    Column('website', String(191), server_default=text("NULL::character varying")),
    CheckConstraint('company_id > 0')
)


t_seekerprofile = Table(
    'seekerprofile', metadata,
    Column('seeker_id', ForeignKey('useraccount.id'), nullable=False, unique=True),
    Column('contact_email', String(191), nullable=False),
    Column('first_name', String(191), server_default=text("NULL::character varying")),
    Column('last_name', String(191), server_default=text("NULL::character varying")),
    Column('contact_phone', Integer),
    Column('city', String(191), server_default=text("NULL::character varying")),
    Column('state_abbv', String(2), server_default=text("NULL::character varying")),
    Column('zip_code', String(5), server_default=text("NULL::character varying")),
    CheckConstraint('seeker_id > 0')
)


t_useractivity = Table(
    'useractivity', metadata,
    Column('user_id', ForeignKey('useraccount.id'), nullable=False, unique=True),
    Column('is_active', Boolean, nullable=False, server_default=text("true")),
    Column('join_date', TIMESTAMP(precision=0), nullable=False, server_default=text("now()")),
    Column('last_login', TIMESTAMP(precision=0), nullable=False, server_default=text("now()")),
    CheckConstraint('user_id > 0')
)