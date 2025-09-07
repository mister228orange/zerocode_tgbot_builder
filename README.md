# Zerocode Telegram bot builder
Tool to instant buiding telegram bots by draw.io described workflow.
- Describe flow
- Export it as xml
- Send to app by existing endpoint
- Pay for zerocoding in crypto
- Get your very usefull and unique docker image with binary volumes , ready to deployment in International Scampire

<sup><sub>"Кажется говно конечно, но местным нравится"</sub></sup>

# 2 different WORKFLOWS
I. ##Use /start, then bot begin dialog.     

```mermaid
flowchart TD
    Init["/start"] --"start"--> State1["question + OptionList"]
State1 -- "Option 1" --> State1_1[State 1.1<br> question + OptionList]
State1 -- "Option 2" --> State1_2[Finite State]
State1 -- "Option 3" --> State1_3[State 1.3<br> question + OptionList]

State1_1 -- "Option 1" --> State1_1_1[Finite State]
State1_1 -- "Option 2" --> State1_1_2[Finite State]
State1_1 -- "Option 3" --> State1_1_3[Finite State]

State1_3 -- "Option 1" --> State1_3_1[Finite State]
State1_3 -- "Option 2" --> State1_3_2[Finite State]
```
init state
Bot: ->question                             /     \
      [options]                option[1]   /       \option[2] 
while state not finite:                   /          \ 
  User: option_k                      state1          state2
  Bot: change state -> change options
Bot return finite state
Usage: customizable classification
<sup><sub>"Узнай какой ты смешарик)"</sub></sup>

II 
```mermaid
flowchart TD
    Init["start"] --"start"--> State[Wait msg]
    
    %% Основной цикл
    State -- "Prompt+msg" --> Classifier[LLM/Oracle]
    Classifier[LLM] -- "class_k, arg" --> State
    
    State -- "Class 1 + Response 1" --> State1[State 1<br>Bot: Response 1]
    State -- "Class 2 + Response 2" --> State2[State 2<br>Bot: Response 2]
    
    State1 -- "User message" --> Classifier[LLM]
    Classifier[LLM] -- "class, Arg" --> State1
    State2 -- "User message" --> Classifier2[Any other Data source]
    Classifier2[Any other Data source] -- "class + arg" -->State2
    
    State1 -- "Class 3 + Response 3" --> Terminal1[Terminal State 1]
    State1 -- "Class 4 + Response 4" --> Terminal2[Terminal State 2]
    
    State2 -- "Class 5 + Response 5" --> Terminal3[Terminal State 3]
    State2 -- "Class 6 + Response 6" --> Terminal4[Terminal State 4]


    class Start start;
    class Init init;
    class Classifier,Classifier1,Classifier2 classifier;
    class State1,State2 state;
    class Terminal1,Terminal2,Terminal3,Terminal4 terminal;
```
Usage: Flexiable scenarios to LLM agents<br>
classificator/oracle - its any data resourse which can return different response

<sup><sub>"Автоматизация техподдержки, потому что пользуясь анонимностью связи, и стремлением владельцев отгородить себя от обратной связи эти ублюдки с годами трансформируются в нечто среднее между Theon Greyjoy and Eichmann"</sub></sup>
