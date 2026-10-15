'''

    Defined tools for our agents to use
        - process_refund: Check eligibility and process refund if eligible(using refund service[can pass human for final approval])
        - track_order: Get status or order(DELIVERED, PLACED etc)
        - get_transaction_history: Get customer transaction history from order table.
        - get_refund_status: Check refund status(PROCESSED, COMPLETED etc)
        - vector_db_retriver: Retrieve context from vector db when required
        - human_handoff: handover to human agent

'''

from langchain_core.tools import tool

## Defining tools
@tool
def process_refund(order_id: str, reason: str):
    '''
        Use this tool to validate eligibility and process customer refund.
    '''
    order = database.get_order(order_id)
    if not order:
        return 'Order not found'
    elif not refund_service.is_eligible(order, reason):
        return 'Refund not eligible'

    refund = refund_service.process(
        order_id = order_id,
        amount = order.refundable_amount,
    )

    return refund.status

@tool
def track_order(order_id: str):
    '''
        Use this tool to Retrieve order and delivery tracking details.
    '''
    order = database.get_order(order_id)
    if not order:
        return 'Order not found'

    return {
        'order_status': order.status,
        'delivery_status': order.delivery_status
    }

@tool
def get_transaction_history(customer_id: str, order_id=None):
    '''
        Use this tool to retrieve customer payment and refund history.
    '''

    transaction = database.get_transactions_history(
        customer_id=customer_id,
        order_id=order_id,
    )

    if not transaction:
        return 'No transaction found please check order_id'

@tool
def get_refund_status(refund_id: str):
    '''
        Use this to check the current status of a refund.
    '''

    refund = refund_service.get_status(refund_id)

    return refund or 'Refund not found'

@tool
def vector_db_retriver(query):
    '''
        Use this to retrive relavent documents from vector database
        - This tool perform efficient retriveal of documents(reranking, hybrid search)
    '''

    client = vector_db.client()
    response = client.retrieve()

    return response

@tool
def human_handoff(history):
    '''
        This is a human handoff tool. Use it when human intervention is required
    '''
    connect_human()
    return {'msg': 'Connecting to human agent'}
