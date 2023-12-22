import os

from openai import OpenAI

import openai


api_key = os.environ.get("OPENAI_TOKEN")
client = OpenAI(api_key=api_key)


async def create_thread():
    thread = client.beta.threads.create()
    return thread.id


async def generate_text(prompt, thread_id) -> dict:
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id="asst_lYyjxPbAFy8dYVY0HDiUCEbk"
    )

    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        )

        if keep_retrieving_run.status == "completed":
            break

    all_messages = client.beta.threads.messages.list(thread_id=thread_id)

    return all_messages.data[0].content[0].text.value
