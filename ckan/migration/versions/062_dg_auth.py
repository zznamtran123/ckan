from migrate import *

def upgrade(migrate_engine):

    update_schema = '''
BEGIN;

ALTER TABLE "user"
    ADD COLUMN authorized boolean DEFAULT FALSE;

COMMIT;

'''
    migrate_engine.execute(update_schema)


    # authorize any sysadmins
    import ckan.model as model
    sysadmins = model.Session.query(model.SystemRole).filter_by(role=model.Role.ADMIN)
    for sysadmin in sysadmins:

        user = model.User.get(sysadmin.user.id)
        user.authorized = True
        model.Session.commit()
