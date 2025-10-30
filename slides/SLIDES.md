# SEN4013 V&V Project Presentation
## Flask Todo App Verification & Validation

**Team:** [Your Names]
**Date:** January 16, 2026
**Duration:** 5 minutes per person (adjust based on team size)

---

## Slide 1: Title Slide

**Title:** Software Verification & Validation of a Flask Todo Application

**Subtitle:** Comprehensive Testing with Functional, Property-Based, Formal, and UI/E2E Methods

**Team Members:**
- [Name 1]
- [Name 2]
- [Name 3]
- [Name 4]

**Date:** January 16, 2026

**Speaker Notes:**
"Good [morning/afternoon]. Our team conducted a comprehensive V&V study on a Flask-based todo application. We applied six different testing techniques to build confidence in the software's correctness, covering functional tests, property-based tests, runtime contracts, formal verification, and end-to-end UI testing. This presentation summarizes our approach, findings, and recommendations."

---

## Slide 2: What is Verification & Validation?

**Content:**
- **Verification:** "Are we building the product right?"
  - Does the software conform to its specification?
  - Checks correctness of implementation

- **Validation:** "Are we building the right product?"
  - Does the software meet user needs and expectations?
  - Checks fitness for purpose

- **Why Automate V&V?**
  - Higher confidence through repeatability
  - Catch defects early (lower cost)
  - Enable continuous integration/deployment
  - Provide auditable evidence of quality

**Visual:** Two-column comparison or flowchart showing Verification vs Validation

**Speaker Notes:**
"Verification asks 'are we building the product right?' — does our code match the spec? Validation asks 'are we building the right product?' — does it solve the user's problem? Automating V&V gives us repeatable evidence of quality, catches bugs early when they're cheap to fix, and supports modern CI/CD practices. In this project, we focused primarily on verification but also validated UI behavior against typical user expectations."

---

## Slide 3: System Under Test

**Content:**
**Flask Todo Application**
- Web UI for task management (add, edit, complete, delete)
- REST API at `/api/todos` (CRUD operations)
- Interactive Swagger documentation at `/apidocs`
- SQLite database for persistence

**Tech Stack:**
- Flask 1.1.1 + Flask-SQLAlchemy 2.4.1
- Flasgger (Swagger/OpenAPI)
- Python 3.12

**Why This App?**
- Real-world structure (UI + API + database)
- Multiple test surfaces (web forms, REST endpoints, database)
- Well-documented via Swagger

**Source:** https://github.com/onurtacc/flask-todo-app

**Visual:** Screenshot of the app UI or architecture diagram

**Speaker Notes:**
"Our system under test is a Flask-based todo list application. It exposes both a web UI for human users and a REST API for programmatic access, with interactive Swagger docs at /apidocs. It uses SQLite for data storage. We chose this app because it represents a realistic microservice with multiple interfaces to test, and the Swagger documentation provided a clear API contract to verify against."

---

## Slide 4: V&V Toolchain

**Content:**

| Tool | Purpose | Why We Used It |
|------|---------|----------------|
| **pytest** | Unit/functional testing | Industry standard, simple assertions, automatic discovery |
| **Hypothesis** | Property-based testing | Auto-generates edge cases, finds bugs humans miss |
| **coverage.py** | Code coverage analysis | Measures which code paths are tested (67% achieved) |
| **Playwright** | UI/E2E testing | Automates real browsers, captures screenshots for evidence |
| **icontract** | Runtime contracts | Enforces preconditions/postconditions at runtime |
| **CrossHair** | Formal verification | Uses SMT solver to prove contracts hold for all inputs |

**Visual:** Icons or logos of each tool

**Speaker Notes:**
"We assembled a toolchain that covers multiple dimensions of quality. Pytest handles functional tests with simple assertions. Hypothesis generates hundreds of edge-case inputs automatically—like fuzzing with structure. Coverage.py measures how much code we exercised. Playwright drives a real browser for UI tests and captures screenshots. Icontract lets us write executable specifications as contracts. CrossHair uses a theorem prover to search for contract violations we might have missed. Together, these tools provide complementary evidence of correctness."

---

## Slide 5: Test Strategy & Approach

**Content:**

**Our Testing Strategy:**
1. **Functional Tests** — Verify typical CRUD workflows via API
2. **Property-Based Tests** — Use Hypothesis to generate 100+ inputs matching regex patterns
3. **Negative Tests** — Check error handling (empty titles, oversized titles)
4. **UI/E2E Tests** — Automate browser to add a todo, capture screenshot
5. **Structural Coverage** — Measure code paths exercised (target: 70%+)
6. **Contract Enforcement** — Define business rules as code, check at runtime
7. **Formal Verification** — Use symbolic execution to prove contract properties

**Test Execution:**
- All tests automated and repeatable
- Run via `pytest` command
- Artifacts: coverage XML, JUnit XML, screenshots

**Speaker Notes:**
"Our strategy covered the full testing pyramid. At the base, we have unit and functional tests checking individual API endpoints. Above that, property-based tests generated diverse inputs to stress edge cases. We also tested error paths—what happens when users send bad data. At the top, UI tests validate the complete user journey through a real browser. We also layered in structural coverage to find untested code, and formal methods to mathematically verify business rules. Everything is automated—one command runs the entire suite and generates reports."

---

## Slide 6: Functional Tests

**Content:**

**Test Cases:**
- ✅ T01: Home UI loads (HTTP 200)
- ✅ T02: Create todo via API, verify it appears in list
- ✅ T03: Reject empty title (HTTP 400)

**Example Test (pytest):**
```python
def test_home_ui_loads(client):
    r = client.get("/")
    assert r.status_code == 200
```

**Results:**
- 3/3 functional tests passed
- Verified core CRUD operations
- Confirmed error handling for empty titles

**Speaker Notes:**
"We started with functional tests covering the happy paths: loading the UI, creating a todo via the API, and listing todos. We also tested a negative case—sending an empty title—and confirmed the API rejects it with HTTP 400. These tests are straightforward but essential. They verify that basic workflows function as expected and that the API follows good HTTP semantics. All three passed."

---

## Slide 7: Property-Based Tests (Hypothesis)

**Content:**

**What is Property-Based Testing?**
- Instead of writing individual test cases, define **properties** (rules) the system must satisfy
- Hypothesis generates hundreds of inputs automatically
- If a property fails, Hypothesis shrinks the input to the minimal failing case

**Our Property:**
"For any valid title (1-40 chars, alphanumeric + punctuation), POST should succeed and GET should return it"

**Test Code:**
```python
@given(
    title=st.from_regex(r"[A-Za-z0-9 ,.!?-]{1,40}", fullmatch=True),
    desc=st.from_regex(r"[A-Za-z0-9 ,.!?-]{0,120}", fullmatch=True) | st.none()
)
def test_create_list_roundtrip(client, title, desc):
    r = client.post("/api/todos", json={"title": title, "description": desc})
    assert r.status_code in (200, 201)
    r = client.get("/api/todos")
    assert any(item["title"] == title for item in r.get_json())
```

**Results:**
- ✅ 100+ generated test cases passed
- Covered edge cases: single-char titles, max-length titles, special characters

**Speaker Notes:**
"Property-based testing is a powerful technique. Instead of writing 'test with title equals hello', we say 'for ANY title matching this pattern, the system should behave correctly.' Hypothesis then generates hundreds of examples: single-letter titles, max-length titles, titles with punctuation, etc. Our test ran 100+ cases and all passed. This gives us much stronger confidence than hand-written examples—Hypothesis often finds edge cases humans wouldn't think of."

---

## Slide 8: Runtime Contracts (icontract)

**Content:**

**What are Contracts?**
- Formal specifications attached to functions
- **Preconditions:** Must be true before function executes
- **Postconditions:** Must be true after function executes
- Fail fast if violated (better than silent corruption)

**Our Contract: `normalize_title`**
```python
@require(lambda title: isinstance(title, str))
@require(lambda title: 1 <= len(title.strip()) <= 40)
@ensure(lambda title, result: result == title.strip())
def normalize_title(title: str) -> str:
    return title.strip()
```

**What This Guarantees:**
- Input must be a string
- After trimming, must be 1-40 chars
- Output is exactly the trimmed input

**Results:**
- ✅ Contract test passed
- Enforces business rule: "titles must be 1-40 characters after normalization"

**Speaker Notes:**
"Contracts are executable specifications. The 'require' decorators define preconditions—what must be true before the function runs. The 'ensure' decorator defines postconditions—what must be true after. If a contract is violated, the program crashes immediately with a clear error, rather than silently producing bad data. Our normalize_title function enforces the business rule that titles must be 1-40 characters after trimming whitespace. This contract ran successfully in all tests, proving the function behaves correctly within its specified domain."

---

## Slide 9: Formal Verification (CrossHair)

**Content:**

**What is Formal Verification?**
- Uses mathematical techniques to **prove** properties hold for all possible inputs
- CrossHair uses symbolic execution + SMT (Satisfiability Modulo Theories) solver
- Searches for **counterexamples** that violate contracts

**How It Works:**
1. CrossHair reads the `@require` and `@ensure` decorators
2. Symbolically executes the function with all possible inputs
3. Uses Z3 theorem prover to find inputs that violate contracts
4. If none found → proven correct within contract bounds

**Command:**
```bash
crosshair check domain_contracts.py
```

**Result:**
```
(no output = success)
```

**Interpretation:**
- ✅ No counterexamples found
- The `normalize_title` function provably satisfies its contracts for all valid inputs
- Formal guarantee, not just tested examples

**Visual:** Diagram showing symbolic execution tree

**Speaker Notes:**
"Formal verification goes beyond testing by mathematically proving correctness. CrossHair uses symbolic execution—it doesn't run the function with concrete values, but with symbolic 'any string' inputs. It then uses a theorem prover called Z3 to search for inputs that would violate the contracts. If it finds one, it reports a counterexample. If it doesn't, that's a proof the function is correct within its contract bounds. When we ran CrossHair on our normalize_title function, it found no counterexamples, meaning we have a formal guarantee the function works correctly for all inputs satisfying the preconditions. This is stronger evidence than testing could ever provide."

---

## Slide 10: Structural Coverage Analysis

**Content:**

**Coverage Results:**
```
Name                           Stmts   Miss  Cover
----------------------------------------------------
app.py                            95     45    53%
tests/*                           35      0   100%
domain_contracts.py                6      0   100%
----------------------------------------------------
TOTAL                            136     45    67%
```

**What Was Covered:**
- ✅ API create and list endpoints
- ✅ Home UI route
- ✅ Error handling for empty titles
- ✅ All test code and contracts

**What Was NOT Covered:**
- ❌ Web form handlers (add, edit, delete via UI)
- ❌ API endpoints: GET by ID, PUT, DELETE
- ❌ Some error paths in validation logic

**Interpretation:**
- 67% coverage is acceptable for initial V&V
- Gaps indicate where additional tests are needed
- Test code at 100% coverage (good practice)

**Visual:** Bar chart or pie chart showing 67% coverage

**Speaker Notes:**
"Coverage measures which lines of code were executed during testing. We achieved 67% overall coverage, with 53% of the application code and 100% of our test code. The covered portions include the API endpoints we tested—create and list—plus error handling for empty titles. The uncovered 33% includes web form handlers and remaining API endpoints like update and delete. This coverage report tells us where our testing is strong and where we have gaps. It's not about hitting 100%—that's often wasteful—but about understanding what's tested and making deliberate decisions about what's not."

---

## Slide 11: UI/E2E Testing (Playwright)

**Content:**

**What is E2E Testing?**
- Tests the entire system through the user interface
- Uses a real browser (Chromium, Firefox, or WebKit)
- Simulates user actions: navigate, type, click, submit
- Captures screenshots as visual evidence

**Our Test:**
1. Launch browser
2. Navigate to http://127.0.0.1:5000
3. Fill form: title="Buy milk", description="2L semi-skimmed"
4. Click "Add" button
5. Verify "Buy milk" appears in page content
6. Capture screenshot to `artifacts/ui_after_add.png`

**Result:**
- ✅ Test passed
- Todo successfully added via UI
- Screenshot captured

**Visual:** Show the screenshot from `artifacts/ui_after_add.png`

**Speaker Notes:**
"End-to-end testing validates the complete user journey through a real browser. We used Playwright to automate Chromium: it opens the app, fills in the form with 'Buy milk', clicks Add, and verifies the todo appears. This tests not just the backend logic but also the HTML templates, JavaScript, form handling, and database round-trip. The screenshot we captured is proof the UI worked correctly. This is the closest our automated tests get to how a real user experiences the application."

---

## Slide 12: Incidents & Findings

**Content:**

**Incident INC-001: Missing Title Length Validation** 🔴

**Severity:** Medium
**Status:** Unresolved

**Problem:**
- API accepts arbitrarily long titles (tested with 200 chars)
- Database schema defines `String(100)`, suggesting 100-char limit
- No validation enforces this limit in application code
- Result: Silent truncation or unexpected behavior

**Test Case:** T04 (Excessive Title Length)
- Expected: HTTP 400 with error message
- Actual: HTTP 201 Created

**Impact:**
- Data integrity: Silent data loss
- User experience: No feedback on invalid input
- Security: Potential for exploitation if database layer doesn't handle overflow gracefully

**Recommendation:**
Add validation at [app.py:152](app.py#L152):
```python
if len(title) > 100:
    return jsonify({"error": "Title must be 100 characters or less"}), 400
```

**Speaker Notes:**
"Our testing uncovered one significant defect. The API accepts titles of any length, but the database schema limits titles to 100 characters. This mismatch means the application silently truncates long titles or—depending on the database—could cause errors. A user trying to add a 200-character title gets an HTTP 201 success response, but their title is cut off. We classified this as medium severity: it causes data loss and poor user experience, but it's not a critical crash or security vulnerability. The fix is simple—add a length check before creating the todo. This finding demonstrates the value of negative testing: we didn't just test happy paths, we tested what happens when users send unexpected data."

---

## Slide 13: Recommendations

**Content:**

**Immediate Actions:**
1. ✅ Fix INC-001: Add title length validation (5 minutes)
2. 📈 Expand test coverage to 80%+ (test remaining API endpoints)
3. 🧪 Enhance property tests (Unicode, emoji, SQL injection patterns)

**Process Improvements:**
4. 🔄 **CI/CD Integration:** Run tests on every commit
   ```yaml
   - pytest --cov --junitxml=junit.xml
   - coverage xml
   - crosshair check domain_contracts.py
   ```
5. 📝 **Contract-Driven Development:** Add contracts to all API endpoints
6. 🔍 **Mutation Testing:** Use `mutmut` to verify tests catch bugs

**Long-Term Strategy:**
7. 🎯 **Fuzzing:** Apply `atheris` to find crash-inducing inputs
8. 🗺️ **Model Checking:** For complex workflows, use TLA+ or Alloy

**Speaker Notes:**
"Based on our findings, we recommend three tiers of action. First, immediate fixes: resolve the title length bug—it's a five-minute fix. Second, expand coverage and enhance property tests to cover more edge cases. Third, integrate tests into CI/CD so every code change is automatically verified. For process improvements, we suggest adopting contract-driven development across the entire codebase—not just for normalize_title—and using mutation testing to ensure our tests actually catch bugs. Long-term, consider fuzzing and model checking for even stronger guarantees. These investments in V&V pay dividends by catching bugs early, reducing production incidents, and enabling faster, confident releases."

---

## Slide 14: Conclusion & Summary

**Content:**

**What We Achieved:**
- ✅ 6/7 tests passed (83% pass rate)
- ✅ 67% structural code coverage
- ✅ 100+ property-based test cases auto-generated
- ✅ Formal proof of contract correctness (CrossHair)
- ✅ Visual evidence via UI screenshot
- ✅ 1 medium-severity defect identified (INC-001)

**Deliverables:**
- Comprehensive test suite (functional, property, contract, E2E)
- Coverage reports (XML, HTML)
- JUnit test results XML
- Incident report with reproduction steps and fix recommendation
- Full V&V report documenting approach, results, and recommendations

**Key Takeaway:**
"Multiple testing techniques provide complementary evidence. Unit tests catch basic bugs, property tests find edge cases, formal methods prove correctness, and E2E tests validate user experience. Together, they build confidence that the software works as intended."

**Thank You!**
Questions?

**Speaker Notes:**
"To conclude: we applied six V&V techniques to the Flask todo app, achieving 83% test pass rate and 67% code coverage. We auto-generated over 100 test cases with Hypothesis, formally proved our contracts with CrossHair, and captured visual evidence via Playwright. We identified one input validation defect and provided a fix. This multi-faceted approach—functional, property, formal, and E2E—gives stakeholders strong confidence in the application's correctness. No single technique is perfect, but together they cover each other's blind spots. Thank you. We're happy to take questions."

---

## Backup Slides (Optional - For Q&A)

### Backup Slide 1: Why Not Just Use Unit Tests?

**Content:**
- **Unit tests:** Good for verifying individual functions, but miss integration issues
- **Property tests:** Find edge cases humans wouldn't think to test
- **Formal verification:** Proves correctness for infinite input space, not just examples
- **E2E tests:** Validate the entire system including UI, templates, database
- **Coverage analysis:** Identifies gaps in testing

**Bottom Line:** No single technique is sufficient. V&V requires multiple perspectives.

---

### Backup Slide 2: Tool Comparison

| Technique | Pros | Cons | When to Use |
|-----------|------|------|-------------|
| Functional (pytest) | Easy to write, fast, good for regressions | Only tests examples you think of | Always—foundation of test suite |
| Property-based (Hypothesis) | Finds unexpected edge cases | Can be slow, requires property definitions | When input space is large |
| Formal (CrossHair) | Mathematical proof of correctness | Limited to pure functions, can be slow | For critical business logic |
| E2E (Playwright) | Tests real user experience | Slow, brittle if UI changes often | For key user workflows |
| Coverage (coverage.py) | Shows untested code | Doesn't measure test quality | To identify gaps |

---

### Backup Slide 3: Challenges We Faced

1. **Python 3.12 Compatibility:** Flasgger 0.9.5 used deprecated `imp` module → upgraded to 0.9.7.1
2. **Import Issues:** `app.py` ran `app.run()` on import → wrapped in `if __name__ == "__main__"`
3. **UI Test Selectors:** Had to inspect HTML to find correct input names for Playwright
4. **CrossHair Performance:** Formal verification can be slow for complex functions (ours was fast)

**Lesson:** V&V tools require environment setup and debugging, but the effort pays off in confidence.

---

### Backup Slide 4: References & Documentation

**Tools:**
- pytest: https://docs.pytest.org/
- Hypothesis: https://hypothesis.readthedocs.io/
- coverage.py: https://coverage.readthedocs.io/
- Playwright: https://playwright.dev/python/
- icontract: https://icontract.readthedocs.io/
- CrossHair: https://crosshair.readthedocs.io/

**Project:**
- GitHub: https://github.com/onurtacc/flask-todo-app
- Our Report: [REPORT.md](REPORT.md)

**Further Reading:**
- Dijkstra (1970): "Testing shows the presence, not the absence of bugs"
- Formal Methods in Industry: Microsoft's use of TLA+ for Azure services
- Property-Based Testing: QuickCheck (Haskell), ScalaCheck, fast-check (JavaScript)

---

**END OF PRESENTATION**

---

## Presentation Tips

**Timing:**
- 12 slides = ~2.5 minutes per slide for a 30-minute presentation
- Adjust if team size requires different timing (e.g., 5 min/person × 4 people = 20 min + 10 min Q&A)

**Delivery:**
- Practice with timer—don't rush slide 7 (property-based) and slide 9 (formal), as they're conceptually dense
- Use speaker notes—don't just read slides
- Show the screenshot on slide 11, show htmlcov on slide 10 if possible (live demo or screenshot)
- Incident slide (12) is key for showing V&V value—emphasize the finding

**Visual Aids:**
- Include screenshots of htmlcov, Swagger UI, app UI, or test output
- Use icons/logos for tools (pytest, Playwright, etc.)
- Consider live demo: run `pytest -v` or open `htmlcov/index.html`

**Engagement:**
- Ask audience: "Who has used property-based testing before?" (probably few—good teaching moment)
- Q&A: Prepare for "Why didn't you test X?" → answer: "We prioritized based on risk; that's a good candidate for future work"

**Export to PDF:**
- Use Markdown-to-slides tools: Marp, reveal.js, or Google Slides
- If using PowerPoint: paste content and add visuals

Good luck! 🚀
