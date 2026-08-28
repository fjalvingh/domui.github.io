# DomUI documentation site

The source of [domui.github.io](https://domui.github.io), the documentation for
the [DomUI framework](https://github.com/fjalvingh/domui). It is a static site,
generated from the Markdown below `site/content` by
[sigeto](https://github.com/fjalvingh/sitegenerator), which is checked out as
the `sitegenerator` submodule, and published to GitHub Pages by
`.github/workflows/build.yml` on every push.

## Building it locally

```
git submodule update --init
(cd sitegenerator && mvn -q clean package)
java -jar sitegenerator/target/sitegen.jar -i site -include https://demo.domui.org/
```

The result is written to `site/_output`; open its `index.html` in a browser.

`-include` is the base URL of the running demo application that the `!demo()`
tags in the documentation embed - a page containing one of those tags fails the
build without it. Point it at your own DomUI demo instance to check pages
against a local build instead.

## Committing

`sitegenerator/install-hooks.sh` installs git hooks that generate the site
before a commit or push is accepted, so a broken link never reaches the
published site. Give them the demo URL as well, or they fail on every `!demo()`
tag:

```
export SIGETO_ARGS='-include https://demo.domui.org/'
```

Move tracking is off (`#moves off` in `site/redirects.tsv`) while the
documentation is being restructured: pages are still being moved around and
their old URLs are not worth keeping. Once the structure has settled, replace
that line with the `#moves since <commit>` line the build prints, and from then
on every move is recorded and the old URLs keep working.
