import mailbox
import email
import json
import re
import os
import sys

MBOX = sys.argv[1]
ATTACHMENT_BASE_DIR = sys.argv[2]


def jsonify_message(msg):
    # Map in fields from the message
    parsed_msg = dict([(k, v) for (k, v) in msg.items()])
    jsonified_msg = {
        'subject': parsed_msg['Subject'],
        'from': parsed_msg['From'],
        'to': parsed_msg['To'],
    }
    message_id = parsed_msg['X-MS-Exchange-CrossTenant-Network-Message-Id']

    parts = [p for p in msg.walk()]
    for part in parts:
        content_type = part.get_content_type()
        if content_type == 'text/plain':
            jsonified_msg['body'] = part.get_payload()
        else:
            content_disposition = ''
            for header in part._headers:
                if header[0] == 'Content-Disposition':
                    content_disposition = header[1]

            filename_regex = r'filename=\"(.*)\"'
            search_result = re.search(filename_regex, content_disposition)
            if not search_result:
                continue
            attachment_filename = search_result.group(1)
            attachment_filetype = attachment_filename.split('.')[-1]
            attachment_filename = attachment_filename.split('.')[0]
            attachment_as_base64 = part.get_payload().encode('ascii')
            saved_filename = os.path.join(ATTACHMENT_BASE_DIR, "%s-%s.%s" % (attachment_filename, message_id, attachment_filetype))
            outfile = open(saved_filename, "wb")
            outfile.write(attachment_as_base64.decode('base64'))
            outfile.close()
            jsonified_msg['attachment_filepath'] = saved_filename
    return jsonified_msg


mbox = mailbox.UnixMailbox(open(MBOX, 'rb'), email.message_from_file)

messages = []

while 1:
    msg = mbox.next()
    if msg is None:
        break
    msg = jsonify_message(msg)
    messages.append(msg)

json_path = os.path.join(ATTACHMENT_BASE_DIR, "parsed_emails.json")
json_file = open(json_path, 'w')
json.dump(messages, json_file, indent=4, sort_keys=True, ensure_ascii=False)
json_file.close()
