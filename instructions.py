"""
Custom instructions for the LLM assistant.
"""

DEFAULT_SYSTEM_PROMPT = """You are a helpful, harmless, honest english speaking AI assistant. 
When a user asks you a question, respond accurately and be truthful. 
If you don't know the answer to something, say that you don't know rather than making up an answer.
Always try to be helpful, but prioritize truthfulness and honesty above all else.

- Keep responses concise and to the point
- Format output nicely using markdown when appropriate 
- If asked to generate code, make sure it's properly formatted and practical
- Do not generate content that is harmful, illegal, unethical or deceptive
- Do not share personal information about real individuals unless it is publicly available information about public figures
"""

def get_system_prompt(custom_instructions=None):
    """
    Returns the system prompt to use, incorporating any custom instructions.
    
    Args:
        custom_instructions (str, optional): Custom instructions to add to the default prompt.
        
    Returns:
        str: The complete system prompt
    """
    if custom_instructions:
        return f"{DEFAULT_SYSTEM_PROMPT}\n\nAdditional Instructions:\n{custom_instructions}"
    return DEFAULT_SYSTEM_PROMPT

def format_prompt(user_instruction, system_prompt=None):
    """
    Format a prompt for the LLM with proper system and user roles.
    
    Args:
        user_instruction (str): The user's instruction/query
        system_prompt (str, optional): Custom system prompt to use. If None, uses default.
        
    Returns:
        str: Formatted prompt ready to send to the LLM
    """
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
        
    # For chat-based models (e.g., for OpenAI format)
    formatted_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_instruction}<|im_end|>\n<|im_start|>assistant\n"
    
    return formatted_prompt

def parse_config(config_file_path=None):
    """
    Parse a configuration file for custom assistant settings.
    
    Args:
        config_file_path (str, optional): Path to a configuration file
        
    Returns:
        dict: Configuration settings
    """
    # Default configuration
    config = {
        "system_prompt": DEFAULT_SYSTEM_PROMPT,
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9,
    }
    
    # If a config file is provided, read it
    if config_file_path:
        try:
            import json
            with open(config_file_path, 'r') as f:
                custom_config = json.load(f)
                config.update(custom_config)
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    return config