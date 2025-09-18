# ui.py
from flask import render_template_string

def render_page(title: str, body_html: str, status: int = 200):
    html = f"""<!doctype html>
<html lang="fi">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 2rem; line-height: 1.5; }}
    a {{ text-decoration: none; }}
    .timer {{ font-weight: 600; }}
  </style>
</head>
<body>
  {{% include "_nav.html" %}}
  {body_html}
</body>
</html>"""
    return render_template_string(html), status

def render_error_with_link(message: str, href: str, link_text: str, status: int = 400):
    body = f"""
    <h1>{message}</h1>
    <p><a href="{href}">{link_text}</a></p>
    """
    return render_page("Virhe", body, status=status)

def render_success_redirect_with_countdown(message: str, seconds: int, href: str, link_text: str):
    body = f"""
    <h1>{message}</h1>
    <p>Siirrytään eteenpäin <span id="sec" class="timer">{seconds}</span> sekunnissa…</p>
    <p><a href="{href}">{link_text}</a></p>
    <script>
      (function() {{
        var s = {seconds};
        var el = document.getElementById('sec');
        var t = setInterval(function() {{
          s -= 1;
          if (s <= 0) {{ clearInterval(t); return; }}
          el.textContent = s;
        }}, 1000);
      }})();
    </script>
    """
    page, status = render_page("Onnistui", body, status=200)
    page = page.replace("</head>", f'<meta http-equiv="refresh" content="{seconds};url={href}" />\n</head>')
    return page
