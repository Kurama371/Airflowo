import re

PATTERNS = {
    "skyblock_stats": re.compile(r"^(?=.*✎ Mana)(?=.*❤)(?=.*/).*"),
    "lobby_join": re.compile(r"^\[MVP\+.* the lobby!( <<<)?$"),
    "guild_message": re.compile(r"^Guild > .*\:.*"),
    "in_limbo": re.compile(r"^You were spawned in Limbo\.")
}

CHAT_PATTERN = re.compile(r"^((?:Guild|Party|Co-op|From|To) ?(>)?? |(?:(?:\[:v:\] )?(?:\[[\w\s]+\] )??))??(\[\w{3,}\+{0,2}\] )??(\w{1,16})(?: \[\w{1,6}\])??: (.*)$")


def get_message_type(msg):
    for type, pattern in PATTERNS.items():
        if pattern.search(msg):
            return type
    return None
    

def handle_message(msg, client):
    msg_type = get_message_type(msg)
    
    if msg_type == "skyblock_stats":
        return
    elif msg_type == "lobby_join":
        client.mc_instance.chat("/limbo")
        return
    elif msg_type == "in_limbo":
        print("in limbo!")
        client.broker_instance.send({
            "type": "info",
            "msg": "In Limbo"
        })
        client.state = "IDLE"
    elif msg_type == "guild_message":
        match = CHAT_PATTERN.match(msg)
        if match:
            sender = match[4]
            text = match[5]
            
            client.broker_instance.send({
                "type": "guild_msg",
                "msg": f"{text}",
                "sender": f"{sender}"
            })

        return
    elif msg_type == None:
        client.broker_instance.send({
            "type": "other_msg",
            "msg": f"{msg}"
        })
    
    


    



