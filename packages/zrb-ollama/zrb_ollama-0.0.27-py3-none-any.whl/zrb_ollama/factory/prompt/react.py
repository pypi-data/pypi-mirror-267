from langchain.prompts import PromptTemplate
from langchain_core.prompts import BasePromptTemplate

from ...config import SYSTEM_PROMPT
from ...task.any_prompt_task import AnyPromptTask
from ..schema import PromptFactory


def react_prompt_factory(system_prompt: str = SYSTEM_PROMPT) -> PromptFactory:
    def create_prompt(task: AnyPromptTask) -> BasePromptTemplate:
        return PromptTemplate.from_template(
            "\n".join(
                [
                    task.render_str(system_prompt),
                    "",
                    "# TOOLS",
                    "You have access to the following tools:",
                    "{tools}",
                    "",
                    "To use a tool, please use the following format:",
                    "",
                    "```",
                    "",
                    "Thought: Do I need to use a tool? Yes",
                    "Action: the action to take, should be one of [{tool_names}]",
                    "Action Input: the input to the action",
                    "Observation: the result of the action",
                    "```",
                    "",
                    "",
                    "When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:",  # noqa
                    "",
                    "```",
                    "",
                    "Thought: Do I need to use a tool? No",
                    "Final Answer: [your response here]",
                    "```",
                    "",
                    "Begin!",
                    "",
                    "Previous conversation history:",
                    "{chat_history}",
                    "",
                    "New input: {input}",
                    "{agent_scratchpad}",
                ]
            )
        )

    return create_prompt
