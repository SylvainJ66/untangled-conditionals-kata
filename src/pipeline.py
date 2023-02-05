class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        if project.has_tests():
            if "success" == project.run_tests():
                self.log.info("Tests passed")
                if "success" == project.deploy():
                    self.log.info("Deployment successful")
                    self.send_email("Deployment completed successfully")
                else:
                    self.log.error("Deployment failed")
                    if self.config.send_email_summary():
                        self.log.info("Sending email")
                        self.emailer.send("Deployment failed")
                    else:
                        self.log.info("Email disabled")
            else:
                self.log.error("Tests failed")
                if self.config.send_email_summary():
                    self.log.info("Sending email")
                    self.emailer.send("Tests failed")
                else:
                    self.log.info("Email disabled")
        else:
            self.log.info("No tests")
            if "success" == project.deploy():
                self.log.info("Deployment successful")
                self.send_email("Deployment completed successfully")
            else:
                self.log.error("Deployment failed")
                self.send_email("Deployment failed")

    def send_email(self, email_message):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(email_message)
        else:
            self.log.info("Email disabled")
