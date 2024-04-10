import openai
import requests
from datetime import date
import json

SERVER_URL = "http://54.172.175.160"

class OpenAIModule:
    # Example class to illustrate the concept; actual implementation may vary
    pass

class BlumeOpenAIWrapper:
    client_instance = None
    # Variables to store original methods
    original_completion_create = None
    original_chat_completion_create = None
    options = {}

    @staticmethod
    def send_to_backend(endpoint, data, options):
        """Send intercepted data to the backend server."""
        payload = {"query": data, "options": options}
        try:
            print("SERVER URL", f"{SERVER_URL}/llm")
            response = requests.post(f"{SERVER_URL}/llm", json=payload)
            response.raise_for_status()  # raises exception when not a 2xx response
            if response.status_code != 204:
                print("ERROR RESPONSE", response.json())
            print("Backend response: ", response.json())
        except Exception as e:
            print("Error sending data to backend: ", e)

    @classmethod
    def completion_proxy_handler(cls, *args, **kwargs):
        """Proxy handler for Completion.create or chat completions for v1+"""
        current_date = date.today().strftime("%Y-%m-%d")
        options = kwargs.pop('options', cls.options)
        options['date'] = current_date
        query_text = args[0] if args else kwargs.get('prompt', '') or kwargs.get('messages', [])
        if isinstance(query_text, list):  # Handle chat completion messages
            query_text = ' '.join([msg.get('content', '') for msg in query_text])
        print("Intercepted Completion/ChatCompletion input: ", query_text)
        cls.send_to_backend("llm", query_text, options)
        return cls.original_completion_create(*args, **kwargs)
    
    @classmethod
    def chat_completion_proxy_handler(cls, *args, **kwargs):
        """Proxy handler for Completion.create or chat completions for v1+"""
        current_date = date.today().strftime("%Y-%m-%d")
        options = kwargs.pop('options', cls.options)
        options['date'] = current_date
        query_text = args[0] if args else kwargs.get('prompt', '') or kwargs.get('messages', [])
        if isinstance(query_text, list):  # Handle chat completion messages
            query_text = ' '.join([msg.get('content', '') for msg in query_text])
        print("Intercepted Completion/ChatCompletion input: ", query_text)
        cls.send_to_backend("llm", query_text, options)
        return cls.original_chat_completion_create(*args, **kwargs)

    @classmethod
    def wrap(cls, incoming_client_instance: OpenAIModule = None, user_id: str = None, options: dict = None):
        if incoming_client_instance:
            cls.client_instance = incoming_client_instance
            # Determine which API version or method set is being used
            if hasattr(incoming_client_instance, 'Completion') and hasattr(incoming_client_instance.Completion, 'create'):
                # Save reference to the original method
                cls.original_completion_create = incoming_client_instance.Completion.create
                # Override with proxy handler
                incoming_client_instance.Completion.create = cls.completion_proxy_handler
            if hasattr(incoming_client_instance, 'ChatCompletion') and hasattr(incoming_client_instance.ChatCompletion, 'create'):
                # For OpenAI API versions where ChatCompletion is separate
                cls.original_chat_completion_create = incoming_client_instance.ChatCompletion.create
                incoming_client_instance.ChatCompletion.create = cls.chat_completion_proxy_handler  # Use the same proxy for simplicity
            # For v1+ where chat completions might be directly under chat.completions.create
            if hasattr(incoming_client_instance, 'chat') and hasattr(incoming_client_instance.chat, 'completions') and hasattr(incoming_client_instance.chat.completions, 'create'):
                # This assumes v1+ syntax; adjust as necessary based on actual OpenAI client structure
                cls.original_chat_completion_create = incoming_client_instance.chat.completions.create
                print("INCOMING", incoming_client_instance.chat.completions.create)
                print(cls.original_chat_completion_create)
                incoming_client_instance.chat.completions.create = cls.chat_completion_proxy_handler
        if options:
            cls.options = options
        return cls.client_instance

# Usage example:
# client = openai.ApiClient(...)  # or however the OpenAI client is initialized
# BlumeOpenAIWrapper.wrap(client, user_id="your_user_id", options={"some_option": "value"})
