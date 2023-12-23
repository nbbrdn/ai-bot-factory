import logging
import os
import time

from openai import OpenAI

api_key = os.environ.get("OPENAI_TOKEN")
assistant_id = os.environ.get("ASSISTANT_ID")

client = OpenAI(api_key=api_key)


async def create_thread():
    thread = client.beta.threads.create()
    return thread.id


async def generate_text(prompt, thread_id) -> dict:
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        )
        logging.info(f"openai api request status): {run.status}")

        if keep_retrieving_run.status == "completed":
            break
        time.sleep(3)

    all_messages = client.beta.threads.messages.list(thread_id=thread_id)

    return all_messages.data[0].content[0].text.value
