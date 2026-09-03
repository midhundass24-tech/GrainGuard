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
    raise RuntimeError("No Gemini API keys found in .env")

current_key_index = 0

MODEL = "gemini-3.6-flash"

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(prompt, round_name):

    global current_key_index

    for attempt in range(len(API_KEYS)):

        print()
        print("=" * 60)
        print(f"🤖 {round_name}")
        print("=" * 60)
        print(
            f"Using API key {current_key_index + 1}/"
            f"{len(API_KEYS)}..."
        )

        try:

            client = genai.Client(
                api_key=API_KEYS[current_key_index]
            )

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

            quota_error = (
                "429" in error_text
                or "quota" in error_text
                or "rate limit" in error_text
                or "resource exhausted" in error_text
            )

            if not quota_error:
                raise

            print(
                f"⚠️ API key {current_key_index + 1} "
                "is unavailable/quota limited."
            )

            if current_key_index == len(API_KEYS) - 1:
                raise RuntimeError(
                    "❌ All Gemini API keys are exhausted."
                )

            current_key_index += 1

            print(
                f"🔄 Switching to API key "
                f"{current_key_index + 1}..."
            )

    raise RuntimeError("All Gemini API keys failed.")


# ============================================================
# FILE HELPERS
# ============================================================

def read_output(filename):

    path = OUTPUT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Missing previous output: {path}"
        )

    return path.read_text(encoding="utf-8")


def save_output(filename, content):

    path = OUTPUT_DIR / filename

    path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"💾 Saved → {path}")


# ============================================================
# LOAD EXISTING ROUND 1 + ROUND 2
# ============================================================

FINAL_PROMPT = (
    INPUT_DIR / "final_prompt.txt"
).read_text(encoding="utf-8")

architecture = read_output(
    "round1_architecture.md"
)

backend = read_output(
    "round2_backend.md"
)

print()
print("=" * 60)
print("🔄 RESUMING FROM ROUND 3")
print("=" * 60)
print("✅ Round 1 loaded")
print("✅ Round 2 loaded")
print("➡️ Starting Round 3")
print()


# ============================================================
# ROUND 3 — FRONTEND
# ============================================================

round3_prompt = f"""
You are the frontend engineer for a hackathon project.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE FROM ROUND 1:

{architecture}


BACKEND FROM ROUND 2:

{backend}


ROUND 3 — FRONTEND IMPLEMENTATION

Design and implement the frontend for the project.

The frontend should be:

- Modern
- Clean
- Responsive
- Easy to use
- Suitable for a hackathon demonstration

First explain:

1. Frontend technology
2. Pages
3. Components
4. State management
5. API communication
6. User flow
7. Frontend folder structure

Then provide the frontend implementation.

For every file use:

FILE: path/to/file.ext

Then provide the COMPLETE contents of that file.

Rules:

- Do not omit important code.
- Do not use fake placeholder code.
- Match the backend API exactly.
- Keep the implementation realistic.
- Avoid unnecessary frameworks.

At the end provide:

FRONTEND SETUP COMMANDS

and

FRONTEND RUN COMMANDS.
"""

frontend = ask_gemini(
    round3_prompt,
    "ROUND 3 — FRONTEND"
)

save_output(
    "round3_frontend.md",
    frontend
)


# ============================================================
# ROUND 4 — INTEGRATION
# ============================================================

round4_prompt = f"""
You are a senior software integration engineer.

ORIGINAL SPECIFICATION:

{FINAL_PROMPT}


ARCHITECTURE:

{architecture}


BACKEND:

{backend}


FRONTEND:

{frontend}


ROUND 4 — FULL SYSTEM INTEGRATION

Check whether all parts of the system work together.

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
14. Integration failures

Identify problems and provide exact fixes.

For changed files use:

FILE: path/to/file.ext

Then provide the COMPLETE corrected file.

Do not redesign working parts unnecessarily.

At the end provide:

FULL SYSTEM STARTUP STEPS

and

MANUAL DEMO STEPS.
"""

integration = ask_gemini(
    round4_prompt,
    "ROUND 4 — INTEGRATION"
)

save_output(
    "round4_integration.md",
    integration
)


# ============================================================
# ROUND 5 — TESTING
# ============================================================

round5_prompt = f"""
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

Then provide the COMPLETE corrected file.

Do not rewrite working code unnecessarily.
"""

testing = ask_gemini(
    round5_prompt,
    "ROUND 5 — TESTING"
)

save_output(
    "round5_testing.md",
    testing
)


# ============================================================
# ROUND 6 — FINAL POLISH
# ============================================================

round6_prompt = f"""
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

Then provide the COMPLETE corrected file.

Do not introduce unnecessary frameworks or major
architectural changes.

Finally provide:

DEMO SCRIPT

Create a 3–5 minute demonstration sequence.

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

final_polish = ask_gemini(
    round6_prompt,
    "ROUND 6 — FINAL POLISH"
)

save_output(
    "round6_final_polish.md",
    final_polish
)


# ============================================================
# DONE
# ============================================================

print()
print("=" * 60)
print("🎉 ROUNDS 3–6 COMPLETED!")
print("=" * 60)
print()
print("Your outputs are:")
print("  ✅ round1_architecture.md  (already existed)")
print("  ✅ round2_backend.md       (already existed)")
print("  ✅ round3_frontend.md")
print("  ✅ round4_integration.md")
print("  ✅ round5_testing.md")
print("  ✅ round6_final_polish.md")
print()