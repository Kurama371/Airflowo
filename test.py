import re


CHAT_PATTERN = re.compile(r"^((?:Guild|Party|Co-op|From|To) ?(>)?? |(?:(?:\[:v:\] )?(?:\[[\w\s]+\] )??))??(\[\w{3,}\+{0,2}\] )??(\w{1,16})(?: \[\w{1,6}\])??: (.*)$")


msg = "Guild > [MVP+] Criteox [GM]: boop"

match = CHAT_PATTERN.match(msg)
if match:
    sender = match[4]
    text = match[5]
    print(text)