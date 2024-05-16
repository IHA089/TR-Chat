import os

def L_BOX(message, title):
    terminal_width = os.get_terminal_size().columns
    body_width = terminal_width-20
    box_width = max(len(message), len(title)) + 4

    left_box_line_color="\033[1;31m"
    left_box_text_color="\033[1;35m"
    left_box_sender_color="\033[1;37m"

    if len(message) > body_width:
        alfa = L_BODY(body_width, body_width, message, left_box_line_color, left_box_text_color)
        boxed_msg = "\r" + left_box_line_color + "┌" + "─" * (body_width - 2) + "┐\n"+alfa+"\r" + left_box_line_color + "└" +  "─" * (body_width - (4+len(title)))+ left_box_sender_color + title + left_box_line_color + "──┘"
    else:
        boxed_msg = "\r" + left_box_line_color + "┌" + "─" * (box_width - 2) +"┐\n\r" + left_box_line_color + "│ " + left_box_text_color + message + " " * (box_width - len(message) - 3) + left_box_line_color + "│\n\r" + left_box_line_color + "└" + "─" * (box_width - (4+len(title)))+ left_box_sender_color + title + left_box_line_color + "──┘"
    return boxed_msg

def R_BOX(message, title):
    terminal_width = os.get_terminal_size().columns
    body_width = terminal_width-20
    box_width = max(len(message), len(title)) + 4

    right_box_line_color="\033[92;1m"
    right_box_text_color="\033[1;34m"
    right_box_sender_color="\033[1;37m"

    if len(message) > body_width:
        start_position = terminal_width-body_width-1
        alfa = R_BODY(body_width, body_width, start_position, message, right_box_line_color, right_box_text_color)
        boxed_msg = "\r" + " " * start_position + right_box_line_color + "┌" + "─" * (body_width - 2) + "┐\n"+alfa+"\r" + " " * start_position + right_box_line_color + "└" + "─" * (body_width - (4+len(title)))+right_box_sender_color + title + right_box_line_color + "──┘"
    else:
        start_position = terminal_width-box_width-1
        boxed_msg = "\r" + " " * start_position + right_box_line_color + "┌" + "─" * (box_width - 2) + "┐\n\r" + " " * start_position + right_box_line_color + "│ " + right_box_text_color + message + " " * (box_width - len(message) - 3) + right_box_line_color + "│\n\r" + " " * start_position + right_box_line_color + "└" + "─" * (box_width - (4+len(title)))+ right_box_sender_color + title + right_box_line_color + "──┘"
    return boxed_msg

def L_BODY(box_width, body_width, message, line_color, msg_color):
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
            jm = jm + "\r" + line_color + "│ " + msg_color + pre + " " * (box_width - len(pre) - 3) + line_color + "│\n"
            pre=""
            ml=""
        else:
            pre = ml
            ml = ml+word+" "
    ml = ml[:-1]
    jm = jm+"\r" + line_color + "│ " + msg_color + ml + " " * (box_width - len(ml) - 3) + line_color + "│\n"
    return jm

def R_BODY(box_width, body_width, start_position, message, line_color, msg_color):
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
            jm = jm + "\r" + " " * start_position + line_color + "│ " + msg_color + pre + " " * (box_width - len(pre) - 3) + line_color + "│\n"
            pre=""
            ml=""
        else:
            pre = ml
            ml = ml+word+" "
    ml = ml[:-1]
    jm = jm+"\r" + " " * start_position + line_color + "│ " + msg_color + ml + " " * (box_width - len(ml) - 3) + line_color + "│\n"
    return jm
