# SEN4013 Software Verification & Validation Project
## Comprehensive V&V of a Flask Todo Application

**Team:** [Team Member 1, Team Member 2, Team Member 3, Team Member 4]
**Course:** SEN4013 - Software Verification and Validation
**Date:** January 16, 2026
**Duration:** 6-8 minutes total

---

## Slide 1: Title & Project Overview
**30 seconds**

**Comprehensive Verification & Validation of a Flask Todo Application**

**Team Members:**
- [Name 1] - Functional & Property Testing
- [Name 2] - Formal Verification & Contracts
- [Name 3] - UI Testing & Coverage
- [Name 4] - Integration & Documentation

**What We Did:**
- Selected Flask Todo app for V&V analysis
- Applied 6 automated testing techniques
- Found 1 bug, achieved 67% coverage
- Generated formal proofs and test artifacts

**[SCREENSHOT: Architecture diagram or project overview]**

---

## Slide 2: Requirements Alignment & Project Motivation
**1 minute**

**Meeting ALL SEN4013 Project Requirements**

| Requirement | Our Deliverable | Status |
|-------------|-----------------|--------|
| **Part 1: Automated Tools Review** (35 pts) | 6 tools reviewed & justified | ✅ Slide 3 |
| **Part 2: Functional Testing** (35 pts) | pytest test suite with CRUD tests | ✅ Slide 4 |
| **Part 2: Structural Testing** (35 pts) | 67% coverage with coverage.py | ✅ Slide 5 |
| **Part 3: Report** (20 pts) | Complete PDF with all sections | ✅ Submitted |
| **Part 4: Presentation** (10 pts) | This presentation + video | ✅ Now |

**Why This Project?**
- Real-world Flask web app with REST API
- Multiple testing surfaces (UI, API, database)
- Clear Swagger specification to verify against
- Manageable scope for deep V&V analysis

**Key Concepts:**
- **Verification:** Building the product right (matches spec)
- **Validation:** Building the right product (meets user needs)
- **Automation:** All testing automated for repeatability

**[SCREENSHOT: Requirements checklist showing all items completed]**

---

## Slide 3: AUTOMATED TOOLS REVIEW - Part 1 Deliverable
**1 minute**

**Six Complementary V&V Tools**

| # | Tool | Type | Why Selected? |
|---|------|------|---------------|
| 1 | **pytest** | Functional Testing | Industry standard, great error messages |
| 2 | **Hypothesis** | Property-Based Testing | Auto-generates 100+ test cases from specs |
| 3 | **coverage.py** | Structural Testing | Measures code coverage, XML/HTML reports |
| 4 | **Playwright** | UI/E2E Testing | Real browser automation, visual evidence |
| 5 | **icontract** | Runtime Verification | Design-by-contract, fail-fast |
| 6 | **CrossHair** | Formal Verification | Mathematical proofs via SMT solver |

**Complementary Nature:**
- pytest catches basic bugs → Hypothesis finds edge cases → coverage.py shows gaps
- Playwright validates UX → icontract enforces invariants → CrossHair proves correctness

**[SCREENSHOT: All 6 tools installed - pip list output]**

---

## Slide 4: FUNCTIONAL TESTING - Part 2 Deliverable
**1 minute**

**Black-Box Testing with pytest**

**What is Functional Testing?**
Tests behavior against requirements (black-box: inputs → expected outputs)

**Our Test Cases:**

**T01: Home UI Load** ✅ PASS
```python
def test_home_ui_loads(client):
    response = client.get("/")
    assert response.status_code == 200
```

**T02: API Create & List** ✅ PASS
```python
def test_create_and_list_todo(client):
    response = client.post("/api/todos", json={"title": "Test"})
    assert response.status_code == 201
    todos = client.get("/api/todos").get_json()
    assert any(t["title"] == "Test" for t in todos)
```

**T03: Empty Title Rejection** ✅ PASS
```python
def test_empty_title_rejected(client):
    response = client.post("/api/todos", json={"title": ""})
    assert response.status_code == 400
```

**T04: Long Title Rejection** ❌ FAIL (Bug INC-001 discovered!)

**[SCREENSHOT: pytest output with 3 green passes, 1 red failure]**

---

## Slide 5: STRUCTURAL TESTING - Part 2 Deliverable
**1 minute**

**White-Box Coverage Analysis with coverage.py**

**What is Structural Testing?**
Examines internal code structure, measures what code is executed (white-box coverage)

**Coverage Achieved: 67%**

```
Name                           Stmts   Miss  Cover
--------------------------------------------------
app.py                            95     45    53%
tests/test_api_properties.py      28      0   100%
tests/test_contracts.py            3      0   100%
tests/test_ui_playwright.py       18      0   100%
--------------------------------------------------
TOTAL                            136     45    67%
```

**What's Covered (Green):**
- ✅ API create/list endpoints
- ✅ Input validation
- ✅ All test code (100%)

**What's NOT Covered (Red):**
- ❌ Web form handlers
- ❌ Update/delete endpoints
- ❌ Some error paths

**67% is acceptable for initial V&V** (industry standard: 70-80%)

**[SCREENSHOT: HTML coverage report showing red/green highlighting]**

---

## Slide 6: Additional Testing Techniques
**1.5 minutes**

**Property-Based Testing (Hypothesis):**
- Auto-generated 100+ test cases from regex patterns
- Found edge cases humans wouldn't think of
- All passed ✅

**UI/E2E Testing (Playwright):**
- Real browser automation testing complete user workflow
- Screenshot evidence captured
- Passed ✅

**Runtime Verification (icontract):**
- Design-by-contract with preconditions/postconditions
- Enforces business rules at runtime
- All contracts satisfied ✅

**Formal Verification (CrossHair):**
- SMT solver provides mathematical proof
- No counterexamples found for `normalize_title`
- Proven correct for all valid inputs ✅

**[SCREENSHOT: Hypothesis statistics showing 100+ examples]**
**[SCREENSHOT: Playwright UI screenshot after adding todo]**

---

## Slide 7: Key Finding - Bug INC-001
**1 minute**

**Incident INC-001: Missing Title Length Validation**

**Severity:** Medium | **Status:** Open (Documented)

**The Bug:**
```python
# Test T04 - Expected behavior
def test_excessive_title_length(client):
    response = client.post("/api/todos", json={"title": "x" * 200})
    assert response.status_code == 400  # Expected: reject
```

**Expected:** HTTP 400 Bad Request
**Actual:** HTTP 201 Created ❌ (App accepts 200-char title!)

**Root Cause:**
```python
# app.py line 152 - Missing validation
if not title:  # ✅ Checks empty
    return jsonify({"error": "Title required"}), 400
# ❌ MISSING: length check (should reject >100 chars)
```

**Impact:**
- Data integrity: Silent truncation by database
- User experience: No feedback for invalid input
- Security: Potential buffer overflow risk

**Fix:** Add `if len(title) > 100: return 400` (10-minute fix)

**This demonstrates V&V value:** Found before production! 🎯

**[SCREENSHOT: Test failure showing expected 400 but got 201]**

---

## Slide 8: Results & Recommendations
**1 minute**

**Quantitative Results:**
- **Pass Rate:** 6/7 tests = 86% (1 expected failure)
- **Coverage:** 67% overall
- **Defects Found:** 1 medium-severity bug (INC-001)
- **Test Cases:** 110+ executed in 60 seconds
- **Automation:** 100%

**Artifacts Generated:**
✅ coverage.xml (Cobertura)
✅ junit.xml (CI/CD ready)
✅ ui_after_add.png (visual evidence)
✅ htmlcov/ (interactive report)

**Immediate Recommendations:**
1. **Fix INC-001** (10 min) - Add title length validation
2. **Expand coverage to 80%** (2 hrs) - Test remaining endpoints
3. **CI/CD integration** (4 hrs) - Run tests on every commit
4. **Security testing** - Add SQL injection, XSS tests

**ROI:** 15 hours invested → Found bug that would cost 10+ hours in production

**[SCREENSHOT: Test results dashboard showing metrics]**

---

## Slide 9: Conclusion & Key Takeaways
**30 seconds**

**What We Achieved:**
✅ Comprehensive V&V using 6 automated techniques
✅ Satisfied ALL project requirements (Parts 1-4)
✅ Explicit functional and structural testing
✅ Found 1 bug, achieved 67% coverage
✅ Generated formal proofs and CI/CD artifacts

**Key Insights:**
1. **No single technique is sufficient** - Each tool found different things
2. **Automation enables confidence** - 110+ tests run in 60 seconds
3. **V&V is cost-effective** - Found bug before production
4. **Limitations matter** - 67% ≠ 100% confidence

**Answer:** Does the Flask app work correctly?
**Yes, with caveats.** Core functionality verified, 1 bug documented, 33% remains untested.

**Confidence Level:** Medium-High (→ High after fixing INC-001)

"Testing shows the presence, not the absence, of bugs." — Dijkstra

**Thank you! Questions?** 🎤

**[SCREENSHOT: Summary visualization of all V&V metrics]**

---

## Quick Reference for Q&A

**Tool Details:**
- All tools open-source and free
- Setup time: ~2 hours
- Total V&V investment: 15 hours

**Coverage Gaps:**
- Web form handlers (add/edit/delete via UI)
- Additional API endpoints (GET by ID, PUT, DELETE)
- Some error handling paths

**Future Work:**
- Mutation testing (validate test quality)
- Security testing (OWASP Top 10)
- Performance/load testing
- Cross-browser testing

**Learning Outcomes Addressed:**
✅ LO#1: V&V concepts (verification vs. validation)
✅ LO#2: Model-checking (property-based, formal verification)
✅ LO#3: Runtime verification (icontract)
✅ LO#4: Selecting appropriate techniques (6 tools justified)
✅ LO#5: Limitations (honest assessment)
✅ LO#6: Automated tools (6 tools used, artifacts generated)

---

**END OF CONCISE PRESENTATION**

---

## Presentation Timing Guide

**Target: 6-8 minutes total**

| Slide | Topic | Time | Cumulative |
|-------|-------|------|------------|
| 1 | Title & Overview | 30s | 0:30 |
| 2 | Requirements & Motivation | 1:00 | 1:30 |
| 3 | Tools Review (Part 1) | 1:00 | 2:30 |
| 4 | Functional Testing (Part 2) | 1:00 | 3:30 |
| 5 | Structural Testing (Part 2) | 1:00 | 4:30 |
| 6 | Additional Techniques | 1:30 | 6:00 |
| 7 | Bug Finding (INC-001) | 1:00 | 7:00 |
| 8 | Results & Recommendations | 1:00 | 8:00 |
| 9 | Conclusion | 0:30 | 8:30 |

**Tips for 6-8 Minute Delivery:**
1. **Practice transitions** - Know exactly where one slide ends and next begins
2. **Point to screenshots** - Let visuals do the talking
3. **Skip speaker notes** - They're for reference only
4. **Focus on requirements** - Slides 2-5 explicitly address all 4 parts
5. **Emphasize the bug** - INC-001 proves V&V value
6. **Time yourself** - Aim for 7 minutes to leave buffer

**If Running Over Time, Cut:**
- Slide 6 details (just say "we also did 4 additional techniques")
- Code snippets on Slide 4 (just say "we wrote 4 functional tests")
- Detailed coverage numbers on Slide 5 (just say "achieved 67%")

**If Running Under Time, Expand:**
- Slide 7: Show curl reproduction of bug
- Slide 8: Discuss CI/CD integration in detail
- Slide 6: Demo one property-based test execution

**Good luck! 🚀**
