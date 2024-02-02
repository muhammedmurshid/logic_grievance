{
    'name': "Grievance",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail', 'logic_base'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/grievance_form.xml',
        'views/web_form.xml',
        'views/types.xml',
        'security/rules.xml',
        'data/activity.xml',
        # 'views/assets.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'logic_greivance/static/src/js/test.js'],
    # },
    'demo': [],
    'summary': "Grievance_form",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
