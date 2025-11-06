#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-mutation-test}
TAG=${TAG:-latest}

# Compute project root (POSIX style)
PROJECT_ROOT_POSIX="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Derive a Windows path if on Git Bash / MSYS for volume mounting
if command -v cygpath >/dev/null 2>&1; then
  PROJECT_ROOT_WIN="$(cygpath -m "${PROJECT_ROOT_POSIX}")"
else
  # Attempt pwd -W (Git Bash) fallback; if it fails just reuse POSIX path
  PROJECT_ROOT_WIN="$( (cd "${PROJECT_ROOT_POSIX}" && pwd -W) 2>/dev/null || echo "${PROJECT_ROOT_POSIX}" )"
fi

# Always prefer POSIX style mount path to avoid Windows path leakage inside container/mutmut
HOST_MOUNT_PATH="${PROJECT_ROOT_POSIX}"

# Optional debug flag
if [[ "${DEBUG_DOCKER_MUTATION:-0}" == "1" ]]; then
  echo "[debug] PROJECT_ROOT_POSIX=${PROJECT_ROOT_POSIX}"
  echo "[debug] PROJECT_ROOT_WIN=${PROJECT_ROOT_WIN}"
  echo "[debug] HOST_MOUNT_PATH=${HOST_MOUNT_PATH}"
fi

if [[ ! -d "${PROJECT_ROOT_POSIX}" ]]; then
  echo "[error] Resolved project root does not exist: ${PROJECT_ROOT_POSIX}" >&2
  exit 2
fi

pushd "${PROJECT_ROOT_POSIX}" >/dev/null

echo "[run-mutation] Building image ${IMAGE_NAME}:${TAG}..."
docker build -f mutation/Dockerfile -t "${IMAGE_NAME}:${TAG}" .

echo "[run-mutation] Running mutation tests in container..."

# Prevent MSYS from rewriting docker arguments (mount/paths)
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'

set +e
docker run --rm \
  -v "${HOST_MOUNT_PATH}:/workspace" \
  -e PYTHONPATH=/workspace \
  -e OPENAI_API_KEY=dummy \
  -e ANTHROPIC_API_KEY=dummy \
  -e HUGGINGFACE_API_KEY=dummy \
  -e TAVILY_API_KEY=dummy \
  -e GOOGLE_API_KEY=dummy \
  "${IMAGE_NAME}:${TAG}" "$@"
STATUS=$?
set -e

if [[ ${STATUS} -ne 0 ]]; then
  echo "[warn] Container exited with status ${STATUS}" >&2
fi

if [ -f mutation/mutmut_results.txt ]; then
  echo "[run-mutation] Summary (mutation/mutmut_results.txt):"
  sed -n '1,50p' mutation/mutmut_results.txt
else
  echo "[info] No mutation results file found (mutation/mutmut_results.txt) yet."
fi

popd >/dev/null

exit ${STATUS}
