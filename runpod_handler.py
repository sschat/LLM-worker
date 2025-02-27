import runpod
import asyncio
import os
import requests
from dotenv import load_dotenv
load_dotenv()

runpod.api_key = os.getenv("RUNPOD_API_KEY")
endpoint = runpod.Endpoint(os.getenv("RUNPOD_ENDPOINT_ID"))

# LLM endpoint
LLM_ENDPOINT = "https://m35z5chdp2dfnx-7860.proxy.runpod.net/"

async def call_llm_service(instruction):
    """
    Call the LLM service with the given instruction.
    
    Args:
        instruction (str): The instruction to send to the LLM
        
    Returns:
        dict: The response from the LLM service
    """
    try:
        response = requests.post(
            LLM_ENDPOINT,
            json={"prompt": instruction}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

async def async_generator_handler(job):
    job_input = job.get("input", {})
    instruction = job_input.get("instruction", "")
    
    if instruction:
        # First generate a message that we're processing
        yield "Processing instruction with LLM..."
        
        # Call the LLM service
        result = await asyncio.to_thread(call_llm_service, instruction)
        
        # Return the result
        yield result
    else:
        # If no instruction provided, fall back to demo mode
        for i in range(5):
            output = f"Generated async token output {i}"
            yield output
            await asyncio.sleep(1)

# Configure and start the RunPod serverless function
runpod.serverless.start(
    {
        "handler": async_generator_handler,
        "return_aggregate_stream": True,
    }
)