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
                    deploy_successful = True
                else:
                    self.log.error("Deployment failed")
                    deploy_successful = False
                if self.config.send_email_summary():
                    self.log.info("Sending email")
                    if deploy_successful:
                        self.emailer.send("Deployment completed successfully")
                    else:
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
                deploy_successful = True
            else:
                self.log.error("Deployment failed")
                deploy_successful = False
            if self.config.send_email_summary():
                self.log.info("Sending email")
                if deploy_successful:
                    self.emailer.send("Deployment completed successfully")
                else:
                    self.emailer.send("Deployment failed")
            else:
                self.log.info("Email disabled")




