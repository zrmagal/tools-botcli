import sys
from Bot import Bot

bot = Bot()

argv = sys.argv

if len(argv) > 1:
    if argv[1].startswith('-'):
        match argv[1]:

            case '-n':
                if len(argv) > 2:
                    bot.new(argv[2])
                else:   
                    bot.new()
            case '-o':
                if len(argv) > 2:
                    bot.open(argv[2])
                else:
                    bot.new()
            case '-l':
                for i in bot.list():
                    print(i)
    else:
        bot.chat(argv[1:])
else:
    print('_botcli.py <chat> [token]')

    print('<chat> is the message sent to chat, or one of the following special commands')
    print("-o\n",
          "\t opens existing chat, if any, or create it")
    print("-n [chatname]\n"
          "\t creates a new chat. The optional [chatname] sets the chat name\n",
          "\t if any, the current timestamp is taken as chat name")
    print("-l\n" +
          "\t lists the existing chats")
    
    print("[token] optional OPEN AI token.\n",
          "\tWhenever the 'OPENAI_KEY' env exists it defines the authentication key.\n",
          "\tIf and only if there is no 'OPENAI_KEY' env, the key is define by the [token] argument.")