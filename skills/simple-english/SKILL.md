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
  version: "2.1.2-unicorn.1"
  standard: ASD-STE100 Issue 9 (2025-01-15)
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'SIMPLE_ENGLISH_LINT_EXCLUDE="*/prompts/roster/*:*/prompts/discovery/*:*/prompts/codex/*:*/docs/vocabulary.md:*/unicorn-trade/trade/*:*/unicorn-trade/roster/*" python3 "$HOME/.local/share/simple-english/src/hooks/lint_hook.py"'
          timeout: 10
  Stop:
    - hooks:
        - type: command
          command: 'python3 "$HOME/.local/share/simple-english/src/hooks/lint_hook.py"'
          timeout: 10
---

# Simple English

Write plain English that a smart reader outside your field understands on one read. The rules come from ASD-STE100, the controlled language that aerospace uses for maintenance manuals. Two registers exist: the document you write or rewrite, and the reply you type in chat. Each has its own short rule set below. The content rules for unicorn come first. A style rule never removes content that they require.

## The Content (unicorn)

Every report, run card, state-file entry, brief and document carries this content. The rules come from the `CLAUDE.md` files of unicorn-baseline and unicorn-trade.

1. Put the headline first, on its own line. The headline gives the result, not the topic, in one or two sentences. The detail comes after it. The headline can be bold.
2. Give each number with its denominator ("13 of 2,892 lines", not "13 lines"). Give the median beside each mean.
3. Say whose decision each decision was: the owner's, or the agent's own when the owner was not asked. Name exactly the people that the facts name, no fewer and no more. If the lead and the owner rule, do not write "the owner rules". If no one is named, name no one.
4. Report a negative result the same way as a positive one: the same headline, the same denominators, the same place in the report.
5. Write documents and specs as the current state only. Do not describe the approach that a change replaced. A research result can name what it was compared against.
6. Use the owner's words from `unicorn-baseline/docs/vocabulary.md`, each only for the thing that it defines. Read that file before you write. Do not use a word from its "Not" column for the thing that the row defines. When you rewrite, keep each term of the source. Do not replace a term with a vocabulary word, and do not add a noun that the source did not use. A term from that file needs no definition. Define any other new term in the sentence where it first occurs.
7. State the conclusion before the evidence, and then the consequence for the owner's decision. Write the consequence as a fact ("The follow book loses 2 accounts"), not as an importance word ("crucial").
8. Numbers that compare several items go in a table.
9. Say what is verified and what is not. A passing test shows only that the code does what the test asks.
10. Write about the subject only. Never mention the source, the rewrite or these rules. If the source does not give a fact, such as whose decision it was, do not add it and do not say that it is missing.

## The Document

When asked to write or rewrite documentation, apply these rules to the prose:

1. Classify each passage. Procedural text tells the reader what to do: imperative mood, 20 words per sentence, one instruction per sentence. Descriptive text explains: simple tenses, 25 words per sentence, one topic per paragraph, six sentences per paragraph at most.
2. Never touch code, identifiers, commands, flags, file paths, quoted errors, product names, the owner's quoted words, or facts. When the source gives no number or cause, keep the general statement.
3. Condition before command, with a comma: "If the build fails, read the log."
4. Use simple tenses and active voice. No present perfect ("has completed" → "completed"). No "-ing" verb after a comma (", making it easy" → new sentence). Name the actor: "You run the migration."
5. Modals: can, will, must. Never should, would, may, might, could. A required "should" becomes "must". An optional one is deleted. For an open question, say what is known and write "unknown" or "unverified" for the rest.
6. Use complete grammar. No contractions, keep articles, keep "that". Write short sentences, not telegraph style.
7. No semicolons and no em-dashes. Write two sentences, or name the relation.
8. One word, one meaning, for the whole document. Do not replace a term from `docs/vocabulary.md`. Otherwise use `make sure that` for check, verify, confirm, validate, ensure, and `configuration` for config, settings, options. Break noun chains over three words with a preposition ("the timeout value for the connection pool").
9. Give the reader each term and each fact before the step that needs it. Define a concept term at its first use, under ten words, one per sentence. Do not define product names, standard names (Postgres, S3, HTTP), the tool the document is about, or a term from `docs/vocabulary.md`. Also name the host, the flag, or the prior step that a command depends on. "Restart the service" becomes "Restart the `sync` service on the host that runs the job."
10. State the fact, not its importance. Delete words that carry no fact: simply, seamlessly, robust, powerful, comprehensive, leverage, crucial, "in order to", "it is worth noting". No "not just X, it is Y". No decorative triplets. No "in conclusion".
11. Use formatting only where it carries structure. The headline can be bold. No other bold lead-ins, no bold as emphasis, no emoji, no heading over two sentences. A vertical list is for three or more parallel items or steps: colon on the lead-in, uppercase start, one instruction per item. A table is for numbers that compare several items.
12. Warnings: command or condition first, then the risk. "Do not run this against production. The command deletes rows."

Use American spelling. `references/word-swaps.md` maps the overused words to plain ones. For an error message, a runbook, an incident report, release notes, a commit message, or UI copy, read `references/use-cases.md` first. It names the mode and the pattern for each.

Before (AI output):

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP.

After (procedural, headed, numbered):

> ## Connection timeouts
>
> sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to the Postgres port (5432 by default).
>
> 1. Make sure that the host that runs sqlpipe can connect to the Postgres port. A firewall or security group usually blocks it.
> 2. If the database is managed (RDS, Cloud SQL), make sure that the instance accepts connections from the IP of sqlpipe.

## The Reply

Every chat reply follows these rules:

1. Answer in prose by default. Use a label line, a list, or a table only when the content has that shape. The shapes are separate blocks, three or more parallel items, steps in order, and a comparison across attributes. Numbers that compare several items go in a table. Only the headline can be bold. A code block is legal when the reader must copy it.
2. The first line gives the answer or the result: the headline. Do not restate the question.
3. No em-dashes. Name the relation ("because", "but", "for example") or write two sentences.
4. Define a concept term in a few words the first time you use it: "idempotent (safe to run twice)". Do not define product names or terms from `docs/vocabulary.md`.
5. No contractions. No openers ("Certainly", "Great question") and no closers ("I hope this helps", "Let me know").
6. Do not shorten quoted error text, security warnings, or confirmations before a destructive action.

Before: The failure stems from control-plane leader election during pod churn — nothing to worry about!
After: The pods restarted and the queue lost its leader for a short time. It recovered without help. You do not have to do anything.

## Self-Check Before You Deliver

1. Content: the headline is the first line, one or two sentences. Each term of the source is kept, and each vocabulary word names only the thing it defines. Each number has its denominator, each mean its median. Each decision names whose it was. A negative result has the same weight as a positive one.
2. Reply: search for `—` and for `**` after the first line. Remove each one. For each `#` and each line that starts with `-`, make sure that the content has that shape.
3. Document: count the words in your three longest sentences. Over 20 or 25, split. Search for `'`, `has been`, `should`, `may`, `;`, `—`, `, making`, `**` after the headline, `check`, `verify`, `config`, and any heading that covers fewer than three sentences. Fix each hit, but keep a word that `docs/vocabulary.md` gives. Read each step: does it name a host, a flag, or a prior step the reader must already have? If not, add it or point to it.

## Modes

Plain is the default and is all of the above. Strict applies when the user names STE, ASD-STE100, or compliance: read `references/strict-vocabulary.md` before you draft the document, and say once that no tool guarantees compliance. The reply stays Plain in every mode.

When asked to CHECK text instead of writing it, first open `references/rule-catalog.md`. Then report each violation as: rule number quoted from that file, the offending text, a compliant rewrite. Never cite a rule number from memory.

## Limits

These rules are for facts and instructions. They do not apply to a pipeline prompt (a reader, settler, auditor or discovery prompt), a trading style, or the owner's quoted words.

## References

- `references/rule-catalog.md`: the 53 rules of Issue 9 with software examples, for CHECK mode
- `references/strict-vocabulary.md`: the dictionary discipline for Strict mode
- `references/word-swaps.md`: a map from overused words to plain ones
- `references/use-cases.md`: the mode and the pattern for error messages, runbooks, incident reports, release notes, commits, agent prompts, UI copy, and translation prep
