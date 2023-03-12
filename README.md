# botGPT-cli
Python script that provides a command line interface to access chat gpt 

_botcli.py \<chat> [token]

\<chat> is the message sent to chat, or one of the following special commands

-o

          opens existing chat, if any, or create it

-n [chatname]

         creates a new chat. The optional [chatname] sets the chat name
         if any, the current timestamp is taken as chat name

-l

         lists the existing chats

[token] optional OPEN AI token.

        Whenever the 'OPENAI_KEY' env exists it defines the authentication key.
        If and only if there is no 'OPENAI_KEY' env, the key is define by the [token] argument.
