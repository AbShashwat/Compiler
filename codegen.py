def resolve_value(instr, pool):

    if "value" in instr:
        value = instr["value"]

        if isinstance(value, dict):
            resolved = {}

            for k, v in value.items():
                if k.endswith("_ref"):
                    resolved[k.replace("_ref", "")] = pool.get(v, "")
                else:
                    resolved[k] = v

            return resolved

        return value

    return pool.get(instr.get("value_ref"), "")


def generate_markdown(ir, pool):

    md = []

    for instr in ir:

        t = instr["type"]
        v = resolve_value(instr, pool)

        if t == "HEADER":
            md.append(f"# {v}")

        elif t == "IMAGE":
            md.append(f"![{v.get('alt', '')}]({v.get('src', '')})")

        elif t == "LINK":
            md.append(f"[{v.get('label', '')}]({v.get('url', '')})")

        elif t == "FOOTER":
            md.append(f"\n---\n{v}")

        else:
            md.append(f"<!-- Unsupported: {t} -->")

    return "\n\n".join(md)


def generate_html(ir, pool, errors):

    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head><title>Generated Page</title></head>",
        "<body>"
    ]

    for instr in ir:

        t = instr["type"]
        v = resolve_value(instr, pool)

        if t == "HEADER":
            html.append(f"<h1>{v}</h1>")

        elif t == "IMAGE":
            html.append(f"<img src='{v.get('src', '')}' alt='{v.get('alt', '')}'>")

        elif t == "LINK":
            html.append(f"<a href='{v.get('url', '')}' target='_blank'>{v.get('label', '')}</a>")

        elif t == "FOOTER":
            html.append(f"<footer>{v}</footer>")

    for err in errors:
        html.append(f"<div style='color:red'>Error: {err}</div>")

    html.append("</body></html>")

    return "\n".join(html)