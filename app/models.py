# coding: utf-8
# Generated using sqlacodegen from Tyler's local postgresql db based on his proposed data dictionary
from sqlalchemy import Boolean, CheckConstraint, Column, Date, Enum, ForeignKey, Integer, SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Attitude(Base):
    __tablename__ = 'attitude'
    __table_args__ = (
        CheckConstraint('id > 0'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('attitude_seq'::regclass)"))
    title = Column(String(191), nullable=False, unique=True)

    seekers = relationship('Seekerprofile', secondary='seekerattitude')


class Skill(Base):
    __tablename__ = 'skill'
    __table_args__ = (
        CheckConstraint('id > 0'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('skill_seq'::regclass)"))
    title = Column(String(191), nullable=False, unique=True)
    type = Column(Enum('tech', 'biz', name='skill_types'), nullable=False)


class Useraccount(Base):
    __tablename__ = 'useraccount'
    __table_args__ = (
        CheckConstraint('id > 0'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('useraccount_seq'::regclass)"))
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


class Jobpost(Base):
    __tablename__ = 'jobpost'
    __table_args__ = (
        CheckConstraint('company_id > 0'),
        CheckConstraint('id > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('jobpost_seq'::regclass)"))
    company_id = Column(ForeignKey('companyprofile.company_id'), nullable=False)
    job_title = Column(String(191), nullable=False)
    is_remote = Column(Boolean)
    city = Column(String(191), server_default=text("NULL::character varying"))
    state_abbv = Column(String(2), server_default=text("NULL::character varying"))
    description = Column(Text)

    company = relationship('Companyprofile')


t_seekerattitude = Table(
    'seekerattitude', metadata,
    Column('seeker_id', ForeignKey('seekerprofile.seeker_id'), nullable=False),
    Column('attitude_id', ForeignKey('attitude.id'), nullable=False),
    CheckConstraint('attitude_id > 0'),
    CheckConstraint('seeker_id > 0'),
    UniqueConstraint('seeker_id', 'attitude_id')
)


class Seekerhistoryeducation(Base):
    __tablename__ = 'seekerhistoryeducation'
    __table_args__ = (
        CheckConstraint('id > 0'),
        CheckConstraint('seeker_id > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('seekerhistoryeducation_seq'::regclass)"))
    seeker_id = Column(ForeignKey('seekerprofile.seeker_id'), nullable=False)
    education_level = Column(String(191), nullable=False)
    study_field = Column(String(191), nullable=False)
    school = Column(String(191), server_default=text("NULL::character varying"))
    city = Column(String(191), server_default=text("NULL::character varying"))
    state_abbv = Column(String(2), server_default=text("NULL::character varying"))
    active_enrollment = Column(SmallInteger)
    start_date = Column(Date)
    end_date = Column(Date)

    seeker = relationship('Seekerprofile')


class Seekerhistoryjob(Base):
    __tablename__ = 'seekerhistoryjob'
    __table_args__ = (
        CheckConstraint('id > 0'),
        CheckConstraint('seeker_id > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('seekerhistoryjob_seq'::regclass)"))
    seeker_id = Column(ForeignKey('seekerprofile.seeker_id'), nullable=False)
    job_title = Column(String(191), nullable=False)
    company = Column(String(191), server_default=text("NULL::character varying"))
    city = Column(String(191), server_default=text("NULL::character varying"))
    state_abbv = Column(String(2), server_default=text("NULL::character varying"))
    active_employment = Column(SmallInteger)
    start_date = Column(Date)
    end_date = Column(Date)

    seeker = relationship('Seekerprofile')


t_seekerskill = Table(
    'seekerskill', metadata,
    Column('seeker_id', ForeignKey('seekerprofile.seeker_id'), nullable=False),
    Column('skill_id', ForeignKey('skill.id'), nullable=False),
    Column('skill_level', Enum('1', '2', '3', '4', '5', name='skill_levels'), nullable=False, comment='1=familiar,5=expert'),
    CheckConstraint('seeker_id > 0'),
    CheckConstraint('skill_id > 0'),
    UniqueConstraint('seeker_id', 'skill_id')
)


class Jobpostattitude(Base):
    __tablename__ = 'jobpostattitude'
    __table_args__ = (
        CheckConstraint('attitude_id > 0'),
        CheckConstraint('id > 0'),
        CheckConstraint('jobpost_id > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('jobpostattitude_seq'::regclass)"))
    jobpost_id = Column(ForeignKey('jobpost.id'), nullable=False)
    attitude_id = Column(ForeignKey('attitude.id'), nullable=False)
    importance_level = Column(Enum('1', '2', '3', '4', '5', '6', '7', name='importance_levels'), nullable=False, comment='1=required,4=preferred,7=optional')

    attitude = relationship('Attitude')
    jobpost = relationship('Jobpost')


class Jobpostskill(Base):
    __tablename__ = 'jobpostskill'
    __table_args__ = (
        CheckConstraint('id > 0'),
        CheckConstraint('jobpost_id > 0'),
        CheckConstraint('skill_id > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('jobpostskill_seq'::regclass)"))
    jobpost_id = Column(ForeignKey('jobpost.id'), nullable=False)
    skill_id = Column(ForeignKey('skill.id'), nullable=False)
    skill_level_min = Column(Enum('1', '2', '3', '4', '5', name='skill_levels'), nullable=False, comment='1=familiar,5=expert')
    importance_level = Column(Enum('1', '2', '3', '4', '5', '6', '7', name='importance_levels'), nullable=False, comment='1=required,4=preferred,7=optional')

    jobpost = relationship('Jobpost')
    skill = relationship('Skill')
