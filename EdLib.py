import random
#Task, rename each function to a more descriptive name based on what it is doing. 
#Use each function in a new command in BOT.py

def getUwU(): #To test BOT code.
    return """
⡆⣐⢕⢕⢕⢕⢕⢕⢕⢕⠅⢗⢕⢕⢕⢕⢕⢕⢕⠕⠕⢕⢕⢕⢕⢕⢕⢕⢕⢕
⢐⢕⢕⢕⢕⢕⣕⢕⢕⠕⠁⢕⢕⢕⢕⢕⢕⢕⢕⠅⡄⢕⢕⢕⢕⢕⢕⢕⢕⢕
⢕⢕⢕⢕⢕⠅⢗⢕⠕⣠⠄⣗⢕⢕⠕⢕⢕⢕⠕⢠⣿⠐⢕⢕⢕⠑⢕⢕⠵⢕ 
⢕⢕⢕⢕⠁⢜⠕⢁⣴⣿⡇⢓⢕⢵⢐⢕⢕⠕⢁⣾⢿⣧⠑⢕⢕⠄⢑⢕⠅⢕ 
⢕⢕⠵⢁⠔⢁⣤⣤⣶⣶⣶⡐⣕⢽⠐⢕⠕⣡⣾⣶⣶⣶⣤⡁⢓⢕⠄⢑⢅⢑ 
⠍⣧⠄⣶⣾⣿⣿⣿⣿⣿⣿⣷⣔⢕⢄⢡⣾⣿⣿⣿⣿⣿⣿⣿⣦⡑⢕⢤⠱⢐ 
⢠⢕⠅⣾⣿⠋⢿⣿⣿⣿⠉⣿⣿⣷⣦⣶⣽⣿⣿⠈⣿⣿⣿⣿⠏⢹⣷⣷⡅⢐ 
⣔⢕⢥⢻⣿⡀⠈⠛⠛⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠛⠛⠁⠄⣼⣿⣿⡇⢔ 
⢕⢕⢽⢸⢟⢟⢖⢖⢤⣶⡟⢻⣿⡿⠻⣿⣿⡟⢀⣿⣦⢤⢤⢔⢞⢿⢿⣿⠁⢕ 
⢕⢕⠅⣐⢕⢕⢕⢕⢕⣿⣿⡄⠛⢀⣦⠈⠛⢁⣼⣿⢗⢕⢕⢕⢕⢕⢕⡏⣘⢕ 
⢕⢕⠅⢓⣕⣕⣕⣕⣵⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣕⢕⢕⢕⢕⡵⢀⢕⢕ 
⢑⢕⠃⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⢕⢕⢕ 
⣆⢕⠄⢱⣄⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢁⢕⢕⠕⢁ 
⣿⣦⡀⣿⣿⣷⣶⣬⣍⣛⣛⣛⡛⠿⠿⠿⠛⠛⢛⣛⣉⣭⣤⣂⢜⠕⢑⣡⣴⣿
"""

def func2(index):
    ls = ["<:dam:826071637128511529>",
          "<:sealofapproval:865125910134784032>",
          "<:pongers:865218289943445504>",
          "<:shitOnMyDik:890500026244153454>",
          "<:Glush:1079073691549302894>",
          "<:Light_Blue_Shy_Guy10:1079262284062408784>",
          "<:holyshitthatsucksman:1099674137133318177>",
          "<:niceCOCK:1103250536804929588>",
          "<:sussy:1088828832997458010>"
          ]
    if index >= len(ls):
        return ls[random.randint(0, len(ls) - 1)]
    else:
        return ls[index]

def func3(input_to_function): #Rename both function and variable
    if str(input_to_function).isalpha(): #Google this function to find out what it does
        return True
    else:
        return False

def func4(message_content_split_list):
    new_msg_list = []
    for msg in message_content_split_list:
        index = 0
        new_string = ""
        for m in msg:
            if index % 2 == 0:
                new_string += m.lower()
            else:
                new_string += m.upper()
            index += 1
        new_msg_list.append(new_string)

    return new_msg_list





def main(): #Run this program to see the test outputs. Do this only if stuck. (> py EdLib.py)
    #print(getUwU())
    #print(func2(9))
    #print(func3(100))
    #print(func4(["test1", "the other one"]))
    print("Uncomment function to test.")

if __name__ == "__main__": #Ignore this
    main()