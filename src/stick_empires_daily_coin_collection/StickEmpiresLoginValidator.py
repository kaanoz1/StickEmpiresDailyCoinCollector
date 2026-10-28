class StickEmpiresLoginValidator:


    @staticmethod
    def is_login_validated_by_server(login_response: bytes) -> bool:
        if b"FS_NEW_LOGIN_NAME" in login_response:
            return True
        else:
            return False