from flask import render_template_string, redirect

def render_page(title: str, body_html: str, status: int = 200):
    html = f"""<!doctype html>
<html lang="fi">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
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

def render_success_with_link(message: str, href: str, link_text: str):
    body = f"""
    <h1>{message}</h1>
    <p><a href="{href}">{link_text}</a></p>
    """
    return render_page("Onnistui", body, status=200)

def handle_not_found(resource_name: str = "resurssi"):
    return render_error_with_link(f"VIRHE: {resource_name} ei löydy", "/", "Takaisin etusivulle", status=404)

def handle_forbidden(message: str = "Ei käyttöoikeutta"):
    return render_error_with_link(f"VIRHE: {message}", "/", "Takaisin etusivulle", status=403)

def handle_login_required():
    return redirect("/login")

def handle_validation_error(message: str, redirect_url: str, link_text: str):
    return render_error_with_link(f"VIRHE: {message}", redirect_url, link_text)

def handle_authentication_error():
    return render_error_with_link("VIRHE: väärä tunnus tai salasana", "/login", "Palaa kirjautumiseen", status=401)

def handle_duplicate_user_error():
    return render_error_with_link("VIRHE: tunnus on jo varattu", "/create", "Palaa rekisteröitymiseen", status=409)

def handle_password_mismatch_error():
    return render_error_with_link("VIRHE: salasanat eivät ole samat", "/create", "Palaa rekisteröitymiseen")

def handle_display_name_too_long_error():
    return render_error_with_link("VIRHE: näyttönimi on liian pitkä (max 100 merkkiä)", "/profile", "Palaa profiiliin")

def handle_message_error(message: str):
    return render_error_with_link(f"VIRHE: {message}", "/messages", "Takaisin viesteihin")

def handle_thread_not_found():
    return render_error_with_link("VIRHE: keskustelua ei löydy", "/messages", "Takaisin viesteihin", status=404)

def handle_thread_access_denied():
    return render_error_with_link("VIRHE: ei käyttöoikeutta tähän keskusteluun", "/messages", "Takaisin viesteihin", status=403)

def handle_empty_message_error():
    return render_error_with_link("VIRHE: viesti ei voi olla tyhjä", "/messages", "Takaisin viesteihin")

def handle_recipient_required_error():
    return render_error_with_link("VIRHE: vastaanottaja ja viesti ovat pakollisia", "/messages/new", "Takaisin")

def handle_recipient_not_found_error():
    return render_error_with_link("VIRHE: vastaanottajaa ei löydy", "/messages/new", "Takaisin")

def handle_self_message_error():
    return render_error_with_link("VIRHE: et voi lähettää viestiä itsellesi", "/messages/new", "Takaisin")

def handle_announcement_not_found():
    return render_error_with_link("VIRHE: ilmoitusta ei löydy", "/", "Takaisin etusivulle", status=404)

def handle_announcement_forbidden(action: str = "käsitellä"):
    return render_error_with_link(f"VIRHE: ei oikeutta {action} tätä ilmoitusta", "/", "Takaisin etusivulle", status=403)
