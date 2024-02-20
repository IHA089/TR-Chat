import os

def L_BOX(message, title):
    terminal_width = os.get_terminal_size().columns
    body_width = terminal_width-20
    box_width = max(len(message), len(title)) + 4
    if len(message) > body_width:
        alfa = L_BODY(body_width, body_width, message)
        boxed_msg = "\r" + "┌" + "─" * (body_width - 2) + "┐\n"+alfa+"\r" + "└" + "─" * (body_width - (4+len(title)))+title + "──┘"
    else:
        boxed_msg = "\r" + "┌" + "─" * (box_width - 2) + "┐\n\r" + "│ " + message + " " * (box_width - len(message) - 3) + "│\n\r" + "└" + "─" * (box_width - (4+len(title)))+title + "──┘"
    return boxed_msg

def R_BOX(message, title):
    terminal_width = os.get_terminal_size().columns
    body_width = terminal_width-20
    box_width = max(len(message), len(title)) + 4

    if len(message) > body_width:
        start_position = terminal_width-body_width-1
        alfa = R_BODY(body_width, body_width, start_position, message)
        boxed_msg = "\r" + " " * start_position + "┌" + "─" * (body_width - 2) + "┐\n"+alfa+"\r" + " " * start_position + "└" + "─" * (body_width - (4+len(title)))+title + "──┘"
    else:
        start_position = terminal_width-box_width-1
        boxed_msg = "\r" + " " * start_position + "┌" + "─" * (box_width - 2) + "┐\n\r" + " " * start_position + "│ " + message + " " * (box_width - len(message) - 3) + "│\n\r" + " " * start_position + "└" + "─" * (box_width - (4+len(title)))+title + "──┘"
    return boxed_msg

def L_BODY(box_width, body_width, message):
    ll = message.split(" ")
    jm=""
    ml = ""
    pre = ""
    for word in ll:
        if "\n" in word:
            word = word.replace("\n", "\\n")
        if "\t" in word:
            word = word.replace("\t", "\\t")
        if "\r" in word:
            word = word.replace("\r", "\\r")
        if len(ml) >= body_width-2:
            jm = jm + "\r" + "│ " + pre + " " * (box_width - len(pre) - 3) + "│\n"
            pre=""
            ml=""
        else:
            pre = ml
            ml = ml+word+" "
    ml = ml[:-1]
    jm = jm+"\r" + "│ " + ml + " " * (box_width - len(ml) - 3) + "│\n"
    return jm

def R_BODY(box_width, body_width, start_position, message):
    ll = message.split(" ")
    jm=""
    ml = ""
    pre = ""
    for word in ll:
        if "\n" in word:
            word = word.replace("\n","\\n")
        if "\t" in word:
            word = word.replace("\t", "\\t")
        if "\r" in word:
            word = word.replace("\r", "\\r")

        if len(ml) >= body_width-2:
            jm = jm + "\r" + " " * start_position + "│ " + pre + " " * (box_width - len(pre) - 3) + "│\n"
            pre=""
            ml=""
        else:
            pre = ml
            ml = ml+word+" "
    ml = ml[:-1]
    jm = jm+"\r" + " " * start_position + "│ " + ml + " " * (box_width - len(ml) - 3) + "│\n"
    return jm