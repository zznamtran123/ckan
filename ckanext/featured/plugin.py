import logging

import ckan.plugins as p

log = logging.getLogger(__name__)


class FeaturedPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IConfigurable, inherit=True)

    featured_groups_cache = None
    featured_orgs_cache = None

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'theme/templates')

    def configure(self, config):
        groups = config.get('ckan.featured_groups', '')
        if groups:
            log.warning('Config setting `ckan.featured_groups` is deprecated '
                        'please use `ckanext.featured.groups`')
        self.groups = config.get('ckanext.featured.groups', groups).split()
        self.groups_count = int(config.get('ckanext.featured.groups_count', 2))
        self.orgs = config.get('ckanext.featured.orgs', '').split()
        self.orgs_count = int(config.get('ckanext.featured.orgs_count', 2))

    def get_helpers(self):
        return {
            'featured_organizations': self.featured_orgs,
            'featured_groups': self.featured_groups,
        }

    def featured_groups(self):
        if not self.featured_groups_cache:
            self.get_featured_groups()
        vars = {'items': self.featured_groups_cache, 'type': 'group'}
        return p.toolkit.literal(
            p.toolkit.render('ckanext-featured/featured_groups.html', vars))

    def featured_orgs(self):
        if not self.featured_orgs_cache:
            self.get_featured_orgs()
        vars = {'items': self.featured_orgs_cache, 'type': 'org'}
        return p.toolkit.literal(
            p.toolkit.render('ckanext-featured/featured_groups.html', vars))

    def get_featured_groups(self):
        groups = self.featured_group_org(get_action='group_show',
                                         list_action='group_list',
                                         count=self.groups_count,
                                         items=self.groups)
        self.featured_groups_cache = groups

    def get_featured_orgs(self):
        orgs = self.featured_group_org(get_action='organization_show',
                                       list_action='organization_list',
                                       count=self.orgs_count,
                                       items=self.orgs)
        self.featured_orgs_cache = orgs



    def featured_group_org(self, items, get_action, list_action, count):
        def get_group(id):
            context = {'ignore_auth': True,
                       'limits': {'packages': 2},
                       'for_view': True}
            data_dict = {'id': id}

            try:
                group_dict = p.toolkit.get_action(get_action)(context, data_dict)
            except p.toolkit.ObjectNotFound:
                return None

            return group_dict

        groups_data = []

        extras = p.toolkit.get_action(list_action)({}, {})

        # list of found ids to prevent duplicates
        found = []
        for group_name in items + extras:
            group = get_group(group_name)
            # ckeck if duplicate
            if group['id'] in found:
                continue
            found.append(group['id'])
            if group:
                groups_data.append(group)
            if len(groups_data) == count:
                break

        return groups_data
