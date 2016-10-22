#!/usr/bin/python

import argparse
import json
import os
import subprocess
import sys
from ConfigParser import SafeConfigParser

# Get absolute path of ../config from the current script location (not the
# current folder)
config_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, 'config'))

# Read Transvision's configuration file from ../config/config.ini
# If not available use default a /storage folder to store data
config_file = os.path.join(config_folder, 'config.ini')
if not os.path.isfile(config_file):
    print 'Configuration file /app/config/config.ini is missing. Default folders will be used.'
    root_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))
    library_path = os.path.join(root_folder, 'libraries')
else:
    config_parser = SafeConfigParser()
    config_parser.read(config_file)
    library_path = config_parser.get('config', 'libraries')
    storage_path = os.path.join(config_parser.get('config', 'root'), 'TMX')

# Import compare-locales library (http://hg.mozilla.org/l10n/compare-locales/)
compare_locales_path = os.path.join(library_path, 'compare-locales')

if not os.path.isdir(compare_locales_path):
    try:
        print 'Cloning compare-locales...'
        cmd_status = subprocess.check_output(
            ['hg', 'clone', 'https://hg.mozilla.org/l10n/compare-locales',
                compare_locales_path, '-u', 'RELEASE_1_1'],
            stderr=subprocess.STDOUT,
            shell=False)
        print cmd_status
    except Exception as e:
        print e
sys.path.insert(0, os.path.join(compare_locales_path))

try:
    from compare_locales import parser
except ImportError:
    print 'Error importing compare-locales library'
    sys.exit(1)


class StringExtraction():


    def __init__(self, storage_path, locale, reference_locale, repository_name):
        ''' Initialize object '''

        self.supported_formats = ['.dtd', '.properties', '.ini', '.inc']
        self.storage_path = storage_path
        self.file_list = []
        self.translations = {}
        self.repository_name = repository_name
        self.locale = locale
        self.reference_locale = reference_locale

        # Define the locale storage filename
        self.storage_file = os.path.join(
            storage_path, locale,
            'cache_{0}_{1}'.format(locale, repository_name))

        self.reference_storage_file = os.path.join(
            storage_path, reference_locale,
            'cache_{0}_{1}'.format(reference_locale, repository_name))


    def setRepositoryPath(self, path):
        ''' Set path to repository '''

        self.repository_path = path


    def extractFileList(self):
        ''' Extract the list of supported files'''

        for root, dirs, files in os.walk(self.repository_path, followlinks=True):
            for file in files:
                for supported_format in self.supported_formats:
                    if file.endswith(supported_format):
                        self.file_list.append(os.path.join(root, file))
        self.file_list.sort()


    def extractStrings(self):
        ''' Extract strings from all files '''
        self.extractFileList()

        for file_name in self.file_list:
            file_extension = os.path.splitext(file_name)[1]

            file_parser = parser.getParser(file_extension)
            file_parser.readFile(file_name)
            entities, map = file_parser.parse()

            for entity in entities:
                relative_path = file_name[len(self.repository_path) + 1:]
                # Hack to work around Transvision symlink mess
                relative_path = relative_path.replace('locales/en-US/en-US/', '')
                string_id = '{0}:{1}'.format(relative_path, entity)
                self.translations[string_id] = entity.val


        # Remove extra strings from locale
        if self.reference_locale != self.locale:
            # Read the JSON cache for reference locale if available
            file_name = self.reference_storage_file + '.json'
            if os.path.isfile(file_name):
                with open(self.reference_storage_file + '.json') as f:
                    reference_strings = json.load(f)
                f.close()

                for string_id in self.translations.keys():
                    if string_id not in reference_strings:
                        del(self.translations[string_id])


    def storeTranslations(self):
        ''' Store translations on file (JSON, PHP) '''
        # Store translations in JSON format
        f = open(self.storage_file + '.json', 'w')
        f.write(json.dumps(self.translations, sort_keys=True))
        f.close()

        # Store translations in PHP format (array)
        string_ids = self.translations.keys()
        string_ids.sort()

        f = open(self.storage_file + '.php', 'w')
        f.write('<?php\n$tmx = [\n')
        for string_id in string_ids:
            translation = self.escape(self.translations[string_id].encode('utf-8'))
            f.write("'{0}' => '{1}',\n".format(string_id, translation))
        f.write('];\n')
        f.close()


    def escape(self, translation):
        '''
            Escape quotes and backslahes in translation. There are two issues:
            * Internal Python escaping: the string "this is a \", has an internal
              representation as "this is a \\".
              Also, "\\ test" is equivalent to r"\ test" (raw string).
            * We need to print these strings into a file, with the format of a
              PHP array delimited by single quotes ('id' => 'translation'). Hence
              we need to escape single quotes, but also escape backslashes.
              "this is a 'test'" => "this is a \'test\'"
              "this is a \'test\'" => "this is a \\\'test\\\'"
        '''

        # Escape slashes
        escaped_translation = translation.replace('\\', '\\\\')
        # Escape single quotes
        escaped_translation = escaped_translation.replace('\'', '\\\'')

        return escaped_translation


def main():
    # Read command line input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('repo_path', help='Path to locale files')
    parser.add_argument('locale_code', help='Locale language code')
    parser.add_argument('reference_code', help='Reference language code')
    parser.add_argument('repository_name', help='Repository name')
    args = parser.parse_args()

    extracted_strings = StringExtraction(storage_path, args.locale_code, args.reference_code, args.repository_name)
    extracted_strings.setRepositoryPath(args.repo_path.rstrip('/'))
    extracted_strings.extractStrings()
    extracted_strings.storeTranslations()


if __name__ == '__main__':
    main()
