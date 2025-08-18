"""
Simple Python 3 script to convert eml Email files to mbox files.
Convert script requires only The Python Standard Libraries.
This script is useful to convert eml files exported from
E-Mail Accounts to mbox files. Mbox files can be imported
in common email clients such as Outlook, Thunderbird, or
Gnome Evolution.
Placing eml files to be converted to mbox files:
 * place all your eml files into the "in" directory:
   e.g. in/username_at_email_domain/inbox/123456.eml
Output (mbox-out):
 * mbox file for each of the discovered subdirectories with eml files.
"""


import re
import os
import mailbox
from email import policy
from email.parser import BytesParser


eml_regex = re.compile('.*\\.eml')

output_mbox_file="emails.mbox"
if os.path.exists(output_mbox_file):
    print(f"WARN: Deleting existing mbox: {output_mbox_file}")
    os.remove(output_mbox_file)

destination = mailbox.mbox(output_mbox_file)
destination.lock()

for root, dirs, files in os.walk("emails/yann@johncloud.fr", topdown=True):
    eml_files = list(filter(eml_regex.match, files))
    for eml_file in eml_files:
        eml_file_path = os.path.join(root, eml_file)
        with open(eml_file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
            destination.add(mailbox.MHMessage(msg))

destination.flush()
destination.unlock()
