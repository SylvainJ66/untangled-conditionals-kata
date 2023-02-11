class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        tests_passed = self.run_tests(project)
        deploy_successful = self.deploy(project, tests_passed)
        self.send_email_summary(deploy_successful, tests_passed)

    def send_email_summary(self, deploy_successful, tests_passed):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            if tests_passed:
                if deploy_successful:
                    self.emailer.send("Deployment completed successfully")
                else:
                    self.emailer.send("Deployment failed")
            else:
                self.emailer.send("Tests failed")
        else:
            self.log.info("Email disabled")

    def deploy(self, project, tests_passed):
        if tests_passed:
            if "success" == project.deploy():
                self.log.info("Deployment successful")
                deploy_successful = True
            else:
                self.log.error("Deployment failed")
                deploy_successful = False
        else:
            deploy_successful = False
        return deploy_successful

    def run_tests(self, project):
        if project.has_tests():
            if "success" == project.run_tests():
                self.log.info("Tests passed")
                tests_passed = True
            else:
                self.log.error("Tests failed")
                tests_passed = False
        else:
            self.log.info("No tests")
            tests_passed = True
        return tests_passed