---
name: simple-english
description: |
  The writing rules for the unicorn leads, coordinators, caretakers,
  builders and worker sub-agents: plain English in the spirit of
  ASD-STE100, plus the content every unicorn report and document must
  carry. Load it only when your session prompt or your agent definition
  names simple-english. Never load it in a session that runs a pipeline
  step: the discovery agent step or term review, a reader, settler or
  auditor, or a trading or deciding agent of unicorn-trade.
license: MIT
compatibility: claude-code
metadata:
  version: "2.1.2-unicorn.3"
  standard: ASD-STE100 Issue 9 (2025-01-15)
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'SIMPLE_ENGLISH_LINT_EXCLUDE="*/prompts/roster/*:*/prompts/discovery/*:*/prompts/codex/*:*/docs/vocabulary.md:*/unicorn-trade/trade/*:*/unicorn-trade/roster/*" python3 "$CLAUDE_PROJECT_DIR/.claude/skills/simple-english/hooks/lint_hook.py"'
          timeout: 10
  Stop:
    - hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/skills/simple-english/hooks/lint_hook.py"'
          timeout: 10
---

# Simple English

Write plain English that a smart reader outside the field understands on one read. Apply these rules in order. An earlier rule wins over a later one.

**Keep (never lose these)**

1. Keep every fact, number, name, decision and caveat. Add none.
2. Keep each term the writer used. Do not swap a term for a synonym or for a word from `docs/vocabulary.md`, and use one word for one thing in the whole text.
3. Keep code, paths, commands, flags, quoted errors and the owner's quoted words exactly.
4. Give each number with its denominator ("13 of 2,892 lines"), and the median beside each mean.
5. Name exactly who decided each decision, as the facts name them: no fewer people and no more. If no one is named, name no one.
6. Report a negative result like a positive one: same headline, same denominators.
7. Say what is verified and what is not.

**Shape**

8. The first line is the headline: the result in one or two sentences, not the topic. It can be bold.
9. Then the evidence, then the consequence, stated as a fact.
10. Numbers that compare several items go in a table. A list is for three or more parallel items or steps. Otherwise, prose.
11. Describe the current state only. Write about the subject, never about the source or these rules.

**Style**

12. Short sentences: 20 words for instructions, 25 for description. One topic per paragraph.
13. Active voice and simple tenses. Condition before command: "If the build fails, read the log."
14. Use can, will or must. Not should, would, may, might or could.
15. No em-dashes, no semicolons, no contractions, no bold after the headline.
16. No filler or importance words (crucial, robust, seamlessly, "in order to"). State the fact instead.
