import datetime

def generate_html_report(violations):
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: #333; }}
            .violation {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }}
            .no-violations {{ font-weight: bold; color: green; }}
        </style>
    </head>
    <body>
        <h1>Vaylo – Compliance Violations Report</h1>
        <p><strong>Generated:</strong> {today}</p>
    """

    if not violations:
        html += "<p class='no-violations'>🎉 No violations found in this data.</p>"
    else:
        for v in violations:
            rule = v.get("rule", "-")
            field = v.get("field", "-")
            name = v.get("record", {}).get("name", "-")
            error = v.get("error", "N/A")

            html += f"""
            <div class="violation">
                <strong>Rule:</strong> {rule}<br>
                <strong>Field:</strong> {field}<br>
                <strong>Name:</strong> {name}<br>
                <strong>Error:</strong> {error}
            </div>
            """

    html += "</body></html>"
    return html.encode("utf-8")
