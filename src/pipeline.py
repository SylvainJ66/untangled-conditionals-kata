NO_TESTS = "No tests"
TESTS_PASSED = "Tests passed"
DEPLOYMENT_FAILED = "Deployment failed"
COMPLETED_SUCCESSFULLY = "Deployment completed successfully"
DEPLOYMENT_SUCCESSFUL = "Deployment successful"
LOG_FAILED = "Tests failed"


class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        if project.has_tests():
            if "success" != project.run_tests():
                self.log.error(LOG_FAILED)
                self.send_email(LOG_FAILED)
                return

            self.log.info(TESTS_PASSED)
            if "success" == project.deploy():
                self.log.info(DEPLOYMENT_SUCCESSFUL)
                self.send_email(COMPLETED_SUCCESSFULLY)
            else:
                self.log.error(DEPLOYMENT_FAILED)
                self.send_email(DEPLOYMENT_FAILED)
        else:
            self.log.info(NO_TESTS)
            if "success" == project.deploy():
                self.log.info(DEPLOYMENT_SUCCESSFUL)
                self.send_email(COMPLETED_SUCCESSFULLY)
            else:
                self.log.error(DEPLOYMENT_FAILED)
                self.send_email(DEPLOYMENT_FAILED)

    def send_email(self, email_message):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(email_message)
        else:
            self.log.info("Email disabled")
