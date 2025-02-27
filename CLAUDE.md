# CLAUDE.md - LLM Worker

## Commands
- Setup: `pip install -r requirements.txt` or `conda env create -f environment.yml && conda activate runpod-app`
- Run: `python app.py`
- Test handler: `python runpod_handler.py`
- Docker build: `docker build -t my-runpod-app .`
- Docker run: `docker run -p 8000:8000 my-runpod-app`
- Test with input: `python -c "import json, runpod_handler; print(runpod_handler.handler({'input': json.load(open('test_input.json'))['input']}))"` 

## Code Style
- **Imports**: Standard library first, then third-party, finally local modules
- **Formatting**: 4-space indentation, 79 character line limit
- **Documentation**: Use docstrings for functions with triple quotes
- **Types**: Add type hints for function parameters and returns
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Use specific exceptions in try/except blocks
- **Logging**: Use logging module instead of print statements