# The shark skill

When Claude says your business idea is great, put it in front of a Shark Tank where every shark is a
Claude, and they all want to say no.
One Claude Code skill. Free, MIT, no signup, no API key, nothing to connect.

Made by **Alex Chen** ([@nocodealex](https://instagram.com/nocodealex)), an AI creator who builds free Claude Code skills. Step-by-step guide at [chen.media](https://chen.media/guides/pitch-your-idea-to-a-panel-of-claude-sharks-who-want-to-say-no-how-to-install-the-free-skill).

Ask Claude "is this a good business idea?" and it usually says yes. `/shark` puts the same idea in
front of a Shark Tank-style panel instead:

1. **5 sharks** read your pitch, and each writes their biggest worry and their three hardest
   questions. Each one has a personality and a signature line: the tech billionaire shark ("Is this a
   business or a hobby?"), the royalty shark (it only offers money for a cut of every sale), the
   customer shark, the numbers shark and the skeptic shark.
2. A **founder** Claude answers every question, only from what you told it. When your pitch does not
   have the answer, it says so, and that question goes on your homework list.
3. Each shark decides **IN or OUT**, with a practice offer ("$50,000 for 10%"), one line of why, and
   the one thing that would change their mind. A shark that's out says it the classic way: "For that
   reason, I'm out."

What comes back is `BOARD.md`: how many sharks are in, every decision and offer, what would change
their minds, and the questions you could not answer yet.

**It never touches your files.** Everything is written inside `.shark/` in the folder you run it in.

## Install

Paste this into Claude:

```
https://github.com/alexyc9381/shark-skill
Install this skill, then confirm /shark works.
```

Or copy the folder yourself, in Claude Code:

```bash
git clone https://github.com/alexyc9381/shark-skill
cp -r shark-skill/skills/shark ~/.claude/skills/
```

Or with the skills CLI (works for Claude Code and other agents):

```bash
npx skills add alexyc9381/shark-skill
```

Or as a plugin:

```
/plugin marketplace add alexyc9381/shark-skill
/plugin install shark-skill@shark-skill
```

## Use

```
/shark A subscription box of local hot sauces. $35 a month, 12 customers so far, I want to reach 500.
```

| flag | meaning |
| --- | --- |
| `--investors N` | 2 to 10 sharks. Default 5. |
| `--seed S` | A random panel from all 10 sharks, reproducibly. |

Five investors is 11 sub-agent calls (5 sets of questions, 1 founder, 5 decisions). Every sub-agent
counts toward your Claude plan's usage. Turn on accept-edits mode (Shift+Tab) first so you are not
asked to approve every file.

See `examples/hot-sauce/BOARD.md` for a real 2-investor session: "A subscription box of hot sauces
from small local makers, $35 a month" got no deal from either shark, and six pieces of homework.

## How it works

`skills/shark/shark.py` does the bookkeeping: it opens the session, writes one brief per sub-agent,
checks every output exists, counts the deals and renders the board. Claude only hosts: it never
invests, never answers for you and never edits a decision. The investors are in
`skills/shark/investors.json`.

```bash
python3 -m unittest discover -s tests
```

## Making a video or post about this?

Go ahead. Credit it like this, in your caption or description:

```text
/shark skill by Alex Chen (@nocodealex): github.com/alexyc9381/shark-skill
```

Tag [@nocodealex](https://instagram.com/nocodealex) so I can see it. Every board the skill writes already ends with the same credit, so leave it in the shot.

Writing about it or citing it in a paper? Use **Cite this repository** in the sidebar on GitHub.

## Uninstall

```bash
rm -rf ~/.claude/skills/shark
```

Not made by Anthropic, and not connected to the TV show. The sharks are language models and the offers are practice numbers, not
real money and not financial advice.
