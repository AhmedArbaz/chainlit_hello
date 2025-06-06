import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv, find_dotenv
import os

from openai.types.responses import ResponseTextDeltaEvent
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
    model="gemini-2.0-flash",  #streaming karty time ais ko ham nay 2.0-flash say 1.5-pro pay kar dia hay
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


    msg = cl.Message(content="") # ab ham nay message may content empty kar dia ta kay streaming hamin sahi say nazar ay
    await msg.send()


    history.append(
        {"role": "user", "content": message.content}
    )
    # result = await Runner.run(
    #     agent1,
    #     input=history,  #jo ham message karin gay vo ais may a jay ga input puri history ke sath
    #     run_config=run_config,
    # )

    result = Runner.run_streamed(
         agent1,
         input=history,  #jo ham message karin gay vo ais may a jay ga input puri history ke sath
         run_config=run_config,
    )
    # ya auper vala result commit kar kay ham nay ais ko run_streamed kar dia ta kay streaming may kam hon

    async for event in result.stream_events():
        if event.type == 'raw_respnse_event' and isinstance(event.data, ResponseTextDeltaEvent):
            # print(event.data.delta, end="", flush=True)
           await msg.stream_token(event.data.delta)
            # await msg.send()

    history.append(
        {"role": "assistant", "content": result.final_output}
    )
    cl.user_session.set("history", history)  #ab hamay history ko update karna hai ta kay hamara chat history store ho sake
    await cl.Message(content=result.final_output).send()