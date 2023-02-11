class TestFailed(Exception):
    pass


class DeploymentFailed(Exception):
    pass


class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        try:
            self.run_tests(project)
            self.deploy(project)
        except TestFailed:
            self.send_email_summary("Tests failed")
        except DeploymentFailed:
            self.send_email_summary("Deployment failed")
        else:
            self.send_email_summary("Deployment completed successfully")

    def send_email_summary(self, summary):
        if not self.config.send_email_summary():
            self.log.info("Email disabled")
            return
        self.log.info("Sending email")
        self.emailer.send(summary)

    def deploy(self, project):
        if "success" != project.deploy():
            self.log.error("Deployment failed")
            raise DeploymentFailed
        self.log.info("Deployment successful")
        return

    def run_tests(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            return
        if "success" == project.run_tests():
            self.log.info("Tests passed")
            return
        self.log.error("Tests failed")
        raise TestFailed
