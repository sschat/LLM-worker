import runpod
import asyncio
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Configure RunPod API key
runpod.api_key = os.getenv("RUNPOD_API_KEY")
endpoint = runpod.Endpoint(os.getenv("RUNPOD_ENDPOINT_ID"))

# LLM endpoint
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "https://m35z5chdp2dfnx-5000.proxy.runpod.net/v1/completions")
LLM_API_KEY = os.getenv("RUNPOD_API_KEY")

def call_llm_service(instruction):
    """
    Call the LLM service with the given instruction.
    
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

async def async_generator_handler(job):
    """
    Handler for RunPod serverless jobs.
    
    Args:
        job (dict): The job input from RunPod
        
    Yields:
        str or dict: Status updates and final result
    """
    # RunPod provides input in job["input"]
    job_input = job["input"] if isinstance(job, dict) and "input" in job else {}
    instruction = job_input.get("instruction", "")
    
    if instruction:
        # First generate a message that we're processing
        yield {"status": "processing", "message": "Processing instruction with LLM..."}
        
        # Call the LLM service
        try:
            # Get response from LLM (now a regular function, not a coroutine)
            # so no need for asyncio.to_thread
            response = call_llm_service(instruction)
            
            # Check for errors
            if "error" in response:
                yield {"status": "error", "message": response["error"]}
            else:
                # Extract the result text and return a clean response
                result_text = response.get("result", "No result returned from LLM")
                
                # Return a properly formatted response
                yield {
                    "status": "success",
                    "output": result_text,
                    "metadata": {
                        "model": response.get("model", "unknown"),
                        "finish_reason": response.get("finish_reason", ""),
                        "usage": response.get("usage", {})
                    }
                }
        except Exception as e:
            yield {"status": "error", "message": f"Failed to process instruction: {str(e)}"}
    else:
        # If no instruction provided, fall back to demo mode
        yield {"status": "warning", "message": "No instruction provided, falling back to demo mode"}
        for i in range(5):
            output = f"Generated async token output {i}"
            yield {"status": "demo", "output": output}
            await asyncio.sleep(1)

# Configure and start the RunPod serverless function
runpod.serverless.start(
    {
        "handler": async_generator_handler,
        "return_aggregate_stream": True,
    }
)