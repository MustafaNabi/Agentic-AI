# Module imports
import ollama
from fastmcp import Client
from pydantic import BaseModel, Field
import asyncio
import time
from pathlib import Path
path = Path("/home/omen15/Development/Agentic AI/mcp_servers/basic_math.py")


async def tool_call_at_once(client, tool_call):
    tool = tool_call.function.name
    arguments = tool_call.function.arguments
    result =  await client.call_tool(tool, arguments)
    return result, tool, arguments






async def main():
    async with Client(path) as client:
        
        tools = []
        mcp_tools = await client.list_tools()
        for tool in mcp_tools:
            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                    },
                })
        
        MAX_TRIES = 15
        model = "gemma4:e4b"
        options = {"num_ctx": 36864, "temperature": 0.5}
        system_prompt = "You are a helpful assistent with expertise in complex mathematics. Assume the role of an mathematician. Be brief in response unless asked for verbose response"
        messages = [{"role": "system", "content": system_prompt}]
        message = input('Welcome to Calculator!!\nEnter "quit" to quit\nEnter "help" for help\n\nAsk your question: ')
               
        
        while True:
           
            if message == "quit":
                print("Exiting ...")
                exit(0)
            elif message == "help":
                print('"Calculater" is an LLM based math tool that can do perform complex calculations\nEnter you math question in English\n\n')
                message = input("Ask your Question: ")
                continue
            else:
                messages.append({"role": "user", "content": message})
                
            for tries in range(MAX_TRIES):
                response = ollama.chat(
                    model=model,
                    messages=messages,
                    tools=tools,
                    options=options,
                    keep_alive="10m"
                )

                messages.append(response.message)
            

                if not response.message.tool_calls:
                    print(response.message.content, end="\n\n")
                    break
                
                if response.message.tool_calls:
                    results =  await asyncio.gather(*(tool_call_at_once(client, tool_call) for tool_call in response.message.tool_calls))   

                    for result, tool, arguments in results:
                        messages.append({
                            "role": "tool",
                            "content": str(result)
                            })
            else:
                print(f"Answer could not be calculated in {MAX_TRIES} iterations\n\n")
            message = input("Ask your next Question: ")
            messages.append({"role": "User", "content": message})

if __name__ == "__main__":
    asyncio.run(main())
