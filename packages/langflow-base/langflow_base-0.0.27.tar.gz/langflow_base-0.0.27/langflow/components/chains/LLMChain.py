from typing import Optional

from langchain.chains import LLMChain

from langflow.field_typing import BaseLanguageModel, BaseMemory, BasePromptTemplate, Text
from langflow.interface.custom.custom_component import CustomComponent


class LLMChainComponent(CustomComponent):
    display_name = "LLMChain"
    description = "Chain to run queries against LLMs"

    def build_config(self):
        return {
            "prompt": {"display_name": "Prompt"},
            "llm": {"display_name": "LLM"},
            "memory": {"display_name": "Memory"},
        }

    def build(
        self,
        prompt: BasePromptTemplate,
        llm: BaseLanguageModel,
        memory: Optional[BaseMemory] = None,
    ) -> Text:
        runnable = LLMChain(prompt=prompt, llm=llm, memory=memory)
        result_dict = runnable.invoke({})
        output_key = runnable.output_key
        result = result_dict[output_key]
        self.status = result
        return result
