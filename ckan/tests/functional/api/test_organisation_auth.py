from nose.tools import assert_equal
from pylons import config
import pylons.test
import paste

from ckan.lib.create_test_data import CreateTestData
import ckan.lib.helpers as h
import ckan.model as model

_json = h.json

class TestUserController(object):

    @classmethod
    def setup_class(cls):
        CreateTestData.create()
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)
        cls.sysadmin_user = model.User.get('testsysadmin')
        cls.extra_environ = {'Authorization' : str(cls.sysadmin_user.apikey)}

        p = model.Permission(name="package.view")
        model.Session.add(p)
        model.Session.commit()

    @classmethod
    def teardown_class(self):
        model.repo.rebuild_db()

    def test_role_create(self):
        # Currently not adding the permissions to the new role.... hmm...
        params = _json.dumps({'name':'test_role', 'permissions': [{"name":"package.view"}]})

        response = self.app.post('/api/action/organization_role_create',
                params=params, extra_environ=self.extra_environ).json
        assert response['success'] is True

    def test_role_delete_succeed(self):
        params = _json.dumps({'name':'test_role', 'permissions': [{"name":"package.view"}]})
        response = self.app.post('/api/action/organization_role_create',
                params=params, extra_environ=self.extra_environ).json
        assert response['success'] is True

        params = _json.dumps({'id':'test_role'})
        response = self.app.post('/api/action/organization_role_delete',
                params=params, extra_environ=self.extra_environ).json
        assert response['success'] is True

    def test_role_delete_fail(self):
        params = _json.dumps({'id':'non-existant'})
        response = self.app.post('/api/action/organization_role_delete',
                params=params, extra_environ=self.extra_environ, status=404)

    def test_role_show_succeed(self):
        params = _json.dumps({'name':'test_role', 'permissions': [{"name":"package.view"}]})
        response = self.app.post('/api/action/organization_role_create',
                params=params, extra_environ=self.extra_environ).json
        assert response['success'] is True

        params = _json.dumps({'id':'test_role'})
        response = self.app.post('/api/action/organization_role_show',
                params=params, extra_environ=self.extra_environ).json
        assert response['success'] is True

    def test_role_show_fail(self):
        params = _json.dumps({'id':'non-existant'})
        self.app.post('/api/action/organization_role_show',
                params=params, extra_environ=self.extra_environ, status=404)

    def test_role_list(self):
        params = _json.dumps({})
        response = self.app.post('/api/action/organization_role_list',
                params=params, extra_environ=self.extra_environ, status=200).json
        assert response['success'] == True
        print response
