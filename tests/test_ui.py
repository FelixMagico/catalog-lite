"""Test della interfaccia con Playwright: un browser vero clicca sul sito."""
from playwright.sync_api import expect


def login(page, username, password):
    page.goto("/auth/login")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button:has-text('Accedi')")


def test_login_with_wrong_password_shows_error(page):
    login(page, "admin", "sbagliata")
    expect(page.locator(".flash")).to_have_text("Username o password errati.")


def test_request_and_approval_flow(page):
    # 1. mi registro, accedo e chiedo VLC
    page.goto("/auth/register")
    page.fill("input[name=username]", "mario")
    page.fill("input[name=password]", "password1")
    page.click("button:has-text('Crea account')")
    login(page, "mario", "password1")
    page.click("tr:has-text('VLC') button")
    expect(page.locator("tr:has-text('VLC')")).to_contain_text("In attesa")

    # 2. l'admin approva
    page.click("button:has-text('Esci')")
    login(page, "admin", "admin123")
    page.goto("/admin/")
    expect(page.locator("tr:has-text('mario')")).to_contain_text("VLC")
    page.click("button:has-text('Approva')")
    expect(page.locator("main")).to_contain_text("Nessuna richiesta in attesa")

    # 3. l'utente vede la richiesta approvata
    page.click("button:has-text('Esci')")
    login(page, "mario", "password1")
    expect(page.locator("tr:has-text('VLC')")).to_contain_text("Approvata")


def test_normal_user_cannot_open_admin_page(page):
    page.goto("/auth/register")
    page.fill("input[name=username]", "luca")
    page.fill("input[name=password]", "password1")
    page.click("button:has-text('Crea account')")
    login(page, "luca", "password1")
    response = page.goto("/admin/")
    assert response.status == 403



