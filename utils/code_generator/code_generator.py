# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')
CHAR_FIELD_DEF = " = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('"
BOOTSTRAP_FIELD_DEF = '''
                            {%% bootstrap_field form.%s layout="horizontal" %%}'''
DETAIL_FIELD_DEF = '''
                                        <tr class="no-borders-tr">
                                            <td width="20%">{{% trans '{0}' %}}:</td>
                                            <td><b>{{{{ {1}.{2} }}}}</b></td>
                                        </tr>'''
HEADER_FIELD_DEF = '''
            <th class="text-center">{%% trans '%s' %%}</th>'''

COLUMN_FIELD_DEF = "{data: \"%s\"}"

module_name = 'system'
app_name = 'department'
fields = [
    'name', 'principal', 'principal_duty',
    'principal_ecard', 'principal_email', 'principal_phone',
    'coordinator', 'coordinator_duty', 'coordinator_ecard',
    'coordinator_email', 'coordinator_phone', 'coordinator_qq',
]

bulkupdate_fields = fields

char_field_list = []
bootstrap_field_list = []
detail_field_list = []
header_field_list = []
column_field_list = []

for field in fields:
    split_f = field.split('_')
    split_f = [split_f[0].capitalize(), *split_f[1:]]
    split_f_cat = ' '.join(split_f)
    char_field_list.append(field + CHAR_FIELD_DEF + split_f_cat + "'))")
    bootstrap_field_list.append(BOOTSTRAP_FIELD_DEF % field)
    detail_field_list.append(DETAIL_FIELD_DEF.format(split_f_cat, app_name, field))
    header_field_list.append(HEADER_FIELD_DEF % (split_f_cat))
    column_field_list.append(COLUMN_FIELD_DEF % field)

params = {
    'module_name': module_name,
    'module_name_first_uppercase': module_name.capitalize(),
    'app_name': app_name,
    'app_name_first_uppercase': app_name.capitalize(),
    'app_fields': "'" + "\', '".join(fields) + "'",
    'app_bulkupdate_fields': "'" + "\', '".join(bulkupdate_fields) + "'",
    'app_model_fields': '\n    '.join(char_field_list),
    'app_bootstrap_fields': ''.join(bootstrap_field_list),
    'app_detail_fields': ''.join(detail_field_list),
    'app_header_fields': ''.join(header_field_list),
    'app_column_fields': ', '.join(column_field_list),
}


def code_gen(src, dst, filename='', **kwargs):
    with open(src) as in_f:
        code_str = in_f.read()
        dst_file = kwargs['app_name'] + '.py' if not filename else filename
        if not os.path.isdir(dst):
            os.makedirs(dst)
        with open(os.path.join(dst, dst_file), 'w') as out_f:
            code = code_str.format(**kwargs)
            print(code, file=out_f)


if __name__ == '__main__':
    if not os.path.isdir(DIST_DIR):
        os.makedirs(DIST_DIR)

    src_dirs = ['api', 'forms', 'models', 'serializers', 'views']

    for dir in src_dirs:
        src = os.path.join(BASE_DIR, 'scaffold', dir, 'system')
        dst = os.path.join(DIST_DIR, params['module_name'] + 's', dir)
        code_gen(src, dst, **params)

    # templates
    pages = ['_%s_import_modal', '_%s_update_modal', '%s_bulk_update', '%s_create_update', '%s_detail', '%s_list']
    for page in pages:
        src = os.path.join(BASE_DIR, 'scaffold', 'templates', page % 'system')
        dst = os.path.join(DIST_DIR, params['module_name'] + 's', 'templates', params['module_name'] + 's')
        code_gen(src, dst, filename=page % params['app_name'] + '.html', **params)

    # urls
    src = os.path.join(BASE_DIR, 'scaffold', 'urls', 'api_urls')
    dst = os.path.join(DIST_DIR, params['module_name'] + 's', 'urls')
    code_gen(src, dst, filename='api_urls' + '.py', **params)

    src = os.path.join(BASE_DIR, 'scaffold', 'urls', 'views_urls')
    dst = os.path.join(DIST_DIR, params['module_name'] + 's', 'urls')
    code_gen(src, dst, filename='views_urls' + '.py', **params)
