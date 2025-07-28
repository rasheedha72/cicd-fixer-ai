import os
import subprocess
import json
import re
from datetime import datetime
import uuid

# 1. Process the uploaded log file (original logic)
def process_log(file_path):
    try:
        with open(file_path, 'r') as file:
            log_content = file.read()
        return log_content
    except Exception as e:
        return f"Error reading log file: {str(e)}"

# 2. Run offline LLM via Ollama (Mistral or other)
def ask_ollama(prompt, model='mistral'):
    command = ['ollama', 'run', model]
    try:
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output, error = process.communicate(input=prompt)
        if error:
            return f"Error from Ollama: {error}"
        return output
    except Exception as e:
        return f"Failed to run Ollama: {str(e)}"

# 3. Save log and AI fix to memory.json
def save_to_memory(log, ai_fix):
    try:
        with open("app/memory.json", "r") as f:
            memory = json.load(f)
    except:
        memory = {}

    log_id = str(uuid.uuid4())
    memory[log_id] = {
        "log_content": log,
        "ai_fix": ai_fix,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    with open("app/memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# 4. Construct AI prompt from log and get AI fix
def get_ai_fix(log_text):
    prompt = f"""You are a CI/CD expert AI. A user has shared this log from their failed CI/CD pipeline:

{log_text}

Please analyze the error and suggest a possible reason for the failure along with a step-by-step fix."""
    
    response = ask_ollama(prompt)
    
    # Save to memory
    save_to_memory(log_text, response)

    return response

# 5. Highlight key log sections (optional HTML styling)
def highlight_sections(log):
    log = re.sub(r"\[BUILD\]", "<span style='color:blue;'>[BUILD]</span>", log)
    log = re.sub(r"\[DEPLOY\]", "<span style='color:green;'>[DEPLOY]</span>", log)
    log = re.sub(r"\[ERROR\]", "<span style='color:red;'>[ERROR]</span>", log)
    return log
