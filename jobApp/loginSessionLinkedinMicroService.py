from linkedin.loginSessionLinkedin import LoginSessionLinkedCreator


if __name__ == "__main__":
    loginbot = LoginSessionLinkedCreator('jobApp/secrets/linkedin.json', headless=False)
    bot = loginbot.createLoginSession(True)
