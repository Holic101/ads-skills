# For Dima

This is your running learning journal. Every time we finish a real task, I add a new dated entry that breaks down what we did and why - the way a friend would explain it over coffee, not the way a manual would. Read top to bottom and you should come away smarter, not just informed.

Newest entries go at the top.

---

## 2026-06-16 - Setting up "Teaching Mode" itself

This first entry is a little meta. The task we did together was to build the thing you're reading right now: a system where I teach you after every task. So let me walk you through how I set it up, because the same thinking applies to almost everything else we'll do.

### Step 1 - What approach did I take, and why?

My starting point was a question most people skip: "Is this a one-time thing or a forever thing?"

You didn't ask me to write one essay. You asked me to make you smarter "after every single task." That word - *every* - changed everything. A one-time request you handle by just doing it. A forever request you handle by changing the system so it keeps happening without anyone remembering to ask.

Think of it like the difference between mopping the floor and fixing the leak. If you only mop, you'll be mopping forever. So I split the job in two:

1. **Fix the leak** - write the instruction into `CLAUDE.md`, the file that configures how this agent behaves on every session. Now "write a FOR_DIMA.md after each task" is a standing rule, not something you have to re-type.
2. **Mop once, visibly** - write the first actual `FOR_DIMA.md` (this file) so the rule isn't just theory. You can see exactly what it produces, and future-me has a template to match.

That two-part move - *change the rule AND show one worked example* - is the whole approach.

### Step 2 - What other approaches did I consider but abandon?

Three roads I didn't take:

- **Just write the essay and stop.** Tempting, because it's the literal request and it's less work. I rejected it because it quietly fails the real goal. Next task, the teaching wouldn't happen unless you remembered to ask again. You'd be mopping forever. The cost of skipping the "leak fix" is invisible today and expensive every day after.

- **Build a hard automation (a "hook") that forces the file to be written.** Claude Code supports hooks - scripts that fire automatically on events. I considered wiring one up so a FOR_DIMA.md is *mechanically* required. I abandoned it because it's the wrong tool for a judgment call. A hook can't tell the difference between "we redesigned your whole campaign structure" (worth teaching) and "I fixed one typo" (not worth a journal entry). Forcing a lesson after trivial work would train you to skip-read the journal, which kills the entire point. An instruction in CLAUDE.md keeps a human-like judgment in the loop ("after any *non-trivial* task").

- **Put the instruction in a separate skill or a README nobody reads.** I rejected this because `CLAUDE.md` is the one file guaranteed to load into my context every session. Burying the rule somewhere less central is like writing your gym goal on a napkin instead of the bathroom mirror. Placement is a decision, not an afterthought.

### Step 3 - How do the parts connect?

There are exactly two artifacts and they're in a deliberate order:

1. **The rule** (the new "Teaching Mode" section in `CLAUDE.md`) - this is the *engine*. It defines the nine steps, the coffee-chat style, and the "running journal, don't overwrite" behavior.
2. **The example** (this `FOR_DIMA.md`) - this is the *engine running once*. It proves the rule works and sets the tone every future entry should match.

The order matters: rule first, example second. The example literally obeys the rule it came from. If you ever want to change how these journals read, you change the rule in `CLAUDE.md`, and every future entry follows. One source of truth, not a habit I have to remember.

### Step 4 - What tools and frameworks did I use, and why those?

- **`CLAUDE.md` over a hook** - explained above: I wanted persistent behavior *with* judgment, not blind enforcement. CLAUDE.md is instructions-as-configuration. It's the cheapest reliable way to make a behavior "default."
- **A Markdown journal over a doc tool or database** - this repo already speaks Markdown and lives in git. Keeping the journal as a plain `.md` file means it's versioned (you can see how your own understanding grew over time via git history), diffable, and readable anywhere. No new tool to learn.
- **A fixed 9-step template** - structure beats blank-page freedom here. If every entry answers the same nine questions, you can compare entries and your brain starts to expect the shape. That repetition is what turns reading into learning.

If I'd picked a fancier tool (say, a database of lessons), I'd have gained query-ability but lost the thing that makes this stick: it's dead simple and it lives right next to the work.

### Step 5 - What tradeoffs did I make?

- **Judgment over guarantee.** By using an instruction instead of forced automation, I accept that a sloppy future session *could* skip the journal. I traded ironclad enforcement for the much bigger prize: entries only get written when they're worth reading. Quality over coverage.
- **A bit more text in CLAUDE.md.** Every line I add there costs context space the agent has to carry around forever. I judged this rule worth the rent. But it's a real cost - CLAUDE.md isn't a junk drawer, and I kept the section tight for that reason.
- **Append-only journal over a tidy single summary.** A running log will get long. I chose that on purpose: your learning history is more valuable than a clean one-pager, and "newest on top" keeps it usable.

### Step 6 - What mistakes or dead ends did we hit?

Honestly, the main trap on this one was *interpreting the task*, not executing it. My first instinct was to treat "write a FOR_DIMA.md" as the entire job. I caught myself because of that word "every" - it signaled this was a process request wearing a task request's clothing. The fix was the two-part split. No code blew up, but the dead end was real: if I'd taken the request literally, I'd have delivered something that looked complete and quietly wasn't.

That's the most common failure mode with instructions in general - doing exactly what was said and missing what was meant.

### Step 7 - What pitfalls should you watch for next time?

- **"Every / always / from now on" = build a system, not a one-off.** The moment a request implies repetition, stop and ask where the rule should live so it survives you forgetting it.
- **Don't automate judgment calls.** If a task needs a human-ish "is this worth doing?" decision, a rigid script will do it badly. Reserve hard automation for things that are the same every time.
- **Put rules where they'll actually be seen.** A great policy in an unread file is a fantasy. Find the "always loaded" surface (here, CLAUDE.md) and put it there.
- **Ship one worked example with any new convention.** Rules are abstract; examples are contagious. People copy what they can see.

### Step 8 - What would an expert notice that a beginner would miss?

A beginner reads "write me a doc" and writes a doc. An expert reads the same sentence and asks: *what's the real job behind this request, and where does the behavior need to live so it keeps happening?*

The expert move here wasn't writing good prose - it was recognizing this was a **systems** task disguised as a **content** task, and choosing the persistence mechanism (CLAUDE.md) and the enforcement style (instruction, not hook) to match. Beginners optimize the deliverable. Experts optimize the thing that produces deliverables.

The other expert tell: respecting the existing house style (short dashes, no emojis, Markdown in git) instead of inventing my own. Fitting into a system is usually smarter than improving it on day one.

### Step 9 - What transfers to completely different projects?

- **Separate the leak from the mop.** Any time you find yourself doing something repetitive, ask what rule or system would stop you from re-deciding it every time. This applies to ad ops (build a reusable launch checklist instead of remembering the steps each launch), to code, to your inbox - everywhere.
- **Read for intent, not just words.** The gap between what's said and what's meant is where most work goes wrong. Train the habit of restating the *goal* before executing the *task*.
- **Match the tool to the type of decision.** Rote and identical? Automate hard. Needs judgment? Use a guideline and keep a human in the loop. Picking wrong in either direction is the source of a huge amount of frustration.
- **A rule plus one example beats either alone.** Whenever you set a standard for a team or for yourself, write it down *and* show one done right. That pairing is how conventions actually spread.

That's the whole thing. The short version: you asked for a habit, so I built the habit, then demonstrated it once. Next task, you'll get one of these for real work - and we'll keep stacking them here.
