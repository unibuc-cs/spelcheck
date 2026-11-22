"""llm.py: the only place that talks to the language model.

The model is reached through the OpenAI-compatible chat API, which vLLM (and
most other servers) provide. Every call asks for JSON that must follow a given
JSON schema, so the rest of the code never has to parse free text.
"""

import json
import os

from openai import OpenAI


class LLM:
    """A connection to one model on one server."""

    def __init__(self, base_url: str, model: str | None = None):
        # base_url  e.g. "http://localhost:18200/v1"
        # The key comes from the OPENAI_API_KEY environment variable. Servers
        # started without a key accept any value, hence the "none" default.
        # timeout: the read step of a long document may write some 15,000
        # tokens, which on a busy server can take longer than the client's
        # default of 10 minutes; the client would then send the request again.
        self.client = OpenAI(base_url=base_url, api_key=os.environ.get("OPENAI_API_KEY", "none"),
                             timeout=1800)
        # If no model name is given, use the (first) model the server offers.
        self.model = model or self.client.models.list().data[0].id

    def ask(self, system: str, user: str, schema: dict,
            samples: int = 1, temperature: float = 0.0, max_tokens: int = 4096) -> list[dict]:
        """Send one prompt and return the answers as parsed JSON objects.

        system       the task instructions (the same for every call of a stage)
        user         the data for this particular call
        schema       JSON schema the answer must follow; the server enforces it
                     while the model writes ("structured output")
        samples      how many independent answers to draw for the same prompt
        temperature  0 = the most likely answer; higher = more variety, which
                     is what the ambiguity check needs. (On a server that
                     batches requests, 0 is still not perfectly repeatable.)
        max_tokens   the longest answer allowed. Only the read step of a long
                     document needs more than the default.

        Returns up to `samples` dicts. An answer that is not valid JSON (for
        example cut off by the length limit) is dropped.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "answer", "schema": schema, "strict": True},
            },
            n=samples,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        answers = []
        for choice in response.choices:
            try:
                answers.append(json.loads(choice.message.content))
            except (TypeError, ValueError):
                pass
        return answers
