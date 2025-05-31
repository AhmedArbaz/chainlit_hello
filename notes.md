# Hello Agent

## Project Creation

```
uv init --package prject-name
cd project-name

uv add chainlit
uv run chainlit run hello

uv run chainlit hello
```

LINK: -> https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/04_hello_agent

chainlit_hello folder may ja kay open ai ko add kanra hay (uv add openai-agents)

.venv folder pay click kar kay copy path karna hay aur phir ctrl+shift+p type python:interpreter / Enter path /paste your copied path there

## Where To get base_url

hamin ya dakhna hota hay kay openai sdk say sath ham kon sa llm use kar sakty hain ollama , gemini
hamin base url panaversity say milay ga ->https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/04_hello_agent (yaha say ham base url milay ga)

## Console output code below shows output in console

import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv, find_dotenv
import os
Load environment variables
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

Step 1: Provider

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

Config: Defined at Run Level

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
    )

Step 3: Agent

agent1 = Agent(
    instructions="You are a helpful assistant that can asnwer questions about Chainlit.",name="Panaversity Support Agent"
)

step 4: Run

result = Runner.run_sync(
    agent1,
    input="What is the capital of France?",
    run_config=run_config,
)

print(result.final_output)

Ab ais ko run karnay hay to

- uv run hello.py

### NOTE Ager ham openai ki hi api key use karin gay to step 1 provider, step 2 model, aur config runConfig sab hata dain gay

## Now the below code is for we send message on chanlit and it reply on chanlit

- the only issue in it is its not storing the chat history which means if i say what's my previous message it didn't reply says sorry

<!-- import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv, find_dotenv
import os
# Load environment variables
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

#Step 1: Provider

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

    # Config: Defined at Run Level

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
    )

# Step 3: Agent

agent1 = Agent(
    instructions="You are a helpful assistant that can asnwer questions about Chainlit.",name="Panaversity Support Agent"
)

#step 4: Run

# result = Runner.run_sync(
#     agent1,
#     input="What is the capital of France?",
#     run_config=run_config,
# )

# print(result.final_output)

# Ab ham chainlit ke saath integrate karte hain (ta kay hum isay web par bhi istemal kar saken) to nichay vala code uncomment karen:

# NOTE Ham nay ya kia phalay nichay valay code ko uncmmit kia phir jo auper hamara result vala code tha usay copy kia change only ya kia kay await Runner.run kia bas await lagay aur run_sync hata diya .run kia , aur input may message.content da diya ta kay jo ham vaha output dain vo yaha dikhay hamin aur run_config ko bhi pass kia. End may await kar kay cl.Message(content=result.final_output).send() kar dia

@cl.on_message  # ya decorator use kia tha on_message jo kay chanilit ka hai aur messages receive karne kay liye hai
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent1,
        input=message.content,  #jo ham message karin gay vo ais may a jay ga input
        run_config=run_config,
    )
    await cl.Message(content=result.final_output).send() -->

- ham nay code ko commit out kar dia hay

# Below is the code with history also our chat bot stores history also now

<!-- import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv, find_dotenv
import os
# Load environment variables
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

#Step 1: Provider

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

    # Config: Defined at Run Level

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
    )

# Step 3: Agent

agent1 = Agent(
    instructions="You are a helpful assistant that can asnwer questions about Chainlit.",name="Panaversity Support Agent"
)

#step 4: Run

# result = Runner.run_sync(
#     agent1,
#     input="What is the capital of France?",
#     run_config=run_config,
# )

# print(result.final_output)


# Ab ham chainlit ke saath integrate karte hain (ta kay hum isay web par bhi istemal kar saken) to nichay vala code uncomment karen:


# Abhi nichay valy code may issue bas ya hay kay hamary pass chat history nahi hain vo store kay liay ham use krin gay

@cl.on_chat_start  # ya decorator use kia tha on_chat_start jo kay chat start hone par trigger hota hai
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Welcome to the Panaversity Support Agent! How can I assist you today?"
    ).send()

# NOTE Ham nay ya kia phalay nichay valay code ko uncmmit kia phir jo auper hamara result vala code tha usay copy kia change only ya kia kay await Runner.run kia bas await lagay aur run_sync hata diya .run kia , aur input may message.content da diya ta kay jo ham vaha output dain vo yaha dikhay hamin aur run_config ko bhi pass kia. End may await kar kay cl.Message(content=result.final_output).send() kar dia

@cl.on_message  # ya decorator use kia tha on_message jo kay chanilit ka hai aur messages receive karne kay liye hai
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history") #abhi hamay history ko set karna hai ta kay hamara chat history store ho sake

    history.append(
        {"role": "user", "content": message.content}
    )
    result = await Runner.run(
        agent1,
        input=history,  #jo ham message karin gay vo ais may a jay ga input puri history ke sath
        run_config=run_config,
    )
    history.append(
        {"role": "assistant", "content": result.final_output}
    )
    cl.user_session.set("history", history)  #ab hamay history ko update karna hai ta kay hamara chat history store ho sake
    await cl.Message(content=result.final_output).send() -->

## Now we want to set it when user give message on chanlit then we respond to that message

- NOTE Ham nay ya kia phalay nichay valay code ko uncmmit kia phir jo auper hamara result vala code tha usay copy kia change only ya kia kay await Runner.run kia bas await lagay aur run_sync hata diya .run kia , aur input may message.content da diya ta kay jo ham vaha output dain vo yaha dikhay hamin aur run_config ko bhi pass kia. End may await kar kay cl.Message(content=result.final_output).send() kar dia

## Now run on Chanilt Command

uv run chainlit run hello.py -w

## Complete Basic configuration

- Now hamaray bot kay pass chat history nahi hay eg. what is my last message (said sorry)

- 