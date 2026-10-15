'''
    This is the entry point for our customer service agent
    - It will capture the user input(Voice/Text) and process it 
    - Here we extract query, metadata, session_id, etc
    - After processing and validation respond back to user with generate response

'''

@app.post("/query")
def get_input(request):
    '''
        Process the user request
        - If query_type is voice 
            Convert speech to text

        Check user query for prompt injection, jailbreak attempt, malicious URLs etc
            - If true:
                return 
            - Else 
                - forward to RAG service for processing
                - check RAG response for PII, PHI etc
                    - Sanitize response
                    Example: Credit card numbers

                        1111 1111 1111 0000 -> xxxx xxxx xxxx 0000

                return reducted reponse    
    '''

    # Process user query and convert to text if voice 
    if request['query_type'] == 'voice':
        text_query, speech_features = speech_to_text(request['query'])
        metadata = {request['metadata'] + speech_features}
    else: 
        text_query = request['query_text']
        metadata = request['metadata']

    user_query = {
        "query": text_query,
        "session_id": request["session_id"],
        "metadata": metadata
    }

    # Based on rule and thresholds check query for malicious intent
    if sanitize_query(user_query):
        # Log all details 
        logger.log(details)

        # Generic Response message with invalid status
        return Response({
            "msg": "Sorry I cannot answer this",
            "invalid": "Query is not allowed.",
        })

    # Send user query to RAG Service
    response = RAG_service(user_query)
    response_text = response.content
    
    ## Sanitize repsonse
    if sanitize_response(response_text):
        logger.log(details)

        return Response(
            "msg": response_text
        )
    