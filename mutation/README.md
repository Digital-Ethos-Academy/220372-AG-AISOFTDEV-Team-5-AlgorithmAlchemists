# Mutation Testing Container

This directory provides an isolated Docker-based runner for mutation testing using `mutmut`.

## Files
- `Dockerfile`: Builds a minimal Python 3.11 image with project dependencies and mutmut.
- `docker_entrypoint.sh`: Runs baseline tests, then mutation tests, and enforces that no mutants survive.
- `mutmut_results.txt`: Generated after a run with the summary.

## Usage
From repository root:

```bash
# Build the image
docker build -f mutation/Dockerfile -t mutation-test .

# Run mutation testing (mounts source read/write for result output)
docker run --rm \
  -v "$(pwd):/workspace" \
  -w /workspace \
  -e OPENAI_API_KEY=dummy \
  -e ANTHROPIC_API_KEY=dummy \
  -e HUGGINGFACE_API_KEY=dummy \
  -e TAVILY_API_KEY=dummy \
  -e GOOGLE_API_KEY=dummy \
  mutation-test
```

If any mutants survive the container exits with code 2.

## Notes
- Environment variables are set to placeholder values to satisfy validation; never store secrets here.
- Adjust `paths_to_mutate` in `setup.cfg` if project layout changes.
- Add exclusions via `setup.cfg` `[mutmut]` section (e.g., `exclude=app/__init__.py`).
