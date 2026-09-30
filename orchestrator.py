#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent

PRODUCT_ARCH = REPO_ROOT / "docs" / "matrix_v1_architecture"
AI_ARCH = REPO_ROOT / "docs" / "matrix_AI_development_architecture"
STATE_DIR = REPO_ROOT / ".ai"
TASKS_FILE = STATE_DIR / "TASKS.json"

REQUIRED_STATE_FILES = [
    "TASKS.json",
    "PROJECT_STATE.md",
    "DECISIONS.md",
    "BLOCKERS.md",
    "TEST_STATUS.md",
    "DEPLOYMENT_STATUS.md",
    "RESOURCE_STATUS.md",
]

REQUIRED_PRODUCT_FILES = [
    "README.md",
    "11_IMPLEMENTATION_ORDER.md",
    "12_ARCHITECTURE_DECISIONS.md",
]

REQUIRED_AI_FILES = [
    "AGENTS.md",
    "01_ORCHESTRATION_MODEL.md",
    "02_TASK_PLANNING_PROTOCOL.md",
    "06_HUMAN_APPROVAL_POLICY.md",
    "07_PERSISTENT_STATE.md",
    "08_RESOURCE_GUARDRAILS.md",
    "11_AUTONOMOUS_EXECUTION_LOOP.md",
    "12_BOOTSTRAP_AND_HANDOFF.md",
]


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Git command failed")

    return result.stdout.strip()


def check_files(base, names):
    missing = []

    for name in names:
        if not (base / name).is_file():
            missing.append(str(base / name))

    return missing


def disk_status():
    usage = shutil.disk_usage(REPO_ROOT)
    free = usage.free

    gib = 1024 ** 3
    mib = 1024 ** 2

    if free > 1.5 * gib:
        level = "healthy"
    elif free >= 750 * mib:
        level = "warning"
    else:
        level = "critical"

    return free / gib, level


def load_tasks():
    try:
        data = json.loads(TASKS_FILE.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to load TASKS.json: {exc}") from exc

    if data.get("schema_version") != 1:
        raise RuntimeError("TASKS.json schema_version must be 1")

    if data.get("project") != "MATRIX":
        raise RuntimeError('TASKS.json project must be "MATRIX"')

    if not isinstance(data.get("tasks"), list):
        raise RuntimeError("TASKS.json tasks must be a list")

    return data


def main():
    print("MATRIX Orchestrator Bootstrap")
    print("=============================")
    print("Mode: DRY RUN")
    print("No tasks, files, branches, or state will be modified.")
    print()

    failures = []

    # 1. Git repository
    try:
        git_root = Path(git("rev-parse", "--show-toplevel")).resolve()

        if git_root != REPO_ROOT.resolve():
            failures.append(
                f"Git root mismatch: expected {REPO_ROOT}, got {git_root}"
            )
        else:
            print("[OK] Git repository detected")
    except Exception as exc:
        failures.append(f"Git repository check failed: {exc}")

    # 2. Architecture
    missing = []
    missing.extend(check_files(PRODUCT_ARCH, REQUIRED_PRODUCT_FILES))
    missing.extend(check_files(AI_ARCH, REQUIRED_AI_FILES))

    if missing:
        failures.extend(f"Missing architecture file: {path}" for path in missing)
    else:
        print("[OK] Product architecture detected")
        print("[OK] AI development architecture detected")

    # 3. Persistent state
    state_missing = check_files(STATE_DIR, REQUIRED_STATE_FILES)

    if state_missing:
        failures.extend(
            f"Missing state file: {path}" for path in state_missing
        )
    else:
        print("[OK] Persistent .ai state detected")

    # 4. TASKS.json
    tasks = None

    try:
        tasks = load_tasks()
        print("[OK] TASKS.json schema valid")
    except Exception as exc:
        failures.append(str(exc))

    # 5. Git branch and working tree
    try:
        branch = git("branch", "--show-current") or "(detached HEAD)"
        status = git("status", "--porcelain")

        print(f"[INFO] Git branch: {branch}")

        if status:
            print("[INFO] Working tree contains uncommitted changes:")
            for line in status.splitlines():
                print(f"       {line}")
        else:
            print("[OK] Working tree clean")
    except Exception as exc:
        failures.append(f"Git state check failed: {exc}")

    # 6. Disk resources
    try:
        free_gib, level = disk_status()
        print(f"[INFO] Free disk: {free_gib:.2f} GiB")
        print(f"[INFO] Resource level: {level}")

        if level == "critical":
            failures.append(
                "Disk is below the architecture critical threshold of 750 MB."
            )
    except Exception as exc:
        failures.append(f"Resource check failed: {exc}")

    # 7. Task bootstrap state
    if tasks is not None:
        task_count = len(tasks["tasks"])
        print(f"[INFO] Persisted tasks: {task_count}")

        if task_count == 0:
            print("[READY] Initial Planner bootstrap is required.")
            print(
                "[NEXT] Planner should create the initial V1 task DAG and "
                "validate it against "
                "docs/matrix_v1_architecture/11_IMPLEMENTATION_ORDER.md"
            )
        else:
            print("[INFO] Existing task ledger detected.")

    print()

    if failures:
        print("BOOTSTRAP VALIDATION: FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("BOOTSTRAP VALIDATION: PASSED")
    print("Dry-run completed with no state changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
