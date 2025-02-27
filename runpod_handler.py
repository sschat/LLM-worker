import runpod
import asyncio
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Configure RunPod API key
runpod.api_key = os.getenv("RUNPOD_API_KEY")

# LLM endpoint
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "https://m35z5chdp2dfnx-5000.proxy.runpod.net/v1/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", os.getenv("RUNPOD_API_KEY"))

def call_llm_service(instruction):
    """
    Synchronous function to call the LLM service with the given instruction.
    
    Args:
        instruction (str): The instruction to send to the LLM
        
    Returns:
        dict: The processed response with text content
    """
    try:
        # Prepare headers with API key if available
        headers = {
            "Content-Type": "application/json"
        }
        if LLM_API_KEY:
            headers["Authorization"] = f"Bearer {LLM_API_KEY}"
        
        # Make the API call
        response = requests.post(
            LLM_ENDPOINT,
            json={
                "prompt": instruction,
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            },
            headers=headers
        )
        response.raise_for_status()
        
        # Parse the response from the LLM
        raw_response = response.json()
        
        # Process the response based on its structure
        if "choices" in raw_response and len(raw_response["choices"]) > 0:
            # OpenAI-compatible API format
            choice = raw_response["choices"][0]
            
            if "text" in choice:
                # Completion API format
                return {
                    "result": choice["text"],
                    "finish_reason": choice.get("finish_reason", ""),
                    "model": raw_response.get("model", ""),
                    "usage": raw_response.get("usage", {})
                }
            elif "message" in choice and "content" in choice["message"]:
                # Chat API format
                return {
                    "result": choice["message"]["content"],
                    "finish_reason": choice.get("finish_reason", ""),
                    "model": raw_response.get("model", ""),
                    "usage": raw_response.get("usage", {})
                }
            else:
                # Unknown choice format
                return {
                    "result": f"Received response in unknown format: {choice}",
                    "raw_response": raw_response
                }
        else:
            # Non-OpenAI format or custom API
            return {
                "result": raw_response.get("result", 
                          raw_response.get("output", 
                          raw_response.get("response", 
                          "Response received but format not recognized"))),
                "raw_response": raw_response
            }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "result": "Error calling LLM service"}

# Simple synchronous handler for testing
def handler(job):
    """
    Synchronous handler for RunPod serverless jobs.
    
    Args:
        job (dict): The job input from RunPod
        
    Returns:
        dict: The result of processing the job
    """
    # Get input from the job
    job_input = job["input"]
    instruction = job_input.get("instruction", "")
    
    if instruction:
        # Call the LLM service
        try:
            response = call_llm_service(instruction)
            
            # Check for errors
            if "error" in response:
                return {"status": "error", "message": response["error"]}
            else:
                # Extract the result text and return a clean response
                result_text = response.get("result", "No result returned from LLM")
                
                # Return a properly formatted response
                return {
                    "status": "success",
                    "output": result_text,
                    "metadata": {
                        "model": response.get("model", "unknown"),
                        "finish_reason": response.get("finish_reason", ""),
                        "usage": response.get("usage", {})
                    }
                }
        except Exception as e:
            return {"status": "error", "message": f"Failed to process instruction: {str(e)}"}
    else:
        # If no instruction provided
        return {"status": "error", "message": "No instruction provided"}

# Configure and start the RunPod serverless function
runpod.serverless.start({"handler": handler})