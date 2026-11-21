<p align="center">
  <strong>✈️ your AI writes like a LinkedIn post. make it write like a Boeing manual.</strong>
</p>

<p align="center">
  An agent skill that makes LLMs write plain English with the discipline of <a href="https://www.asd-ste100.org/">ASD-STE100 Simplified Technical English</a>,<br>
  the controlled language aerospace has used since 1983 so that a tired mechanic cannot misread an instruction.<br>
  Layman-readable.
</p>

<p align="center">
  <a href="evals/results/rebuild-2026-09-02/RESULTS.md"><img src="https://img.shields.io/badge/reply_defects-%E2%88%9295%25_measured-brightgreen?style=flat" alt="95% fewer visible reply defects, measured"></a>
  <a href="evals/results/RESULTS.md"><img src="https://img.shields.io/badge/benchmarked_on-9_Claude_models-blueviolet?style=flat" alt="9 models benchmarked"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/SKILL.md-open_standard-blue?style=flat" alt="Agent Skills"></a>
  <a href="skills/simple-english/SKILL.md"><img src="https://img.shields.io/badge/version-2.1.2-blue?style=flat" alt="version 2.1.2"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat" alt="MIT"></a>
  <a href="https://github.com/AminBlg/SimpleEnglish/stargazers"><img src="https://img.shields.io/github/stars/AminBlg/SimpleEnglish?style=flat&logo=github&color=yellow" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/97933?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-97933" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/97933/daily" alt="AminBlg%2FSimpleEnglish | Trendshift" width="250" height="55"/></a>
</p>

Works in every agent that reads the [Agent Skills standard](https://agentskills.io): Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, Goose, OpenCode, and about 25 more. One folder, no dependencies, MIT.

## Install

This fork installs into a repository, not into a user account, so the skill loads on every machine that clones the repository. Copy it into the directory that the repository's `.claude/skills` resolves to, and commit the result:

```bash
python3 vendor.py /path/to/repo/.claude/skills
```

The copy holds `SKILL.md` and `hooks/` (`lint_hook.py`, `ste_lint.py`, `slop.tsv`). Its hooks call `$CLAUDE_PROJECT_DIR/.claude/skills/simple-english/hooks/lint_hook.py`, and they run only in a session that loads the skill itself. A sub-agent gets the rules from `skills: [simple-english]` in its agent definition, but no hook. To update a repository, run `vendor.py` again and commit.

## See it

Left is real, unedited Claude output. Right is the same model with the skill loaded.

<table>
<tr>
<th width="50%">Without skill</th>
<th width="50%">With skill</th>
</tr>
<tr>
<td valign="top">

> Leveraging sqlpipe's robust architecture, users can seamlessly synchronize their Postgres tables to S3 with minimal configuration overhead. Before getting started, you should ensure that your AWS credentials have been properly configured — this is crucial for avoiding frustrating permission issues down the line.

</td>
<td valign="top">

> sqlpipe copies your Postgres tables to S3. It needs one configuration file.
>
> Before you start, make sure that your AWS credentials are correct. If they are not, S3 rejects the upload with a permission error.

</td>
</tr>
</table>

More rewrites in [`examples/before-after.md`](examples/before-after.md): READMEs, runbooks, incident reports, error messages, release notes.

## Benchmarks

Every number below is recomputed from the committed raw files by `python3 evals/check_numbers.py`, which CI runs on every push. All Claude runs: `claude-sonnet-4-6`, low effort, no settings loaded. Judges are Claude models on Claude text, so family bias is possible.

Replies, 8 chat questions with a jargon term each, two runs, [raw files and tables](evals/results/rebuild-2026-09-02/RESULTS.md). Counts are totals over the 16 replies. **95% fewer visible defects** (em-dashes, bold, headers, bullets) with 2.0.1 than with no skill (218 → 11). These counts come from the 2026-09-02 runs of 2.0.1, which still had the five-sentence reply cap that 2.1.0 removed. No run exists yet for 2.1.0 or later. A blind judge preferred 2.0.1 over 2.0.0 in 14 of 16 pairs.

| Condition | words | sentences | em-dashes | bold | headers | bullets |
|---|---:|---:|---:|---:|---:|---:|
| no skill | 216 | 16.8 | 62 | 79 | 25 | 52 |
| 2.0.0 | 184 | 14.4 | 43 | 72 | 4 | 52 |
| 2.0.1 | 146 | 7.9 | 5 | 2 | 0 | 4 |

On gpt-4.1-mini the same 8 questions went from 23 sentences, 64 bold spans, and 101 bullets per 8 replies. With 2.0.1 they went to 5.2 sentences and zero formatting.

Documents, the 8 sqlpipe writing tasks scored with the STE linter, one run per cell. One run moves by about 0.5 on this model, so read the rows as parity or better, not as a ranking.

| Condition | viol/100w | Reduction |
|---|---:|---:|
| no skill | 4.09 | |
| 1.3.0 | 2.11 | 48% |
| 2.0.0 | 1.70 | 58% |
| 2.0.1 | 0.91 | 78% |

The linter history: 81.3% fewer linter violations across 9 Claude models (144 generations, [RESULTS.md](evals/results/RESULTS.md)), plus Pi, opencode, and OpenAI runs in [`evals/results/`](evals/results/). Those numbers reproduce. A [2026-09-02 audit](evals/results/WHY-USELESS-2026-09-02.md) showed that they measure rule obedience, not what a reader sees, which is why 2.0.1 reports the reply counts above.

## The rules

[`SKILL.md`](skills/simple-english/SKILL.md) holds one ordered list of 16 rules, about 300 words. An earlier rule wins over a later one.

| Group | Rules | What they keep or kill |
|---|---|---|
| Keep | 1–7 | Facts, terms, code and quotes, denominators and medians, the exact deciders, negative results, what is verified |
| Shape | 8–11 | Headline first, then evidence and consequence, tables for compared numbers, the current state only |
| Style | 12–16 | Long sentences, passive voice, hedging modals, em-dashes and semicolons, bold after the headline, filler words |

## FAQ

Does this make output STE-certified? No. Nothing does, because ASD certifies no tool. Word-level rulings live in the official standard, a [free download](https://www.asd-ste100.org/request.html).

Will my docs sound robotic? They will sound like Airbus manuals: flat and impossible to misread. For docs that is the whole point. Keep your voice for your blog.

Why not just prompt "write clearly"? "Clearly" is an opinion. "No sentence over 20 words" is a spec. Agents follow specs.

Why a 40-year-old aerospace standard? It is maintained (Issue 9, January 2025), numbered, and testable. It is also a near-perfect negative of every AI writing tell.

How was it built? Against the primary Issue 9 text, not summaries. A community audit ([#4](https://github.com/AminBlg/SimpleEnglish/issues/4)) checked the vocabulary tables against the dictionary. Scenarios and recorded results: [`evals/pressure-tests.md`](evals/pressure-tests.md).

## Star history

[![Star History Chart](https://api.star-history.com/chart?repos=AminBlg/SimpleEnglish&type=date&legend=top-left)](https://www.star-history.com/?repos=AminBlg%2FSimpleEnglish&type=date&legend=top-left)

## Contributing

Open an issue for questions and bug reports. Pull requests are welcome. A change that moves a published number ships the raw files with it, and `python3 evals/check_numbers.py` must pass. Run `python3 evals/ste_lint.py --self-test` before you push. Say in the PR whether an agent wrote the code, and do not add attribution trailers.

## License

MIT for everything here. The repo paraphrases the rules for teaching and reproduces no spec text or dictionary content. Unofficial project, not affiliated with or endorsed by ASD or STEMG. ASD-STE100 is a registered trademark of ASD.
