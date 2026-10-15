# This file contain Pseudo code
'''
    Support agent configuration is described here
        - Model selection(orchestrator, tts_model, retriver etc)
        - Tool selection(process_refund, track_order, get_history, human_handoff etc)
        - Prompt selection(Registory storing prompts: RAG prompt, system prompts, Guardrails etc)
    etc.

'''

from utils.prompt_registry
from utils.tools import process_refund, track_order, get_transaction_history, get_refund_status, vector_db_retriver, human_handoff

from Agents import Agent_Builder
from OpenAI import chatOpenAI
from Anthropic import chatAnthropic
from Gemini import chatGemini


## Building specialized agent crew for handling different queries
def build_crew():
    '''
        It initilize crew when RAG service is started to warm agents in environment
        Building our agentic crew for queries routing, processing, retriever etc
            - It has access to tools, prompts etc

    '''
    # Orchestrator model
    orchestrator = chatGemini(os.environ.get('GEMINI_MODEL'))

    # Text-to-SQL model
    tts_model = chatOpenAI(os.environ.get('TTS_MODEL'))

    # Retriver model
    retriver_model = chatAnthropic(os.environ.get('RETRIVER_MODEL'))


    agent_config = Agent_Builder(
        model = orchestrator,
        crew = [tts_model, retriver_model],
        tools = [process_refund, track_order, get_transaction_history, get_refund_status, vector_db_retriver, human_handoff],
        prompts = prompt_registry.pompts,
        max_iterations = 8,
        temperature = 0
    )

    return agent_config

support_agent = build_crew()