# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DST_DIR = os.path.join(BASE_DIR, 'dst')

params = {
    'app_name': 'department',
    'app_fields': [
        'name', 'principal', 'principal_duty',
        'principal_ecard', 'principal_email', 'principal_phone',
        'coordinator', 'coordinator_duty', 'coordinator_ecard',
        'coordinator_email', 'coordinator_phone', 'coordinator_qq',
    ],
    'app_bulkupdate_fields': [
        'name', 'principal', 'principal_duty',
        'principal_ecard', 'principal_email', 'principal_phone',
        'coordinator', 'coordinator_duty', 'coordinator_ecard',
        'coordinator_email', 'coordinator_phone', 'coordinator_qq',
    ],
}

charfield_def = " = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('"
app_model_fields = charfield_def


def code_gen(src, dst, filename='', **kwargs):
    with open(src) as in_f:
        code_str = in_f.read()
        dst_file = (kwargs['app_name'] if not filename else filename) + '.py'
        if not os.path.isdir(dst):
            os.makedirs(dst)
        with open(os.path.join(dst, dst_file), 'w') as out_f:
            code = code_str.format(**kwargs)
            print(code.strip("'\n"), file=out_f)


if __name__ == '__main__':
    if not os.path.isdir(DST_DIR):
        os.makedirs(DST_DIR)

    # api
    src = os.path.join(BASE_DIR, 'scaffold', 'api', 'system')
    dst = os.path.join(DST_DIR, params['app_name'], 'api')
    api_params = {
        'app_name': params['app_name'],
        'app_name_first_uppercase': params['app_name'].capitalize(),
        'app_fields': "'" + "\', '".join(params['app_fields']) + "'",
    }
    code_gen(src, dst, **api_params)

    # forms
    src = os.path.join(BASE_DIR, 'scaffold', 'forms', 'system')
    dst = os.path.join(DST_DIR, params['app_name'], 'forms')
    api_params = {
        'app_name': params['app_name'],
        'app_name_first_uppercase': params['app_name'].capitalize(),
        'app_fields': "'" + "\', '".join(params['app_fields']) + "'",
        'app_bulkupdate_fields': "'" + "\', '".join(params['app_bulkupdate_fields']) + "'",
    }
    code_gen(src, dst, **api_params)

    # models
    src = os.path.join(BASE_DIR, 'scaffold', 'models', 'system')
    dst = os.path.join(DST_DIR, params['app_name'], 'models')
    list = []
    for field in params['app_fields']:
        var = field.split('_')
        list.append(field + charfield_def + var[0].capitalize() + ' ' + ' '.join(var[1:]) + "'))")
    api_params = {
        'app_name': params['app_name'],
        'app_name_first_uppercase': params['app_name'].capitalize(),
        'app_model_fields': '\n    '.join(list),
    }
    code_gen(src, dst, **api_params)

    # serializers
    src = os.path.join(BASE_DIR, 'scaffold', 'serializers', 'system')
    dst = os.path.join(DST_DIR, params['app_name'], 'serializers')
    api_params = {
        'app_name': params['app_name'],
        'app_name_first_uppercase': params['app_name'].capitalize(),
        'app_fields': "'" + "\', '".join(params['app_fields']) + "'",
    }
    code_gen(src, dst, **api_params)

    # # templates
    # src = os.path.join(BASE_DIR, 'scaffold', 'api', 'system')
    # dst = os.path.join(DST_DIR, params['app_name'], 'api')
    # api_params = {
    #     'app_name': params['app_name'],
    #     'app_fields': ', '.join(params['app_fields']),
    # }
    # code_gen(src, dst, **api_params)
    #
    # urls
    api_params = {
        'app_name': params['app_name'],
        'app_name_first_uppercase': params['app_name'].capitalize(),
    }

    src = os.path.join(BASE_DIR, 'scaffold', 'urls', 'api_urls')
    dst = os.path.join(DST_DIR, params['app_name'], 'urls')
    code_gen(src, dst, filename='api_urls', **api_params)

    src = os.path.join(BASE_DIR, 'scaffold', 'urls', 'views_urls')
    dst = os.path.join(DST_DIR, params['app_name'], 'urls')
    code_gen(src, dst, filename='views_urls', **api_params)

    # views
    src = os.path.join(BASE_DIR, 'scaffold', 'views', 'system')
    dst = os.path.join(DST_DIR, params['app_name'], 'views')
    code_gen(src, dst, **api_params)


