import mailbox


mbox = mailbox.mbox("emails.mbox")
for i, message in enumerate(mbox):
    print(message.get("Date"))
