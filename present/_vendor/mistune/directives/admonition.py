from .base import Directive


class Admonition(Directive):
    SUPPORTED_NAMES = {
        "attention",
        "caution",
        "danger",
        "error",
        "hint",
        "important",
        "note",
        "tip",
        "warning",
    }

    def parse(self, block, m, state):
        options = self.parse_options(m)
        if options:
            return {"type": "block_error", "raw": "Admonition has no options"}
        name = m.group("name")
        title = m.group("value")
        text = self.parse_text(m)

        rules = list(block.rules)
        rules.remove("directive")
        children = block.parse(text, state, rules)
        return {"type": "admonition", "children": children, "params": (name, title)}

    def __call__(self, md):
        for name in self.SUPPORTED_NAMES:
            self.register_directive(md, name)

        if md.renderer.NAME == "html":
            md.renderer.register("admonition", render_html_admonition)
        elif md.renderer.NAME == "ast":
            md.renderer.register("admonition", render_ast_admonition)


def render_html_admonition(text, name, title=None):
    html = '<section class="admonition ' + name + '">\n'
    if title:
        html += "<h1>" + title + "</h1>\n"
    if text:
        html += '<div class="admonition-text">\n' + text + "</div>\n"
    return html + "</section>\n"


def render_ast_admonition(children, name, title=None):
    return {
        "type": "admonition",
        "children": children,
        "name": name,
        "title": title,
    }
