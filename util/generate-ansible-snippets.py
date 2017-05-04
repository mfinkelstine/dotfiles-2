#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import os.path
import fnmatch
import logging
import ansible.modules
from ansible.utils.module_docs import get_docstring

# Setup Logging
logger = logging.getLogger('snippet_generator')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# TODO:
# * move the cursor to the "name" field, instead of the first argument
# * free form modules (like command), should be formatted properly


def get_documents():
    for root, dirnames, filenames in os.walk(os.path.dirname(ansible.modules.__file__)):  # noqa: E501
        for filename in fnmatch.filter(filenames, '*.py'):
            if filename == '__init__.py':
                continue
            if filename.endswith('.pyc'):
                continue
            if filename.endswith('.ps1'):
                continue
            documentation = get_docstring(os.path.join(root, filename))[0]
            if documentation is None:
                continue
            yield documentation


def get_play_snippet():
    play_snippet = []
    play_snippet.insert(0, 'snippet play "Execute an ansible play"')
    play_snippet.append('- hosts: ${1:host_group}')
    play_snippet.append('\tremote_user: ${2:remote_user}')
    play_snippet.append('\ttasks:')
    play_snippet.append('\t$0')
    play_snippet.append('endsnippet\n')
    return "\n".join(play_snippet)


def to_snippet(document):
    snippet = []
    # Insert the snippet header, name label, and module name
    snippet.insert(0, '\t%s:' % (document['module']))
    snippet.insert(0, '- %s:' % ('name'))
    snippet.insert(0, 'snippet %s "%s"' % (document['module'], document['short_description']))  # noqa: E501

    if 'options' in document:
        if 'free_form' in document['options']:
            logger.info('Found free-form module: ' + document['module'])

        options = sorted(document['options'].items(), key=lambda x: x[1].get("required", False), reverse=True)  # noqa: E501
        for index, (name, option) in enumerate(options, 1):
            if 'choices' in option:
                default = option.get('default')
                if isinstance(default, list):
                    prefix = lambda x: '#' if x in default else ''  # noqa: E731
                    suffix = lambda x: "'%s'" % x if isinstance(x, str) else x  # noqa: E731
                    value = '[' + ', '.join("%s%s" % (prefix(choice), suffix(choice)) for choice in option['choices'])  # noqa: E501
                else:
                    prefix = lambda x: '#' if x == default else ''  # noqa: E731
                    value = '|'.join('%s%s' % (prefix(choice), choice) for choice in option['choices'])  # noqa: E501
            elif option.get('default') is not None and option['default'] != 'None':  # noqa: E501
                value = option['default']
                if isinstance(value, bool):
                    value = 'yes' if value else 'no'
            else:
                value = "# " + option.get('description', [''])[0]
            if name == 'free_form':  # special for command/shell
                snippet.append('\t\t${%d:%s=%s}' % (index, name, value))
            else:
                snippet.append('\t\t%s: ${%d:%s}' % (name, index, value))

    snippet.append('$0')
    snippet.append('endsnippet')
    return "\n".join(snippet)


if __name__ == "__main__":
    with open("ansible.snippets", "w") as snippetfile:
        snippetfile.writelines(["priority 50\n", "\n", "# THIS FILE IS AUTOMATICALLY GENERATED, PLEASE DON'T MODIFY BY HAND\n", "\n"])  # noqa: E501
        snippetfile.write(get_play_snippet().encode('utf-8'))
        snippetfile.write("\n")
        for document in get_documents():
            logger.info('Generating snippet for module: ' + document['module'])
            if 'deprecated' in document:
                continue
            snippetfile.write(to_snippet(document).encode('utf-8'))
            snippetfile.write("\n\n")
