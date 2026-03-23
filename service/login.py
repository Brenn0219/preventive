def login_microsoft(page, email, senha):
    page.fill("input[type='email']", email)
    page.click("input[type='submit']")

    page.wait_for_timeout(2000)

    page.fill("input[type='password']", senha)
    page.click("input[type='submit']")

    page.wait_for_timeout(2000)

    # "Manter conectado?"
    try:
        page.click("input[id='idBtn_Back']")  # "Sim"
    except:
        pass