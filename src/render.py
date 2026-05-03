from jinja2 import Environment, FileSystemLoader


def render_report(pack, output_path="output/report.html"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    html = template.render(pack=pack)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path