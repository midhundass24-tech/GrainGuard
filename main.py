import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ============================================================
# SETUP
# ============================================================

import re

load_dotenv()

def load_all_gemini_keys():
    keys = []
    single = os.getenv("GEMINI_API_KEY", "").strip()
    if single:
        for k in single.split(","):
            k_clean = k.strip()
            if k_clean and k_clean not in keys:
                keys.append(k_clean)

    env_matches = []
    for k in os.environ.keys():
        if k.startswith("GEMINI_API_KEY_") or k.startswith("GEMINI_KEY_"):
            num_match = re.search(r'\d+', k)
            idx = int(num_match.group()) if num_match else 999
            env_matches.append((idx, k))

    env_matches.sort(key=lambda x: (x[0], x[1]))
    for _, k in env_matches:
        val = os.getenv(k, "").strip()
        if val and val not in keys:
            keys.append(val)

    return keys

API_KEYS = load_all_gemini_keys()

if not API_KEYS:
    raise RuntimeError(
        "No Gemini API keys were found in .env"
    )

current_key_index = 0


def get_client():
    return genai.Client(
        api_key=API_KEYS[current_key_index]
    )

# This is the model that already worked in your test.
MODEL = "gemini-3.7-flash"

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def read_file(path):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return path.read_text(encoding="utf-8")


def save_output(filename, content):
    path = OUTPUT_DIR / filename
    path.write_text(content, encoding="utf-8")

    print(f"✅ Saved: {path}")


def ask_gemini(prompt, round_name):

    global current_key_index

    print()
    print("=" * 60)
    print(f"🤖 {round_name}")
    print("=" * 60)

    attempts = len(API_KEYS)

    for attempt in range(attempts):

        print(
            f"Using Gemini API key "
            f"{current_key_index + 1}/{len(API_KEYS)}..."
        )

        try:

            client = get_client()

            response = client.interactions.create(
                model=MODEL,
                input=prompt
            )

            result = response.output_text

            if not result:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            print(f"✅ {round_name} completed!")

            return result

        except Exception as error:

            error_text = str(error).lower()

            # Likely quota/rate-limit error
            quota_error = (
                "429" in error_text
                or "quota" in error_text
                or "rate limit" in error_text
                or "resource exhausted" in error_text
            )

            if not quota_error:
                raise

            print()
            print(
                f"⚠️ API key {current_key_index + 1} "
                "appears to be out of quota/rate limited."
            )

            if current_key_index >= len(API_KEYS) - 1:
                raise RuntimeError(
                    "❌ All Gemini API keys have been exhausted "
                    "or rate limited."
                )

            current_key_index += 1

            print(
                f"🔄 Switching to API key "
                f"{current_key_index + 1}..."
            )

    raise RuntimeError("All Gemini API keys failed.")

# ============================================================
# LOAD FINAL PROMPT
# ============================================================

PROMPT_FILE = INPUT_DIR / "final_prompt.txt"

FINAL_PROMPT = read_file(PROMPT_FILE)


# ============================================================
# ROUND 1 — ARCHITECTURE
# ============================================================

def round_1():

    prompt = f"""
You are the lead software architect for a hackathon project.

Here is the implementation specification:

================ SPECIFICATION ================

{FINAL_PROMPT}

=================================================

ROUND 1 — ARCHITECTURE

Design a realistic architecture for this project.

Provide:

1. Project overview
2. Target users
3. User workflow
4. System architecture
5. Frontend architecture
6. Backend architecture
7. Database architecture
8. AI architecture
9. API endpoints
10. External services
11. Authentication requirements
12. Project folder structure
13. Data flow
14. Security considerations
15. Error handling
16. Deployment approach
17. MVP features
18. Features that should NOT be built
19. Recommended technology stack
20. Technical risks

Prioritize a working hackathon MVP.

Do not write the full application code.

Finally provide:

IMPLEMENTATION PLAN

Give a numbered implementation plan for the developers.
"""

    result = ask_gemini(
        prompt,
        "ROUND 1 — ARCHITECTURE"
    )

    save_output(
        "round1_architecture.md",
        result
    )

    return result


# ============================================================
# ROUND 2 — BACKEND
# ============================================================

def round_2(architecture):

    prompt = f"""
You are the backend engineer for a hackathon project.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE:

{architecture}


ROUND 2 — BACKEND

Design and implement the backend.

First explain:

1. Backend technology
2. Dependencies
3. Backend folder structure
4. Database schema
5. Database models
6. API endpoints
7. Request formats
8. Response formats
9. Environment variables
10. Authentication
11. Error handling
12. AI/API integration

Then provide the backend implementation.

For every file use this format:

FILE: path/to/file.ext

Then provide the complete file contents.

Rules:

- Do not omit important code.
- Do not write "rest of code here".
- Do not use fake placeholder implementations.
- Keep the project realistic for a hackathon.
- Make the API usable by the frontend.
- Explain setup commands at the end.
"""

    result = ask_gemini(
        prompt,
        "ROUND 2 — BACKEND"
    )

    save_output(
        "round2_backend.md",
        result
    )

    return result


# ============================================================
# ROUND 3 — FRONTEND
# ============================================================

def round_3(architecture, backend):

    prompt = f"""
You are the frontend engineer for a hackathon project.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE:

{architecture}


BACKEND DESIGN:

{backend}


ROUND 3 — FRONTEND

Design and implement the frontend.

The frontend should be:

- Modern
- Clean
- Responsive
- Easy to use
- Suitable for a hackathon demo

First explain:

1. Frontend technology
2. Pages
3. Components
4. State management
5. API communication
6. User flow
7. Folder structure

Then provide the frontend implementation.

For every file use:

FILE: path/to/file.ext

Then provide the complete contents.

Rules:

- Do not omit important code.
- Do not use fake placeholder code.
- Match the backend API.
- Keep the implementation realistic.
- Avoid unnecessary frameworks.

At the end provide frontend installation and run commands.
"""

    result = ask_gemini(
        prompt,
        "ROUND 3 — FRONTEND"
    )

    save_output(
        "round3_frontend.md",
        result
    )

    return result


# ============================================================
# ROUND 4 — INTEGRATION
# ============================================================

def round_4(architecture, backend, frontend):

    prompt = f"""
You are a senior software integration engineer.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE:

{architecture}


BACKEND:

{backend}


FRONTEND:

{frontend}


ROUND 4 — INTEGRATION

Check whether all parts of the system can work together.

Check:

1. Frontend/backend communication
2. API URLs
3. Request formats
4. Response formats
5. Database interactions
6. Authentication
7. Environment variables
8. CORS
9. AI/API integration
10. Error handling
11. Dependencies
12. Data flow
13. File paths
14. Potential integration failures

Identify problems and provide exact fixes.

For changed files use:

FILE: path/to/file.ext

Then provide the complete corrected file.

Do not redesign working parts unnecessarily.

Finally provide:

FULL STARTUP PROCEDURE

and

MANUAL DEMO PROCEDURE
"""

    result = ask_gemini(
        prompt,
        "ROUND 4 — INTEGRATION"
    )

    save_output(
        "round4_integration.md",
        result
    )

    return result


# ============================================================
# ROUND 5 — TESTING
# ============================================================

def round_5(
    architecture,
    backend,
    frontend,
    integration
):

    prompt = f"""
You are the QA engineer for a hackathon project.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE:

{architecture}


BACKEND:

{backend}


FRONTEND:

{frontend}


INTEGRATION:

{integration}


ROUND 5 — TESTING AND DEBUGGING

Perform a serious technical audit.

Look for:

1. Logic bugs
2. Broken imports
3. API failures
4. Database errors
5. Input validation problems
6. Authentication problems
7. Security issues
8. Dependency issues
9. Frontend bugs
10. Backend bugs
11. AI/API failures
12. Empty responses
13. Network failures
14. Environment problems
15. Deployment problems
16. Performance problems

Classify problems as:

CRITICAL
MEDIUM
LOW

Then create:

1. Testing strategy
2. Test cases
3. Edge cases
4. Bug fixes
5. Final test checklist

For important fixes provide:

FILE: path/to/file.ext

Then provide the complete corrected file.

Do not rewrite code unnecessarily.
"""

    result = ask_gemini(
        prompt,
        "ROUND 5 — TESTING"
    )

    save_output(
        "round5_testing.md",
        result
    )

    return result


# ============================================================
# ROUND 6 — FINAL HACKATHON POLISH
# ============================================================

def round_6(
    architecture,
    backend,
    frontend,
    integration,
    testing
):

    prompt = f"""
You are the final senior engineer and hackathon mentor.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE:

{architecture}


BACKEND:

{backend}


FRONTEND:

{frontend}


INTEGRATION:

{integration}


TESTING:

{testing}


ROUND 6 — FINAL HACKATHON POLISH

Prepare the project for the final demonstration.

Focus on:

1. Reliability
2. Demo stability
3. User experience
4. Visual polish
5. Performance
6. AI functionality
7. Error recovery
8. Judge understanding
9. Easy startup
10. Professional presentation

Identify the 3–5 highest-value improvements.

For each improvement explain:

- Why it matters
- Expected impact
- Difficulty
- Whether it should be implemented before the hackathon

Provide exact code changes when needed.

For changed files use:

FILE: path/to/file.ext

Then provide the complete corrected file.

Finally provide:

DEMO SCRIPT

Create a 3–5 minute demonstration.

Also provide:

JUDGE PITCH

Cover:

- Problem
- Solution
- Innovation
- Technology
- Impact

Finally provide:

FINAL PRE-DEMO CHECKLIST
"""

    result = ask_gemini(
        prompt,
        "ROUND 6 — FINAL POLISH"
    )

    save_output(
        "round6_final_polish.md",
        result
    )

    return result


# ============================================================
# RUN EVERYTHING
# ============================================================

def main():

    print()
    print("=" * 60)
    print("🚀 HACKATHON GEMINI PIPELINE")
    print("=" * 60)
    print()
    print(f"Model: {MODEL}")
    print(f"Input: {PROMPT_FILE}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    print("Starting 6 rounds...")
    print()

    # Round 1
    architecture = round_1()

    # Round 2
    backend = round_2(architecture)

    # Round 3
    frontend = round_3(
        architecture,
        backend
    )

    # Round 4
    integration = round_4(
        architecture,
        backend,
        frontend
    )

    # Round 5
    testing = round_5(
        architecture,
        backend,
        frontend,
        integration
    )

    # Round 6
    final_polish = round_6(
        architecture,
        backend,
        frontend,
        integration,
        testing
    )

    print()
    print("=" * 60)
    print("🎉 ALL 6 ROUNDS COMPLETED!")
    print("=" * 60)
    print()
    print("Check the outputs folder:")
    print()
    print("1. round1_architecture.md")
    print("2. round2_backend.md")
    print("3. round3_frontend.md")
    print("4. round4_integration.md")
    print("5. round5_testing.md")
    print("6. round6_final_polish.md")
    print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()