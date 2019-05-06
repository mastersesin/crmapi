returnMsg = {
    "Register Success": {
        "code": 1, "msg": "User created successfully."
    },
    "Phone Duplicated": {
        "code": 2, "msg": "Phone number has been used by another user."
    },
    "Email Duplicated": {
        "code": 3, "msg": "Email address has been used by another user."
    },
    "Username Duplicated": {
        "code": 4, "msg": "Username has been used by another user."
    },
    "Username or Password Incorrect": {
        "code": 5, "msg": "Username or Password Incorrect"
    },
    "Return Token": {
        "code": 6, "msg": ""  # Dynamic msg so not show here
    },
    "400": {
        "code": 7, "msg": "Required form is missing or not in correct format"
    },
    "Email Not In Correct Format": {
        "code": 8, "msg": "Email not in correct format."
    },
    "Password change successfully": {
        "code": 9, "msg": "Password has changed successfully."
    },
    "Return Transaction List": {
        "code": 10, "msg": {}  # Dynamic msg so not show here
    },
    "Return Card Info": {
        "code": 11, "msg": {}  # Dynamic msg so not show here
    },
    "Return Coupons Of Card": {
        "code": 12, "msg": {}  # Dynamic msg so not show here
    },
    "Token Expired": {
        "code": 13, "msg": "Token Expired"
    }
}


class returnMsgTest():
    def __init__(self):
        self.register_success = {"code": 1, "msg": "User created successfully."}
        self.username_or_password_incorrect = {"code": 5, "msg": "Username or Password Incorrect"}
        self.return_token = {"code": 6, "msg": ""}  # Dynamic msg so not show here
        self.four_hundred = {"code": 7, "msg": "Required form is missing or not in correct format"}
        self.password_change_successfully = {"code": 9, "msg": "Password has changed successfully."}
        self.return_transaction_list = {"code": 10, "msg": {}}
        self.return_card_info = {"code": 11, "msg": {}}
        self.token_expired = {"code": 13, "msg": "Token Expired"}
        self.return_coupons_of_card = {"code": 12, "msg": {}}
        self.logout = {"code": 13, "msg": "Logout successfully."}

    def register_success(self):
        return self.register_success

    def username_or_password_incorrect(self):
        return self.username_or_password_incorrect

    def return_token(self):
        return self.return_token

    def four_hundred(self):
        return self.four_hundred

    def password_change_successfully(self):
        return self.password_change_successfully

    def return_transaction_list(self):
        return self.return_transaction_list

    def return_card_info(self):
        return self.return_card_info

    def token_expired(self):
        return self.token_expired

    def logout(self):
        return self.logout
