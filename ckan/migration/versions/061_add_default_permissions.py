from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    metadata = MetaData()
    metadata.bind = migrate_engine
    migrate_engine.execute('''
BEGIN;

CREATE OR REPLACE FUNCTION CREATE_UUID()
  RETURNS uuid AS
$BODY$
 SELECT CAST(md5(current_database()|| user ||current_timestamp ||random()) as uuid)
$BODY$
  LANGUAGE 'sql' VOLATILE;

INSERT INTO permission (id, name, description)
VALUES (CREATE_UUID(), 'package.view', 'View a dataset');

INSERT INTO permission (id, name, description)
VALUES (CREATE_UUID(), 'package.edit', 'Edit a dataset');

INSERT INTO permission (id, name, description)
VALUES (CREATE_UUID(), 'package.create', 'Create a dataset');

COMMIT;
    '''
    )
