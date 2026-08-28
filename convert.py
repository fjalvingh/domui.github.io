#!/usr/bin/env python3
"""Convert the Confluence export at SRC into the sigeto site layout under DST."""
import os, re, sys, shutil, posixpath
from urllib.parse import unquote

SRC = "/home/jal/domui-atlassian"
DST = "/home/jal/git/domui.github.io/site/content"
ROOT_DOC = "welcome-to-domui.md"          # becomes index.md
ROOT_DIR = "welcome-to-domui"             # its children become top level
DRY = "--apply" not in sys.argv

# ---------------------------------------------------------------- mapping
def all_md():
    for dp, dns, fns in os.walk(SRC):
        dns[:] = [d for d in dns if d != "attachments"]
        for fn in fns:
            if fn.endswith((".md", ".mdown")):
                yield os.path.relpath(os.path.join(dp, fn), SRC)

def dest_of(rel):
    """rel is a source path relative to SRC -> destination path relative to DST."""
    if rel == ROOT_DOC:
        return "index.md"
    base = rel[:-3] if rel.endswith(".md") else rel[:-6]
    parts = base.split("/")
    if parts[0] == ROOT_DIR:
        parts = parts[1:]
    return "/".join(parts + ["index.md"])

MD = sorted(all_md())
MAP = {rel: dest_of(rel) for rel in MD}

# sanity: no two sources map onto the same destination
rev = {}
for s, d in MAP.items():
    rev.setdefault(d, []).append(s)
collisions = {d: s for d, s in rev.items() if len(s) > 1}

# ---------------------------------------------------------------- rewriting
LINK_RE = re.compile(r'(!?)\[([^\]]*)\]\(([^)\s]*)(\s+"[^"]*")?\)')
ALERT = {"INFO": "i", "NOTE": "i", "TIP": "v", "IMPORTANT": "i",
         "WARNING": "w", "CAUTION": "w"}
EMOTICON = {"wink.png": ":wink:", "smile.png": ":smile:", "warning.png": ":warning:",
            "star_yellow.png": ":star:", "information.png": ":information_source:",
            "check.png": ":heavy_check_mark:", "sad.png": ":disappointed:",
            "thumbs_up.png": ":+1:", "thumbs_down.png": ":-1:", "tick.png": ":heavy_check_mark:"}

# drawio macros whose rendered PNG survived in the export
DRAWIO = {
    "welcome-to-domui/domui-state-management.md": "welcome-to-domui/attachments/conversationstate.png",
    "welcome-to-domui/data-binding-how-does-it-work.md": "welcome-to-domui/attachments/exampleform.png",
}

report = {"dangling": [], "attach": set(), "unknown_macro": 0, "emoticon": 0,
          "alerts": 0, "ext_att": [], "stripped_frag": []}

def convert(rel, text):
    srcdir = os.path.dirname(rel)                    # relative to SRC
    dstdir = os.path.dirname(MAP[rel])               # relative to DST
    copies = {}                                      # abs src file -> basename in dstdir

    # --- 1. GitHub alert blocks -> sigeto notification blocks
    out, i, lines = [], 0, text.split("\n")
    while i < len(lines):
        m = re.match(r'^>\s*\[!([A-Z]+)\]\s*$', lines[i])
        if m and m.group(1) in ALERT:
            flag = ALERT[m.group(1)]
            report["alerts"] += 1
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                body = re.sub(r'^>\s?', '', lines[i])
                out.append("!%s %s" % (flag, body) if body.strip() else "!%s " % flag)
                i += 1
        else:
            out.append(lines[i]); i += 1
    text = "\n".join(out)

    # --- 2a. restore drawio diagrams whose rendered png is in the export
    if rel in DRAWIO:
        png = DRAWIO[rel]
        text = re.sub(r'^!\[[^\]]*\]\(https://domui\\?\.atlassian\.net[^)]*name=drawio[^)]*\)[ \t]*$',
                      "![](%s)" % posixpath.relpath(png, srcdir), text, flags=re.M)

    # --- 2b. drop dead Confluence macro placeholders
    text, n = re.subn(r'^!\[[^\]]*\]\(https://domui\.atlassian\.net/wiki/plugins/servlet/'
                      r'confluence/placeholder/unknown-macro[^)]*\)\s*$\n?', '',
                      text, flags=re.M)
    report["unknown_macro"] += n

    # --- 3. links & images
    def repl(m):
        bang, label, target, title = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        # Confluence-hosted emoticon images -> emoji shortcodes
        if bang and target.startswith("https://domui.atlassian.net/"):
            name = target.rsplit("/", 1)[-1].split("?")[0]
            if name in EMOTICON:
                report["emoticon"] += 1
                return EMOTICON[name]
            return m.group(0)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith("//"):
            return m.group(0)                        # external / mailto / etc
        if target.startswith("#") or target == "":
            return m.group(0)                        # in-page anchor
        path, _, frag = target.partition("#")
        frag = ("#" + frag) if frag else ""
        abs_src = posixpath.normpath(posixpath.join(srcdir, unquote(path)))
        if abs_src.endswith((".md", ".mdown")):
            if abs_src in MAP:
                newpath = posixpath.relpath(MAP[abs_src], dstdir or ".")
                if frag:
                    # sigeto resolves an internal link without stripping the
                    # fragment, so an anchored .md link fails the build check.
                    report["stripped_frag"].append((rel, target))
                    frag = ""
            else:
                report["dangling"].append((rel, target))
                return label if not bang else m.group(0)   # drop the dead link
        else:
            disk = os.path.join(SRC, abs_src)
            if not os.path.isfile(disk):
                report["dangling"].append((rel, target))
                return label if not bang else m.group(0)
            base = os.path.basename(abs_src)
            # keep resource next to the page that uses it
            prev = copies.get(base)
            if prev and prev != disk:
                base = abs_src.replace("/", "-")     # unlikely; keep unique
            copies[base] = disk
            report["attach"].add(abs_src)
            newpath = base
        return "%s[%s](%s%s)%s" % (bang, label, newpath, frag, title)

    text = LINK_RE.sub(repl, text)

    # --- 4. tidy trailing whitespace-only lines Confluence loves
    text = re.sub(r'[ \t]+$', '', text, flags=re.M)
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + "\n"
    return text, copies

# ---------------------------------------------------------------- run
written = 0
for rel in MD:
    with open(os.path.join(SRC, rel), encoding="utf-8") as f:
        text = f.read()
    new, copies = convert(rel, text)
    dest = os.path.join(DST, MAP[rel])
    if not DRY:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(new)
        for base, disk in copies.items():
            shutil.copy2(disk, os.path.join(os.path.dirname(dest), base))
    written += 1

# ---------------------------------------------------------------- report
print("mode:            %s" % ("DRY RUN" if DRY else "APPLIED"))
print("markdown files:  %d" % written)
print("collisions:      %s" % (collisions or "none"))
print("attachments used:%d" % len(report["attach"]))
print("alerts:          %d converted" % report["alerts"])
print("macro stubs:     %d removed" % report["unknown_macro"])
print("emoticons:       %d -> emoji" % report["emoticon"])
print("stripped anchors:%d" % len(report["stripped_frag"]))
for r, t in report["stripped_frag"]:
    print("   %-55s -> %s" % (r, t))
print("dangling links:  %d" % len(report["dangling"]))
for r, t in report["dangling"]:
    print("   %-70s -> %s" % (r, t))

allatt = set()
for dp, dns, fns in os.walk(SRC):
    if os.path.basename(dp) == "attachments":
        for fn in fns:
            allatt.add(os.path.relpath(os.path.join(dp, fn), SRC))
unused = sorted(allatt - report["attach"])
print("unused attachments: %d" % len(unused))
for u in unused:
    print("   %s" % u)
