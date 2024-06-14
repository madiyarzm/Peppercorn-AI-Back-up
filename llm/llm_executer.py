import json
import os
import traceback
import openai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_random_exponential

class LLMFunctionExecutor:
    def __init__(self, openai_api_key=os.getenv("OPENAI_API_KEY"), model_type="gpt-4-0125-preview", temperature=0.8, max_tokens=None, return_type="dict"):
        self._openai_client = openai.OpenAI(api_key=openai_api_key)
        self._model_type = model_type
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._return_type = return_type

    def ensure_correct_format(self, functions_list):
        for i, func in enumerate(functions_list):
            if "type" not in func or "function" not in func:
                functions_list[i] = {"type": "function", "function": func}
        return functions_list

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def run(self, system_msg, user_content, user_messages=None, functions=None, function_call="auto", model_type=None):
        if model_type is None:
            model_type = self._model_type
        if functions is not None:
            functions = self.ensure_correct_format(functions)
        if len(functions) == 1:
            function_call = functions[0]["function"]["name"]

        function_call = (
            {"type": "function", "function": {"name": function_call}}
            if function_call != "auto"
            else function_call
        )
        messages = []

        if system_msg:
            messages.append({"role": "system", "content": system_msg})
        if user_content:
            messages.append({"role": "user", "content": user_content})
        if user_messages:
            if len(user_messages) != 0:
                messages = user_messages
        try:
            response = self._openai_client.chat.completions.create(
                model=model_type,
                messages=messages,
                tools=functions,
                tool_choice=function_call,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )

            response_message = response.choices[0].message
            function_called = response_message.tool_calls[0].function.name
            try:
                function_args = json.loads(response_message.tool_calls[0].function.arguments)
            except json.decoder.JSONDecodeError as e:
                logger.error(f"{response_message.tool_calls[0].function.arguments}")
                error_message = f"Failed to decode JSON: {e}"
                logger.error(error_message)
                error = traceback.format_exc()
                logger.error(error)

            if self._return_type == "dict":
                return {"function_called": function_called, "function_args": function_args}
            elif self._return_type == "list":
                return [function_called, function_args]
            else:
                return function_called, function_args

        except Exception as e:
            error = traceback.format_exc()
            logger.error(f"Failed on running LLMFunctionExecutor with error - {e,e.args}")
            if 'response_message' in locals():
                logger.info(f"response message - {response_message}")
            logger.info(f"system_msg - {system_msg}")
            logger.info(f"user_content - {user_content}")
            logger.error(error)
            raise e
