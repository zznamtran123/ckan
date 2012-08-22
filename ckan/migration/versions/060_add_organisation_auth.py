from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    metadata = MetaData()
    metadata.bind = migrate_engine
    migrate_engine.execute('''
BEGIN;

CREATE TABLE organisationrole (
	id text NOT NULL,
	name text
);

CREATE TABLE organisationrole_permission (
    organisationrole_id text NOT NULL,
    permission_id text NOT NULL
);

CREATE TABLE permission (
	id text NOT NULL,
	name text,
	description text
);

ALTER TABLE organisationrole
	ADD CONSTRAINT organisationrole_pkey PRIMARY KEY (id);

ALTER TABLE permission
	ADD CONSTRAINT permission_pkey PRIMARY KEY (id);

ALTER TABLE organisationrole_permission
	ADD CONSTRAINT organisationrole_permission_id_fkey FOREIGN KEY (organisationrole_id) REFERENCES organisationrole(id);

ALTER TABLE organisationrole_permission
	ADD CONSTRAINT permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permission(id);

COMMIT;
    '''
    )
