class LoginUser:
    def __init__(self, authentication_service):
        self.authentication_service = authentication_service

    def execute(self, email, password):
        # Delegate authentication to the service
        return self.authentication_service.authenticate(email, password)
