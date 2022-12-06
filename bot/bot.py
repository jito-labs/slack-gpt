import sys
import logging

import openai
from slack_bolt import App
import os

print(os.environ["SLACK_BOT_TOKEN"])
print(os.environ["SLACK_SIGNING_SECRET"])
sys.stdout.flush()

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])


@app.event("message")
def handle_message(body, say, logger):
    try:
        event = body["event"]
        print(body)
        sys.stdout.flush()

        if event["type"] != "bot_message":
            user = event["user"]
            channel = event["channel"]
            text = event["text"]
            logger.info(f"Received message from user {user}: {text}")

            completion = openai.Completion.create(engine="text-davinci-003",
                                                  prompt=text,
                                                  max_tokens=2048,
                                                  temperature=0.8,
                                                  user=event["user"])
            print(f"completion: {completion}")
            print("\n")
            sys.stdout.flush()

            # Post the response to the Slack channel
            say(channel=channel, text=completion.choices[0].text)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    app.start(port=3000)
