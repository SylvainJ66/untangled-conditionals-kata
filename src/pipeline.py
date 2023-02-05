class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            self.deploy(project)
            return
        if project.run_tests() != "success":
            self.log.error("Tests failed")
            self.send_email("Tests failed")
            return
        self.log.info("Tests passed")
        self.deploy(project)

    def deploy(self, project):
        if project.deploy() != "success":
            self.log.error("Deployment failed")
            self.send_email("Deployment failed")
            return
        self.log.info("Deployment successful")
        self.send_email("Deployment completed successfully")

    def send_email(self, message):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(message)
        else:
            self.log.info("Email disabled")