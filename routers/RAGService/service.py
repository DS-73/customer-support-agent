# This file contain Pseudo code
'''
    This is the entry point for our RAG service
    - It initialize and create chat history for context and logging.
    - It implements ReAct Loop with max iteration of 5 
    - It will process the user query using specialized multi-agent crew.
    - Then generate a reponse 
    
'''

from build_agents import support_agent
from utils.chat_history import ChatHistoryManager
from fastapi import APIRouter

# Building Agents
agent = support_agent


router: APIRouter = APIRouter()

@router.post("/process_query")
def process_query(user_query):
    '''
        Based on the user query route it to domain specific agent
        - For exact information retrival like 
            Order ID, Refund Status(Text-To-SQL)
        - Customer Queries/Policy related information 
        - FAQs like
            What is the refund policy?(Vector Database lookup)
        - Tool calling
            Refund eligibility checking etc
        NOTE: Handle case like in invalid orderID or infinite loop etc
    '''

    user_query = user_query['query']
    session_id = user_query['user_id']
    metadata = user_query['metadata']

    # Creating chat history for context management
    # Or retriving if already exist
    history = ChatHistoryManager(session_id=session_id)
    state = AgentState(
        session_id = session_id,
        user_query = user_query,
        query_metadata = metadata,
        chat_history = history,
        iteration = 0
    )
    
    # Adding User query to chat history
    history.save_message(role = "user", content = user_query)


    # MAX iteration allowed in REACT LOOP to avaoin infinite tool calling 
    MAX_ITERATIONS = 5

    # ReACT Loop
    while state.iteration < MAX_ITERATIONS:
        state.iteration += 1

        # Reason Block
        # Agent give decision for user query
        #      Output: 
        #           - decision_type: tool calling, human handoff etc
        #           - content: Response 
        decision = agent.generate(  
            system_prompt = agent.prompts["react_system"],
            chat_history = state.chat_history,
            current_query = state.user_query,
            available_tools = agent.tools
        )

        if decision.type == "final_answer":
            answer = decision.content
            ### Saving AI response to chat history
            history.save_message(role="AI Assistant", content=answer)

            return {
                "answer": answer,
                "session_id": session_id
            }
        elif decision.type == "tool_call":
            tool_output = execute_tool()

            state.chat_history.append({
                "role": "tool",
                "content": tool_output
            })
        elif decision.type == "human_handoff":
            return {
                "answer": "Your request has been forwarded for human assistance.",
            }

    ### Maximum iteration for ReAct loop reached
    return graceful_termination()