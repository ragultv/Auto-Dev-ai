# Auto-Dev-ai Backend

This is the backend API for the Auto-Dev-ai platform, built with FastAPI and Python.

## Features

- **Planner Agent**: Creates project plans based on prompts
- **Research Agent**: Searches web and datasets for information
- **Coder Agent**: Generates ML/DL code
- **Tester Agent**: Runs unit tests and retries failed tests
- **Evaluator Agent**: Evaluates performance and code quality
- **Executor Service**: Manages Docker container execution
- **Database**: SQLAlchemy models for projects, executions, and datasets

## Project Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI entrypoint
│   ├── config.py                    # Configurations
│   ├── dependencies.py              # Common dependencies
│   │
│   ├── routes/                      # API endpoints
│   │   ├── __init__.py
│   │   ├── prompts.py               # Prompt submissions
│   │   ├── agents.py                # Agent triggers
│   │   ├── execution.py             # Execution control
│   │   ├── evaluation.py            # Metrics & evaluation
│   │
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── planner_service.py       # Planner logic
│   │   ├── research_service.py      # Research logic
│   │   ├── coder_service.py         # Code generation
│   │   ├── tester_service.py        # Testing logic
│   │   ├── executor_service.py      # Docker execution
│   │   ├── evaluator_service.py     # Evaluation logic
│   │
│   ├── agents/                      # LangChain agents
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Base agent class
│   │   ├── planner_agent.py         # Planner agent
│   │   ├── research_agent.py        # Research agent
│   │   ├── coder_agent.py           # Coder agent
│   │   ├── tester_agent.py          # Tester agent
│   │   ├── evaluator_agent.py       # Evaluator agent
│   │
│   ├── models/                      # Database models
│   │   ├── __init__.py
│   │   ├── project.py               # Project model
│   │   ├── execution.py             # Execution model
│   │   ├── dataset.py               # Dataset model
│   │
│   ├── schemas/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── prompt_schema.py         # Prompt schemas
│   │   ├── agent_schema.py          # Agent schemas
│   │   ├── execution_schema.py      # Execution schemas
│   │
│   ├── utils/                       # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py                # Logging utilities
│   │   ├── docker_utils.py          # Docker utilities
│   │   ├── dataset_utils.py         # Dataset utilities
│   │   ├── metrics_utils.py         # Metrics utilities
│   │
│   ├── database.py                  # Database connection
│
├── tests/                           # Tests
│   ├── __init__.py
│   ├── test_agents.py               # Agent tests
│   ├── test_execution.py            # Execution tests
│   ├── test_endpoints.py            # Endpoint tests
│
├── scripts/                         # Scripts
│   ├── seed_data.py                 # Database seeding
│   ├── run_docker.py                # Docker management
│
├── docker/                          # Docker files
│   ├── Dockerfile                   # Docker image
│   ├── docker-compose.yml           # Docker compose
│
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
└── README.md                        # This file
```

## Installation

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```
6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Prompts
- `POST /api/v1/prompts/` - Create a new prompt
- `GET /api/v1/prompts/` - Get all prompts
- `GET /api/v1/prompts/{prompt_id}` - Get a specific prompt

### Agents
- `POST /api/v1/agents/planner` - Trigger planner agent
- `POST /api/v1/agents/research` - Trigger research agent
- `POST /api/v1/agents/coder` - Trigger coder agent
- `POST /api/v1/agents/tester` - Trigger tester agent
- `POST /api/v1/agents/evaluator` - Trigger evaluator agent

### Execution
- `POST /api/v1/execution/` - Create a new execution
- `GET /api/v1/execution/` - Get all executions
- `GET /api/v1/execution/{execution_id}` - Get a specific execution
- `POST /api/v1/execution/{execution_id}/start` - Start an execution
- `POST /api/v1/execution/{execution_id}/stop` - Stop an execution

### Evaluation
- `GET /api/v1/evaluation/{execution_id}/metrics` - Get execution metrics
- `POST /api/v1/evaluation/{execution_id}/evaluate` - Evaluate an execution
- `GET /api/v1/evaluation/metrics/summary` - Get metrics summary

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create tables
python -c "from app.database import create_tables; create_tables()"
```

### Docker
```bash
# Build and run with Docker Compose
cd docker
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 