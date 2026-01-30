# /plan - Create Technical Plan

Create a detailed technical plan for implementing a feature or fixing an issue.

## Instructions

1. **Understand the Request**: Read the user's feature request or issue carefully
2. **Research**: Explore relevant code to understand current implementation
3. **Design**: Create a step-by-step implementation plan
4. **Document**: Write the plan to `.claude/plans/[feature-name].md`

## Plan Template

```markdown
# Plan: [Feature Name]

## Status: DRAFT

## Overview
[Brief description of what this plan accomplishes]

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Non-Goals
- What this plan does NOT address

## Technical Design

### Changes Required
1. **File**: `path/to/file.py`
   - Change: Description
   - Reason: Why this change

### New Files
1. **File**: `path/to/new/file.py`
   - Purpose: What this file does

## Implementation Tasks
1. [ ] Task 1
2. [ ] Task 2
3. [ ] Task 3

## Testing Strategy
- Unit tests for X
- Integration tests for Y

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Low/Med/High | Low/Med/High | How to handle |

## Open Questions
- [ ] Question 1?
```

## Usage

```
/plan add GWT value auto-detection
/plan fix authentication timeout issue
```

When the plan is ready for review, change status to `READY_FOR_REVIEW` and ask the user to approve before implementing.
