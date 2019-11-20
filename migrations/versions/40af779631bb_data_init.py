"""data_init

Revision ID: 40af779631bb
Revises: 60ffb2f52d51
Create Date: 2019-11-15 18:05:49.347864

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.String)
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    address = sa.Column(sa.String)
    register_on = sa.Column(sa.DateTime)
    is_confirmed = sa.Column(sa.Boolean)
    role = sa.Column(sa.String)
    authenticated = sa.Column(sa.Boolean)


class Datasource(Base):
    __tablename__ = 'datasources'

    id = sa.Column(sa.Integer, primary_key=True)
    site_name = sa.Column(sa.String)
    site_url = sa.Column(sa.String)




# revision identifiers, used by Alembic.
revision = '40af779631bb'
down_revision = '60ffb2f52d51'
branch_labels = None
depends_on = None


credentials = [
    {
        'role': 'user',
        'username': 'user',
        'password': '$pbkdf2-sha256$29000$DmFs7X0PAcC41zonRCjFmA$x7kmrgRS0yZ0tE/y3kjt36szOc0TgEtzTCozH8hfg4k', # user12345
    },
    {
        'role': 'admin',
        'username': 'admin',
        'password': '$pbkdf2-sha256$29000$O0fIWUuJsVYKAeB8b805Zw$9Nru6otB88XTl4BK9jyuKV1frUKMxj9Euz9Jv1NacGo', # admin12345
    },
]

datasources = [
    {
        'site_name': 'nomornet',
        'site_url': 'https://www.nomor.net/'
    }
]


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    for credential in credentials:
        source = User(
            phone='082111111111',
            address='Lebuawu Pecangaan Jepara',
            register_on=datetime(2019, 9, 1, 1, 0, 0),
            is_confirmed=True,
            authenticated=False,
            **credential
        )
        session.add(source)
        session.commit()

    for datasource in datasources:
        source = Datasource(**datasource)
        session.add(source)
        session.commit()


def downgrade():
    pass

