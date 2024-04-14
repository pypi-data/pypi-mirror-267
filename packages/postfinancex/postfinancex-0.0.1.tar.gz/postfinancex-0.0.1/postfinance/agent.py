from .models import get_model
from .prompts import get_prompt_template


class Agent(object):

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def translate(
        self,
        model: str,
        params: dict,
        content: str,
    ) -> str:
        print("model: " + model)
        print("content: ", content)
        task = "translate"
        model = get_model(task, model, params, self.api_key)
        prompt = get_prompt_template(task).format(content=content)
        return model.generate_text(prompt, guardrails=False)

    def annotate(
        self,
        model: str,
        params: dict,
        content: str,
    ) -> str:
        print("model: " + model)
        print("content: ", content)
        task = "annotate"
        model = get_model(task, model, params, self.api_key)
        prompt = get_prompt_template(task).format(content=content)
        return model.generate_text(prompt, guardrails=False)

    def chat(
        self,
        model: str,
        params: dict,
        content: str,
        messages: str,
    ) -> str:
        print("model: ", model)
        print("content: ", content)
        print("chat history: ", messages)
        task = "chat"
        model = get_model(task, model, params, self.api_key)
        prompt = get_prompt_template(task).format(
            content=content, messages=messages
        )
        return model.generate_text(prompt, guardrails=False)
