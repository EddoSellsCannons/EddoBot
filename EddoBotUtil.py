import random
import time
import struct
import math

def handler(message): #Ensure the command is valid before processing (Checks command, word count, valid types, etc.)
    message_split = message.content.split()
    command = message_split[0]
    if command[0] != "$":
        return None
    
    if command == "$rng":
        if len(message_split) != 2:
            return "Do $rng <range> to generate a random number from 0 to the specified range."
        try:
            rng_range = message_split[1]
            if int(rng_range) > 0:
                return str(rng(rng_range))
            else:
                return "Please enter a range higher than 0"
        except Exception:
            return "Something went wrong. Error handling not implemented yet. sry."

    elif command == "$encrypt":
        if len(message_split) < 2:
            return "Do $encrypt <Word to encrypt> to receive an encrypted version of the word."
        return str(encrypt(message_split[1]))
    elif command == "$decrypt":
        if len(message_split) < 2:
            return "Do $decrypt <Word to encrypt> to receive a decrypted version of the word."
        return str(decrypt(message_split[1]))

    else:
        return "Not a valid command. Do $help for all commands"

def bot_respond(message):
    msg = message.content.lower()

    if "i'm" in msg or "im" in msg:
        dad_bot_index = -1
        if "i'm" in msg:
            dad_bot_index = msg.find("i'm") + 4
        elif "im" in msg:
            dad_bot_index = msg.find("im") + 3
        dad_bot_msg = "Hi, " + msg[dad_bot_index:len(msg)] + ", I'm EddoBot!"
        return dad_bot_msg

def rng(rng_range):
    t = int(time.time() * 1000) % int(rng_range)
    return t

def encrypt(to_encrypt):
    str_pi = str(math.pi)[2:]
    new_encrypt = ""
    i = 0
    for c in to_encrypt:
        char = ord(c)
        c = chr(char + int(str_pi[i % len(str_pi)]))
        i += 1
        new_encrypt += c
    new_encrypt = reverse_str(new_encrypt)
    return new_encrypt

def decrypt(to_decrypt):
    str_pi = str(math.pi)[2:]
    new_decrypt = ""
    to_decrypt = reverse_str(to_decrypt)
    i = 0
    for c in to_decrypt:
        char = ord(c)
        c = chr(char - int(str_pi[i % len(str_pi)]))
        i += 1
        new_decrypt += c
    return new_decrypt

def reverse_str(to_reverse):
    reversed_str = ""
    i = len(to_reverse) - 1
    while i >= 0:
        reversed_str += to_reverse[i]
        i -= 1
    return reversed_str