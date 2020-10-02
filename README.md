# Steps for parsing PST files

1. Install the `readpst` command line utility
2. Run `readpst <pstfile>` from the command line to parse a pst file into mbox files
3. Run `python mbox2json.py <mbox_file> <directory_for_output>` to convert to json

You'll probably want to use the Inbox.mbox file in the above command (it's one of the outputs from the readpst command)

The `directory_for_output` will contain all attachements from the PST file and also a json file containing the emails in the following form:
```json
[
    {
        "attachment_filepath": "<filepath>", 
        "body": "Lorem Ipsum ...", 
        "from": "example@test.com", 
        "subject": "Email Subject", 
        "to": "example2@test.com"
    },
    ...
]
```
