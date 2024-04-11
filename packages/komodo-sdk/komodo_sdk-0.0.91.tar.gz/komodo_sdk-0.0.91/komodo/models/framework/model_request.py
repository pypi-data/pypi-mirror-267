from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_runtime import KomodoRuntime
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.chat_message import ChatMessage


class ModelRequest:
    def __init__(self, prompt: str, runtime: KomodoRuntime, **kwargs):
        self.prompt = prompt
        self.runtime = runtime
        self.kwargs = kwargs

    def __str__(self):
        return str(self.runtime)

    def prepare_messages(self):
        agent = self.runtime.agent
        messages = self.prepare_agent_messages(agent)

        if collection := self.runtime.selected_collection:
            if agent.autoload_collection:
                messages += self.prepare_file_messages(agent, collection)

        workflow_context = self.kwargs.get('workflow_context', KomodoContext())
        workflow_messages = ChatMessage.convert_from_context(workflow_context)
        messages += [m.add_tag('Workflow') for m in workflow_messages]

        history = self.kwargs.get('history', [])
        messages += history

        workflow_inputs = self.kwargs.get('workflow_inputs', [])
        messages += [m.add_tag('Workflow Agent Outputs') for m in workflow_inputs]

        return messages

    def prepare_file_messages(self, agent, collection):
        max_files = agent.max_files_per_request
        max_tokens_per_file = agent.max_tokens_per_file
        max_total_tokens = agent.max_total_tokens
        collection_context = collection.get_collection_context(max_files, max_tokens_per_file, max_total_tokens)
        collection_messages = ChatMessage.convert_from_context(collection_context)
        return [m.add_tag('Files') for m in collection_messages]

    def prepare_agent_messages(self, agent):
        instructions = ChatMessage.build("Instructions", agent.instructions)
        agent_messages = [instructions]

        if agent.allow_hallucinations:
            agent_messages.append(
                ChatMessage.build("Creativity", "You may make up fake data or hallucinate information."))
        else:
            agent_messages.append(
                ChatMessage.build("Creativity", "Do NOT make up fake data or hallucinate information."))

        if agent.tools:
            agent_messages.append(
                ChatMessage.build("Guidance", "Prioritize tools provided to you to answer the questions."))

        agent_messages.extend(ChatMessage.convert_from_context(agent.generate_context(self.prompt, self.runtime)))
        return [m.add_tag('Agent') for m in agent_messages]

    def build_openai_params(self, stream=False):
        params = {
            "model": self.runtime.model,
            "messages": self.prepare_messages(),
            "stream": stream,
            "temperature": self.runtime.temperature,
            "top_p": self.runtime.top_p,
            "seed": self.runtime.seed,
            "max_tokens": self.runtime.max_tokens,
        }

        agent = self.runtime.agent
        if agent.tools:
            params["tools"] = KomodoToolRegistry.get_definitions(agent.tools)

        if agent.provider == "openai" and agent.output_format and 'json' in agent.output_format:
            from openai.types.chat.completion_create_params import ResponseFormat
            params['response_format'] = ResponseFormat(type="json_object")

        return params

    def prepare_detailed_prompt(self):
        conversation = []
        messages = self.prepare_messages()
        for message in messages:
            conversation.append(message['role'] + ": " + message['content'])
        conversation.append("Prompt: " + self.prompt)
        return "\n".join(conversation)
