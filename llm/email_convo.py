import os
from pydantic import ValidationError
from .llm_executer import LLMFunctionExecutor
from .prompts import PROMPTS
from schemas.email_structure import EmailScaffold
from .functions import EMAIL_AGENT_FUNCTIONS

class EmailConvo:
    def __init__(self):
        self.llm_func = LLMFunctionExecutor(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.messages = []
        self.scaffold = None

    def handle_command(self, command):
        client_context = str(command.editorTopContent)
        current_email_sections = str(command.editorLeftContent)
        current_email_structure = str(command.editorRightContent)
        user_messages = str(command.chatMessages)
        sys_msg = PROMPTS.layout_prompt_system_msg.format(client_context, current_email_sections, current_email_structure)
        messages = [{"role": "system", "content": sys_msg}, {"role": "user", "content": user_messages}]
        max_attempts = 10
        for i in range(max_attempts):
            response = self.llm_func.run(system_msg=None, user_content=None, user_messages=messages, functions=EMAIL_AGENT_FUNCTIONS.Email_Task, function_call="auto")
            try:
                ES = EmailScaffold(**response["function_args"])
            except ValidationError as e:
                print(e)
                user_msg = str(e.json()) + "\nPlease try again, you failed the validation step."
                messages.append({"role": "user", "content": user_msg})
                continue
            if i == max_attempts - 1:
                raise Exception("Failed to process the email conversation.")
            else:
                print("Successfully processed the email conversation.")
                break
        return ES
