#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
from cgi import escape
import subprocess


def is_iterm_modern():
  osa = subprocess.Popen(['osascript', './detect_version.applescript'],
                         stdout=subprocess.PIPE)
  result = osa.communicate()[0].strip()
  return result == 'true'


def xml_safe(script):
  return escape(script).encode('utf8')


def build(src_dir, out_dir, templates, context):
  for tpl in templates:
    in_path = src_dir + tpl
    out_path = out_dir + tpl
    with open(in_path, 'r') as fin:
      tpl = fin.read()
    data = tpl.format(**context)
    with open(out_path, 'w') as fout:
      fout.write(data)
    print('{0} -> {1}'.format(in_path, out_path))


def build_application():
  src_dir = './application/'
  out_dir = './Open iTerm.app/Contents/'
  if is_iterm_modern():
    script_path = src_dir + 'application.modern.applescript'
  else:
    script_path = src_dir + 'application.applescript'
  script = open(script_path, 'r').read()
  context = {
      'APPLICATION_APPLESCRIPT': xml_safe(script),
      'APPLICATION_NAME': 'OpeniTerm',
      'APPLICATION_IDENTIFIER': 'com.peterldowns.OpeniTerm',
    }
  templates = ['document.wflow', 'Info.plist']
  build(src_dir, out_dir, templates, context)


def build_service():
  src_dir = './service/'
  out_dir = './Open iTerm.workflow/Contents/'
  if is_iterm_modern():
    script_path = src_dir + 'service.modern.applescript'
  else:
    script_path = src_dir + 'service.applescript'
  script = open(script_path, 'r').read()
  context = {
    'FINDER_SERVICE_APPLESCRIPT': xml_safe(script),
    'FINDER_SERVICE_MENU_NAME': 'Open iTerm',
  }
  templates = ['document.wflow', 'Info.plist']
  build(src_dir, out_dir, templates, context)


if __name__ == '__main__':
  build_application()
  build_service()
