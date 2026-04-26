"""
Backend API for AI Tutor & Quiz Generator using Mistral and LLaMA 2 via Ollama.

This FastAPI application provides two modes of educational assistance:
1. Quiz Generation: Creates customized quizzes on any topic
2. Concept Explanation: Provides clear explanations of educational concepts
"""

from fastapi import FastAPI, Form
import requests
import json

app = FastAPI()
OLLAMA_TIMEOUT_SECONDS = 1800

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def read_ollama_stream(response: requests.Response) -> str:
    """Read Ollama's streamed NDJSON chunks into one response string."""
    chunks = []
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        chunks.append(data.get("response", ""))
        if data.get("done"):
            break
    return "".join(chunks).strip()


def call_ollama(payload: dict) -> str:
    """Call Ollama with streaming enabled so long local generations stay alive."""
    streamed_payload = {**payload, "stream": True}
    with requests.post(
        OLLAMA_API_URL,
        json=streamed_payload,
        timeout=(10, OLLAMA_TIMEOUT_SECONDS),
        stream=True,
    ) as response:
        response.raise_for_status()
        return read_ollama_stream(response)

@app.post("/quiz/")
def generate_quiz(topic: str = Form(...), num_questions: int = Form(5)):
    """
    Generate a customized quiz on a given topic.

    Uses Mistral to create quiz questions with varying difficulty levels,
    multiple choice options, and correct answers.

    Args:
        topic: The subject area for the quiz
        num_questions: Number of questions to generate (default: 5)

    Returns:
        A dictionary containing the generated quiz questions
    """
    # Construct a structured prompt for quiz generation
    # Request specific format with numbered questions, 4 options, and correct answer
    # This ensures the LLM outputs consistently formatted quizzes
    prompt = (
        f"Create a {num_questions}-question quiz on {topic}.\n\n"
        "Format each question as:\n"
        "Q[n]: [Question]\n"
        "A) [Option A]\n"
        "B) [Option B]\n"
        "C) [Option C]\n"
        "D) [Option D]\n"
        f"Answer: [Correct Answer]\n\n"
        f"Generate {num_questions} questions about {topic}:\n"
    )

    # Send the quiz request to Ollama using Mistral.
    # The helper streams chunks from Ollama, then returns one complete quiz.
    result = call_ollama({
        "model": "mistral",  # Mistral for quiz generation
        "prompt": prompt,     # Structured prompt with format requirements
    })

    # Return the generated quiz to the frontend.
    return {"quiz": result}

@app.post("/explain/")
def explain_concept(topic: str = Form(...)):
    """
    Provide a clear explanation of an educational concept.

    Uses LLaMA 2 to explain topics in an accessible, structured manner
    suitable for learning.

    Args:
        topic: The concept to explain (from HTML form data)

    Returns:
        A dictionary containing the concept explanation
    """
    # Construct a prompt for educational explanation
    # Request structured output with definition, key concepts, examples, and misconceptions
    # This helps learners get comprehensive understanding of any topic
    prompt = (
        f"Explain the following topic in a clear, educational manner:\n\n"
        f"{topic}\n\n"
        "Include:\n"
        "- Simple definition\n"
        "- Key concepts and terminology\n"
        "- Real-world examples\n"
        "- Common misconceptions"
    )

    # Send the explanation request to Ollama using LLaMA 2.
    # The helper streams chunks from Ollama, then returns one complete explanation.
    result = call_ollama({
        "model": "llama2",  # LLaMA 2 for educational explanations
        "prompt": prompt,    # Structured prompt with educational framework
    })

    # Return the explanation to the frontend.
    return {"explanation": result}
