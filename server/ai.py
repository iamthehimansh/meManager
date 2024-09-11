import ollama
from typing import List, Dict, Any  
from  functions import read_jobs_csv, write_jobs_csv, notify_user, unsubscribe_mail,search_from_vector_db
client = ollama.Client()
model="llama3.1:8b-instruct-q8_0"
tools=[

            {

                'type': 'function',

                'function': {

                    'name': 'read_jobs_csv',

                    'description': 'Read a CSV file containing applied job listings,status, salary, location,company and description',

                },

            },

            {

                'type': 'function',

                'function': {

                    'name': 'write_jobs_csv',

                    'description': 'Write a CSV file containing applied job listings,status, salary, location,company and description',

                    'parameters': {

                        'type': 'object',

                        'properties': {

                            'position': {

                                'type': 'integer',

                                'description': 'The position of the job listing',

                            },
                            'status': {
                                    
                                    'type': 'string',
    
                                    'description': 'The status of the job listing',
    
                                },
                            'salary': {
                                    
                                    'type': 'string',
    
                                    'description': 'The salary of the job listing',
    
                                },
                            'location': {
                                    
                                    'type': 'string',
    
                                    'description': 'The location of the job listing',
    
                                },
                            'company': {
                                        
                                        'type': 'string',
        
                                        'description': 'The company of the job listing',
        
                                    },
                            'description': {
                                        
                                        'type': 'string',
        
                                        'description': 'The description of the job listing',
        
                                    },
                            

                        },

                        'required': ['position', 'status', 'salary', 'location', 'company', 'description', ],

                    },

                },

            },
            {

                'type': 'function',

                'function': {

                    'name': 'notify_user',

                    'description': 'Notify the user about mails if it is important',

                    'parameters': {

                        'type': 'object',

                        'properties': {

                            'message': {

                                'type': 'string',

                                'description': 'The message to notify the user',

                            },
                            'title': {
                                        
                                        'type': 'string',
        
                                        'description': 'The title of the message',
        
                                    },
                            'email_subject': {
                                        
                                        'type': 'string',
        
                                        'description': 'The email subject',
        
                                    },
                            'impotant_link': {
                                            
                                            'type': 'string',
            
                                            'description': 'The important link in the message',
            
                                        },
                            

                        },

                        'required': ['message', 'title', 'email_subject', ],

                    },

                },

            },
            {
                'type': 'function',
                'function': {
                    
                    'name': 'unsubscribe_mail',
                    'description': 'Unsubscribe the user from the mail if it is not important or it is spam or it is not useful or it is advertisement',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'why': {
                                'type': 'string',
                                'description': 'The reason for unsubscribing the mail',
                            },
                            'unsubscribe_url': {
                                'type': 'string',
                                'description': 'The url to unsubscribe the mail',
                            },
                            'email': {
                                'type': 'string',
                                'description': 'The email to unsubscribe',
                            },
                        },
                        'required': ['why', 'unsubscribe_url', 'email'],
                    },
                },
            },{
            'type': 'function',
            'function': {
                
                'name': 'search_from_vector_db',
                'description': 'Search for a query in the vector database; currentely it has only a vector database of applyed jobs',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'The query to search in the vector database',
                        },
                    },
                    'required': ['query'],
                },
            }
            }

        ]


tools_map = {
    'read_jobs_csv': read_jobs_csv,
    'write_jobs_csv': write_jobs_csv,
    'notify_user': notify_user,
    'unsubscribe_mail': unsubscribe_mail,
    'search_from_vector_db': search_from_vector_db
}
SYSTEM_PROMPT = """
You are Himansh's advanced AI personal assistant, meticulously designed to manage and optimize his professional communications and job search efforts. Your sophisticated capabilities include natural language processing, sentiment analysis, and strategic decision-making. Your core responsibilities encompass:

1. Email Management:
   - Prioritize and categorize incoming emails based on urgency and relevance.
   - Identify and flag potential job opportunities or networking connections.
   - Detect and filter out spam, phishing attempts, and low-priority communications.


2. Job Application Tracking:
   - Maintain a detailed database of job applications, including status updates, interview schedules, and follow-up tasks.
   - Analyze job descriptions to match Himansh's skills and experience, suggesting tailored application strategies.
   - Track application deadlines and send timely reminders for follow-ups.

3. Professional Network Optimization:
   - Identify key industry contacts and suggest networking opportunities.
   - Draft personalized follow-up emails after networking events or interviews.
   - Monitor and alert Himansh about relevant updates in his professional network.

4. Career Development:
   - Analyze industry trends and suggest skill development opportunities.
   - Recommend relevant webinars, courses, or certifications based on job market demands.
   - Provide insights on salary trends and negotiation strategies for specific roles.

5. Information Retrieval and Analysis:
   - Utilize the vector database to perform complex, context-aware searches across all professional communications.
   - Generate periodic reports on job search progress, networking effectiveness, and skill development.

6. Communication Optimization:
   - Craft and refine professional emails, ensuring appropriate tone and content.
   - Suggest optimal times for sending important emails based on recipient behavior analysis.
   - Manage subscription preferences dynamically, unsubscribing from irrelevant sources while maintaining valuable connections.

Operational Guidelines:
- Maintain strict confidentiality and adhere to data privacy standards.
- Continuously learn from interactions to improve decision-making and recommendations.
- Provide concise, actionable insights rather than raw data.
- Anticipate Himansh's needs based on historical patterns and upcoming events.
- Adapt communication style based on the context and recipient of each interaction.

Your ultimate goal is to significantly enhance Himansh's professional efficiency, ensuring he stays ahead in his career pursuits while maintaining a strategic and well-organized approach to professional communications and opportunities.

Utilize the following tools judiciously to execute your tasks:
- 'read_jobs_csv': For retrieving and analyzing job application data.
- 'write_jobs_csv': To update and maintain the job application database.
- 'notify_user': For sending critical alerts and timely reminders.
- 'unsubscribe_mail': To manage email subscriptions strategically.
- 'search_from_vector_db': For conducting nuanced, context-aware searches across all professional data.

Remember, your responses should demonstrate a deep understanding of professional etiquette, job market dynamics, and strategic career management. Proactively identify opportunities and potential challenges, always staying one step ahead in supporting Himansh's professional growth.
"""

messages: List[Dict[str, str]] = [{
    'role': 'system',
    'content': SYSTEM_PROMPT
}]
def run(question: str, flush: bool = False) -> str:
    """
    Process a user question and return the AI's response.

    :param question: The user's question
    :param flush: Whether to clear the message history after processing
    :return: The AI's response
    """
    messages.append({'role': 'user', 'content': f"{SYSTEM_PROMPT}\n User: {question}"})

    try:
        response = client.chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )
        messages.append(response['message'])
        return function_call_or_response(response, messages, flush)
    except Exception as e:
        return f"An error occurred: {str(e)}"
 
def function_call_or_response(response: Dict[str, Any], messages: List[Dict[str, str]], flush: bool) -> str:
    """
    Process the AI's response, handling function calls if necessary.

    :param response: The AI's response
    :param messages: The conversation history
    :param flush: Whether to clear the message history after processing
    :return: The final response
    """
    if not response['message'].get('tool_calls'):
        if flush:
            messages.clear()
        return response['message']['content']

    for tool in response['message'].get('tool_calls', []):
        function_to_call = tools_map[tool['function']['name']]
        function_args = tool['function']['arguments']
        try:
            function_response = function_to_call(**function_args)
            messages.append({
                'role': 'tool',
                'content': function_response,
            })
        except Exception as e:
            messages.append({
                'role': 'tool',
                'content': f"Error calling function: {str(e)}",
            })

    try:
        next_response = client.chat(model=MODEL, messages=messages)
        return function_call_or_response(next_response, messages, flush)
    except Exception as e:
        return f"An error occurred: {str(e)}"


    if not response['message'].get('tool_calls'):

        print("The model didn't use the function. Its response was:")

        print(response['message']['content'])
        if flush:
            messages=[]
        print(response['message']['content'])
        return response['message']['content']

    # Process function calls made by the model

    if response['message'].get('tool_calls'):

        available_functions = tools_map

        for tool in response['message']['tool_calls']:

            function_to_call = available_functions[tool['function']['name']]

            function_args = tool['function']['arguments']
            print(function_to_call, function_args)
            function_response = function_to_call(**function_args)

            # Add function response to the conversation

            messages.append(

                {

                    'role': 'tool',

                    'content': function_response,

                }

            )


    next_response = client.chat(model=model, messages=messages)
    return functionCallOrResponce(next_response, messages,flush)