# Project 10: AI Tutor & Quiz Generator (LearnSphere Academy)

An AI-powered assistant for educators and learners that simplifies complex lessons, generates quizzes with answers, and extracts key learning concepts. Perfect for creating educational content and study aids.

## Features

- **Student-Friendly Explanations**: Simplifies complex topics for easy understanding
- **Auto-Generated Quizzes**: Creates customized quizzes with 5 questions and answers
- **Key Concept Extraction**: Identifies 5-10 important terms for revision
- **FastAPI Backend**: Efficient REST API for educational content generation
- **Streamlit Frontend**: User-friendly interface for educators and learners
- **Local Processing**: All analysis runs locally using Ollama LLMs - no external API dependencies

## Architecture

### Backend Components

1. **Quiz Generator** (`backend/main.py`)
   - Creates customized quizzes on any topic
   - Generates multiple choice questions with options
   - Provides correct answers for grading

2. **Concept Explainer** (`backend/main.py`)
   - Provides clear explanations of educational concepts
   - Simplifies complex topics
   - Adapts to different learning levels

### Frontend Components

1. **Streamlit UI** (`frontend/app.py`)
   - User interface for educators and learners
   - Topic input and quiz generation
   - Results display and export

2. **Reusable Components** (`frontend/components.py`)
   - Modular UI elements
   - Consistent styling and layout

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local LLM inference)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd SchoolOfAI/Official/soai-10-ai-tutor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama** (if not already installed):
   ```bash
   # Install Ollama from https://ollama.com
   # Pull a model (mistral is recommended for speed)
   ollama pull mistral
   # Or pull llama2 for better reasoning
   ollama pull llama2
   # Start Ollama service
   ollama serve
   ```

## Running the Application

### Backend API

1. **Start the FastAPI backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Access the API**: Navigate to `http://localhost:8000` for API documentation

### Frontend UI

1. **Start the Streamlit application** (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

2. **Open your browser**: Navigate to `http://localhost:8501`

## Usage

### 1. Generate Quiz

- Enter your topic in the input field
- Select number of questions (default: 5)
- Click "Generate Quiz" to create questions
- View questions, options, and correct answers

### 2. Explain Concepts

- Enter a concept or topic to explain
- Click "Explain" to get a student-friendly explanation
- Review the simplified explanation

### 3. Extract Key Concepts

- Paste lesson content or notes
- Click "Extract Concepts" to identify key terms
- Review the list of 5-10 important concepts

### 4. Export Results

- Copy quiz questions for use in your materials
- Export explanations as text
- Save key concepts for revision

## Workflow

```
User Input → Backend API → Ollama LLM → Generate Content → Display Results
     ↓              ↓            ↓                ↓                  ↓
  Enter topic  FastAPI     Call model      Quiz/Explanation   Show to
              endpoint     with prompt    generation        user
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=mistral
OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Ollama Models

The system supports any Ollama model. Recommended models:
- `mistral` - Fast and efficient for text simplification (default)
- `llama2` - Better reasoning and multi-step analysis

## Project Structure

```
soai-10-ai-tutor/
├── backend/
│   └── main.py                  # FastAPI backend
├── frontend/
│   ├── app.py                    # Streamlit UI
│   └── components.py             # Reusable UI components
├── data/
│   └── sample_lesson.txt         # Sample lesson content
├── requirements.txt              # Python dependencies
└── README.md                   # This file
```

## Dependencies

- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `streamlit` - Web UI framework
- `requests` - HTTP client for Ollama API
- `python-dateutil` - Date/time parsing

## Troubleshooting

### Ollama Connection Issues

If you see connection errors:
1. Verify Ollama is running: `ollama list`
2. Check the API URL: `curl http://localhost:11434/api/generate`
3. Ensure the model is pulled: `ollama pull mistral`

### Backend API Issues

If the backend isn't responding:
1. Verify uvicorn is running: `ps aux | grep uvicorn`
2. Check the port isn't in use: `lsof -i :8000`
3. Review backend logs for errors

### Frontend Connection Issues

If the frontend can't connect to the backend:
1. Verify both services are running
2. Check the API URL in frontend/app.py
3. Ensure CORS is configured correctly

### Quiz Generation Issues

If quiz questions aren't being generated:
1. Check that the topic is specific enough
2. Verify the LLM model is appropriate
3. Review the prompt in backend/main.py
4. Try with a different model (llama2 vs mistral)

### Slow Performance

For faster generation:
1. Use mistral for speed
2. Reduce the number of questions
3. Increase Ollama's GPU resources if available
4. Simplify the topic or lesson content

## Use Cases

- **Educators**: Create quizzes for lessons quickly
- **Students**: Generate practice questions for revision
- **Content Creators**: Extract key concepts from materials
- **Self-Study**: Simplify complex topics for understanding
- **Curriculum Development**: Build educational content efficiently

## Input Format

The system accepts:
- **Educational Content**: Lecture notes, textbook paragraphs, pasted text
- **Sample Lesson**: Provided in `data/sample_lesson.txt`
- **Topics**: Any subject or concept to explain

## Output Format

The system generates:
- **Student-Friendly Explanation**: Simplified version of complex content
- **5-Question Quiz**: Multiple choice or short-answer with answers
- **Key Concepts List**: 5-10 important terms for revision

## Important Notes

- All processing happens locally - no data is sent to external servers
- Quiz quality depends on the specificity of the topic
- Explanations are AI-generated and should be reviewed for accuracy
- Mistral is faster but llama2 may provide better reasoning
- Both models support text simplification and question generation

## License

This project is part of the School of AI curriculum.
