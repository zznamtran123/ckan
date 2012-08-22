import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types, Column, Table, ForeignKey, and_, func

import meta
import domain_object
import types as _types
import package as _package

__all__ = ['OrganisationRole', 'Permission', 'permission_table',
           'organisationrole_table']

organisationrole_table = sa.Table(
    'organisationrole', meta.metadata,
    Column('id', types.UnicodeText, primary_key=True,
           default=_types.make_uuid),
    Column('name', types.UnicodeText),
)

role_permission_table = Table('organisationrole_permission', meta.metadata,
    Column('organisationrole_id', types.UnicodeText, ForeignKey('organisationrole.id')),
    Column('permission_id', types.UnicodeText, ForeignKey('permission.id'))
)

permission_table = Table(
    'permission', meta.metadata,
    Column('id', types.UnicodeText, primary_key=True,
           default=_types.make_uuid),
    Column('name', types.UnicodeText),
    Column('description', types.UnicodeText)
)


class OrganisationRole(domain_object.DomainObject):

    @classmethod
    def get(cls, name):
        return meta.Session.query(OrganisationRole).filter(
            OrganisationRole.name == name).first()


class Permission(domain_object.DomainObject):

    @classmethod
    def get(cls, reference):
        query = meta.Session.query(cls).filter(cls.id==reference)
        pkg = query.first()
        if pkg == None:
            pkg = cls.by_name(reference)
        return pkg


meta.mapper(Permission, permission_table)

meta.mapper(OrganisationRole, organisationrole_table,
    properties={'permissions': orm.relationship(Permission,
                               secondary=role_permission_table)})
