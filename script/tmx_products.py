#!/usr/bin/python

import argparse
import datetime
import os
import subprocess
import sys
from ConfigParser import SafeConfigParser

# Get absolute path of ../config from the current script location (not the current folder)
config_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'config'))

# Read Transvision's configuration file from ../config/config.ini
config_file = os.path.join(config_folder, 'config.ini')
if not os.path.isfile(config_file):
    print 'Configuration file /app/config/config.ini is missing.'
    sys.exit(1)

parser = SafeConfigParser()
parser.read(config_file)
library_path = parser.get('config', 'libraries')
storage_path = os.path.join(parser.get('config', 'root'), 'TMX')

# Import Silme library (http://hg.mozilla.org/l10n/silme/)
silme_path = os.path.join(library_path, 'silme')

if not os.path.isdir(silme_path):
    try:
        print 'Cloning silme...'
        cmd_status = subprocess.check_output(
            ['hg', 'clone', 'https://hg.mozilla.org/l10n/silme',
                silme_path, '-u', 'silme-0.8.0'],
            stderr=subprocess.STDOUT,
            shell=False)
        print cmd_status
    except Exception as e:
        print e

sys.path.append(os.path.join(silme_path, 'lib'))
try:
    import silme.core
    import silme.io
    import silme.format
    silme.format.Manager.register('dtd', 'properties', 'ini', 'inc')
except ImportError:
    print 'Error importing Silme library'
    sys.exit(1)

def escape(t):
    '''Escape quotes in `t`. Complicated replacements because some strings are already escaped in the repo'''
    return (t.replace("\\'", '_qu0te_')
        .replace('\\', '_sl@sh_')
        .replace("'", "\\'")
        .replace('_qu0te_', "\\'")
        .replace('_sl@sh_', '\\\\')
        )

def get_string(package, local_directory, strings_array):
    for item in package:
        if (type(item[1]) is not silme.core.structure.Blob) and not(isinstance(item[1], silme.core.Package)):
            for entity in item[1]:
                string_id = '{0}/{1}:{2}'.format(local_directory, item[0], entity)
                strings_array[string_id] = item[1][entity].get_value()
        elif (isinstance(item[1], silme.core.Package)):
            if (item[0] != 'en-US') and (item[0] != 'locales'):
                get_string(item[1], local_directory + '/' + item[0], strings_array)
            else:
                get_string(item[1], local_directory, strings_array)

def php_header(target_file):
    target_file.write('<?php\n$tmx = [\n')

def php_add_to_array(entity, translation, target_file):
    translation = escape(translation).encode('utf-8')
    target_file.write("'{0}' => '{1}',\n".format(entity.encode('utf-8'), translation))

def php_close_array(target_file):
    target_file.write('];\n')

if __name__ == '__main__':
    # Read command line input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('locale_repo', help='Path to locale files')
    parser.add_argument('reference_repo', help='Path to reference files')
    parser.add_argument('locale_code', help='Locale language code')
    parser.add_argument('reference_code', help='Reference language code')
    parser.add_argument('repository', help='Repository name')
    args = parser.parse_args()

    exclusionlist = ['.hgtags', '.hg', '.git', '.gitignore']
    dirs_locale = os.listdir(args.locale_repo)
    if args.repository.startswith('gaia') or args.repository == 'l20n_test' :
        dirs_reference = os.listdir(args.reference_repo)
        dirs_reference = [x for x in dirs_reference if x not in exclusionlist]
    else:
        dirs_reference = [
            'browser', 'calendar', 'chat', 'devtools', 'dom', 'editor',
            'extensions', 'mail', 'mobile', 'netwerk', 'other-licenses',
            'security', 'services', 'suite', 'toolkit', 'webapprt'
        ]

    dirs = filter(lambda x:x in dirs_locale, dirs_reference)

    localpath = os.path.join(storage_path, args.locale_code)
    filename_locale = os.path.join(localpath, 'cache_{0}_{1}.php'.format(args.locale_code, args.repository))

    target_locale = open(filename_locale, 'w')
    php_header(target_locale)

    for directory in dirs:
        path_reference = os.path.join(args.reference_repo, directory)
        path_locale = os.path.join(args.locale_repo, directory)

        rcsClient = silme.io.Manager.get('file')
        try:
            l10nPackage_reference = rcsClient.get_package(path_reference, object_type='entitylist')
        except:
            print 'Silme couldn\'t extract data for ', path_reference
            continue

        try:
            l10nPackage_locale = rcsClient.get_package(path_locale, object_type='entitylist')
        except:
            print 'Silme couldn\'t extract data for ', path_locale
            continue

        strings_reference = {}
        strings_locale = {}
        get_string(l10nPackage_reference, directory, strings_reference)
        get_string(l10nPackage_locale, directory, strings_locale)
        for entity in strings_reference:
            php_add_to_array(entity, strings_locale.get(entity, ''), target_locale)

    php_close_array(target_locale)
    target_locale.close()
