# Zerocode Telegram bot builder
Tool to instant buiding telegram bots by draw.io described workflow.
- Describe flow
- Export it as xml
- Send to app by existing endpoint
- Pay for zerocoding in crypto
- Get your very usefull and unique docker image with binary volumes , ready to deployment in International Scampire

<sup><sub>"Кажется говно конечно, но местным нравится"</sub></sup>

# 2 different WORKFLOWS
I. Use /start, then bot begin dialog.     init state
Bot: ->question                             /     \
      [options]                option[1]   /       \option[2] 
while state not finite:                   /          \ 
  User: option_k                      state1          state2
  Bot: change state -> change options
Bot return finite state
Usage: customizable classification
<sup><sub>"Узнай какой ты смешарик)"</sub></sup>

                                            init state
II.     prompt+                             user msg --------> classificator/oracle
User: ->messsage ----> classificator         /     \<-------response[class]
      class_num     <-----|    response[1] /        \response[2] 
while state not finite:                   /          \ 
  Bot: response[class_num];          state1          state2
       change state
  User: msg
Bot return to init state

Usage: Flexiable scenarios to LLM agents
classificator/oracle - its any data resourse which can return different response

<sup><sub>"Автоматизация техподдержки, потому что пользуясь анонимностью связи, и стремлением владельцев отгородить себя от обратной связи эти ублюдки с годами трансформируются в нечто среднее между Theon Greyjoy and Eichmann"</sub></sup>
