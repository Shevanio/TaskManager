import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_simple_tasks(description):
    if not client.api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    
    try:
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accionables.
        Tarea: {description}
        Formato de respuesta: JSON con una lista de subtareas, cada una con un nombre y una descripción.

        """
        params = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": "Eres un asistente experto en gestión de tareas que ayuda a dividir y gestionar tareas complejas en pasos simples y accionables."},
                         {"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 300,
            "verbosity": "minimal",
            "reasoning_effort": "minimal"
        }

        response = client.chat.completions.create(**params)
        content = response.choices[0].message.content.strip()
        
        subtasks = []

        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)
        
        return subtasks if subtasks else ["Error: No se pudieron generar subtareas."]

    except Exception as e:
        print(f"Error creating tasks: {e}")
        return [f"Error: {str(e)}"]