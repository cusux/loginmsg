#!/usr/bin/python3
# -*- coding: utf-8 -*

# Copyright: (c) 2020, Paul Wetering <pwetering@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = r'''
---
module: loginmsg
author:
  - Paul Wetering (@cusux)
short_description: Alter the pre-login and login text of a UNIX target.
version_added: "2.10"
description:
  - The C(loginmsg) module alters the MOTD and/or ISSUE file.
options:
  text:
    description:
      - Text to display before or after user login.
    type: str
    required: true
  when:
    description:
      - Define if the set text is displayed before or after user login.
    type: str
    choices: ["before","after"]
    required: true
  state:
    description:
      - Define wether or not the text is present.
    type: str
    choices: ["present","absent"]
    default: present
  fqdn:
    description:
      - Define wether or not to add an extra line displaying the targets fqdn.
    type: bool
    default: false

notes:
  - This module is for testing purposes only
'''


EXAMPLES = r'''
# Create a new pre-login message
- name: Create the pre-login message with fqdn
  loginmsg:
    text: "Welcome to the wonderfull world of whatever."
    when: before
    state: present
    fqdn: true


# Remove the pre-login message
- name: Create the pre-login message with fqdn
  loginmsg:
    text: "Welcome to the wonderfull world of whatever."
    when: before
    state: absent
'''


RETURN = r'''
'''

import os
import socket

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(text=dict(required=True),
                           when=dict(required=True, choices=['before', 'after']),
                           state=dict(choices=['present', 'absent'], default='present'),
                           fqdn=dict(type=bool, default=False)),
        supports_check_mode=False
    )

    target = ''

    result = dict(
        changed=False
    )

    if module.params['when'] == "before":
        target = "/etc/issue"
    elif module.params['when'] == "after":
        target = "/etc/motd"
    else:
        module.fail_json(msg='Check syntax for <when> parameter', **result)

    if module.params['fqdn']:
        banner = module.params['text'] + "\nServer: " + socket.getfqdn() + "\n"
    else:
        banner = module.params['text'] + "\n"

    if module.params['state'] == "present":
        f = open(target, "w")
        f.write(banner)
        f.close()
        result['changed'] = True
    elif module.params['state'] == "absent":
        os.remove(target)
        result['changed'] = True
    else:
        module.fail_json(msg='Check syntax for <state> parameter', **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
