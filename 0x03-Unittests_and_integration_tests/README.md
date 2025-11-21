# 0x03 - Unittests and Integration Tests

Project focused on writing and organizing automated tests (unit and integration) for Python backend code.

## Requirements

- Python 3.8+
- pytest
- (optional) coverage

## Setup

1. Create and activate virtual environment
   - python3 -m venv venv
   - source venv/bin/activate
2. Install dependencies
   - pip install -r requirements.txt
   - or: pip install pytest coverage

## Running tests

- Run all tests:
  - pytest
- Run unit tests only (common layout: tests/unit):
  - pytest tests/unit
- Run integration tests only (common layout: tests/integration):
  - pytest tests/integration
- Run a single test:
  - pytest tests/unit/test_module.py::test_name -q

## Test coverage

- Generate coverage report:
  - coverage run -m pytest
  - coverage report -m
  - coverage html # opens a browsable report

## Test organization (recommended)

- tests/
  - unit/ # fast, isolated tests (mock external deps)
  - integration/ # tests that exercise multiple components or external services
- tests should mirror source package structure and be deterministic

## Conventions

- Use pytest fixtures for setup/teardown
- Keep unit tests small and fast
- Mark slow or external-dependent tests (e.g., @pytest.mark.integration) and exclude during quick runs:
  - pytest -m "not integration"

## CI

- Run pytest and coverage on every push
- Fail build on test failures or low coverage thresholds

## Contributing

- Write tests for bug fixes and features
- Follow existing test patterns and naming conventions
- Run the test suite locally before submitting changes

## License

Specify project license in LICENSE file.

(Adjust paths, commands, and tools for your repo as needed.)
