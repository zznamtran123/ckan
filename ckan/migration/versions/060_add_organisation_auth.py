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

CREATE TABLE permission (
	id text NOT NULL,
	name text,
	description text,
	organisationrole_id text NOT NULL
);

ALTER TABLE organisationrole
	ADD CONSTRAINT organisationrole_pkey PRIMARY KEY (id);

ALTER TABLE permission
	ADD CONSTRAINT permission_pkey PRIMARY KEY (id);

ALTER TABLE permission
	ADD CONSTRAINT permission_organisationrole_id_fkey FOREIGN KEY (organisationrole_id) REFERENCES organisationrole(id);

COMMIT;
    '''
    )
