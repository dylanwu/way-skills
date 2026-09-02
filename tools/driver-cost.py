#!/usr/bin/env python3
"""Measure what a to-tdd driver session actually cost, and whether the rules held.

Usage:  tools/driver-cost.py [session.jsonl | project-dir-substring]
        tools/driver-cost.py            # auto-pick the most recent session that dispatched agents

Answers three questions the skill's rules are supposed to move:
  1. Did the driver implement instead of driving?   -> Edit/Write count from the driver
  2. Did the end review get dispatched, or handed to the harness command?
  3. What did the driver's own context cost?        -> cache_read is the bill
"""
import json, glob, os, sys, collections

ROOT = os.path.expanduser("~/.claude/projects")

def sessions():
    for f in glob.glob(ROOT + "/*/*.jsonl"):
        if os.path.getsize(f) > 50000:
            yield f

def scan(f):
    models, tools, agents, edits = collections.Counter(), collections.Counter(), [], []
    chars, counts = collections.Counter(), collections.Counter()
    usage = collections.Counter()
    driver_model, turns = None, 0
    for line in open(f, errors="ignore"):
        try: o = json.loads(line)
        except Exception: continue
        m = o.get("message") or {}
        u = m.get("usage")
        if u:
            mm = m.get("model", "?")
            models[mm] += 1
            if mm != "<synthetic>":
                driver_model = driver_model or mm
                turns += 1
                for k in ("input_tokens", "output_tokens",
                          "cache_creation_input_tokens", "cache_read_input_tokens"):
                    usage[k] += u.get(k, 0) or 0
        c = m.get("content")
        if not isinstance(c, list): continue
        for x in c:
            if not isinstance(x, dict): continue
            t = x.get("type")
            if t == "tool_use":
                n = x.get("name")
                tools[n] += 1
                inp = x.get("input") or {}
                if n in ("Edit", "Write", "NotebookEdit") and inp.get("file_path"):
                    edits.append(inp["file_path"])
                if n == "Agent":
                    agents.append((inp.get("model", "<NOT SET>"), (inp.get("description") or "")[:44]))
                if n == "Skill":
                    tools["Skill:" + str(inp.get("skill"))] += 1
                key = "tool_use:" + str(n); s = len(json.dumps(inp))
            elif t == "tool_result":
                r = x.get("content"); s = len(r if isinstance(r, str) else json.dumps(r)); key = "tool_result"
            elif t == "text":
                s = len(x.get("text") or ""); key = "text"
            else:
                s = len(json.dumps(x)); key = str(t)
            chars[key] += s; counts[key] += 1
    return dict(models=models, tools=tools, agents=agents, edits=edits, chars=chars,
                counts=counts, usage=usage, driver_model=driver_model, turns=turns)

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg and os.path.isfile(arg):
        target = arg
    else:
        cands = [f for f in sessions() if not arg or arg in f]
        cands = [(f, scan(f)) for f in cands]
        cands = [(f, d) for f, d in cands if d["tools"].get("Agent")]
        if not cands:
            sys.exit("no session with Agent dispatches found")
        target = max(cands, key=lambda x: os.path.getmtime(x[0]))[0]
    d = scan(target)
    print("session: %s" % target)
    print("project: %s\n" % os.path.basename(os.path.dirname(target)))

    u, n_turns = d["usage"], max(d["turns"], 1)
    total = sum(u.values())
    print("--- 3. what the driver's own context cost (model: %s) ---" % d["driver_model"])
    print("  turns %d | output %s | cache_write %s" % (d["turns"], f"{u['output_tokens']:,}", f"{u['cache_creation_input_tokens']:,}"))
    print("  cache_read %s  (%.0f%% of all tokens)" % (f"{u['cache_read_input_tokens']:,}",
          100 * u["cache_read_input_tokens"] / max(total, 1)))
    print("  avg context re-read per turn: %s" % f"{u['cache_read_input_tokens'] // n_turns:,}")

    impl, docs = [], []
    for fp in d["edits"]:
        base = fp.split("/")[-1].lower()
        (docs if (base.endswith((".md", ".html", ".txt", ".rst")) or "/docs/" in fp.lower()) else impl).append(fp)
    print("\n--- 1. what did the driver edit itself? ---")
    print("  implementation/config: %-4d %s" % (len(impl), "<-- RULE BROKEN" if impl else "ok"))
    for fp in collections.Counter(impl).most_common(6):
        print("       %3dx %s" % (fp[1], fp[0].split("/")[-1]))
    print("  documents (plan/spec/notes): %d" % len(docs))
    for fp, n in collections.Counter(docs).most_common(6):
        print("       %3dx %s" % (n, fp.split("/")[-1]))
    per_turn = u["cache_read_input_tokens"] // n_turns
    print("  NB: judge these by TURNS, not by bytes. Each edit is one driver turn at ~%s"
          % f"{per_turn:,} tokens")
    print("      -> the %d document edits above cost roughly %s cache-read between them"
          % (len(docs), f"{len(docs) * per_turn:,}"))
    print("      A legitimate correction still costs a turn; batching several into one is the lever.")

    print("\n--- 2. how was the end review run? ---")
    cr = d["tools"].get("Skill:code-review", 0)
    print("  harness /code-review invocations: %d   %s" % (cr, "<-- RULE BROKEN" if cr else "ok"))
    print("  Agent dispatches: %d" % len(d["agents"]))
    unset = [a for a in d["agents"] if a[0] == "<NOT SET>"]
    print("  dispatches with no explicit model: %d   %s" % (len(unset), "<-- RULE BROKEN" if unset else "ok"))
    for mdl, desc in d["agents"]:
        print("     model=%-12s %s" % (mdl, desc))

    print("\n--- context composition (share of transcript text) ---")
    tot = sum(d["chars"].values()) or 1
    for k, v in d["chars"].most_common(8):
        print("  %-22s %5.1f%%  %8s chars / %d" % (k[:22], 100 * v / tot, f"{v:,}", d["counts"][k]))

if __name__ == "__main__":
    main()
