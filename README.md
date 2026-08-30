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
java -jar sitegenerator/target/sitegen.jar -i site
```

The result is written to `site/_output`; open its `index.html` in a browser.

`site/variables.properties` holds what the `${name}` variables in the
documentation stand for, `demo` among them: the base URL of the running demo
application that the `!demo()` tags embed. To check the pages against your own
DomUI demo instance instead, override it for that build:

```
java -jar sitegenerator/target/sitegen.jar -i site -Ddemo=http://localhost:8088/demo/
```

## Committing

`sitegenerator/install-hooks.sh` installs git hooks that generate the site
before a commit or push is accepted, so a broken link never reaches the
published site. They need nothing else: the demo URL and every other variable
come from `site/variables.properties`.

Move tracking is off (`#moves off` in `site/redirects.tsv`) while the
documentation is being restructured: pages are still being moved around and
their old URLs are not worth keeping. Once the structure has settled, replace
that line with the `#moves since <commit>` line the build prints, and from then
on every move is recorded and the old URLs keep working.
