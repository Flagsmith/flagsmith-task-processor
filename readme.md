# Flagsmith Task Processor

This repository holds the code responsible for the Flagsmith Task Processor functionality. 

## Development

This repository contains a django app that is intended to be used only when integrated 
with the main [Flagsmith repository](https://github.com/flagsmith/flagsmith) or other 
Flagsmith dependencies. 

### Local Setup

This repository uses poetry for package management and versioning. Run the following
commands to set up a local development environment and run the unit tests. 

```bash
pip install poetry
poetry install
export DJANGO_SETTINGS_MODULE=tests.settings DATABASE_URL=postgres://postgres:password@localhost:5432/flagsmith_task_processor
poetry run pytest tests/unit
```

### Testing

#### Unit

The unit tests should be run using pytest as usual, these tests should mock out any 
external dependencies or create test classes as needed.

### Publishing & Releases

This package is included as a dependency in the main Flagsmith repository. New releases 
should be created using the releases functionality in Github and updated in the main 
Flagsmith repository. 
