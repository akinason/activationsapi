import requests


class Flutterwave:

    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.base_url = "https://api.ravepay.co"

    def _post(self, url, params):
        headers = {"Content-Type": "application/json"}
        res = requests.post(url=url, data=params, headers=headers)

        try:
            return res.json()
        except Exception as e:
            return None

    def verify_payment(self, reference):
        """verifies the status of the payment so as to give value to the customer"""
        url = f"{self.base_url}/flwv3-pug/getpaidx/api/v2/verify"
        params = {"txref": reference, "secret": self.secret_key}
        res = self._post(url, params)

        if res is None:
            return {"success": False, "response": res}

        if res['status'] == "success":
            if res["data"]["status"] == "successful" and res["data"]["chargecode"] == "00":
                return {"success": True, "response": res}

        return {"success": False, "response": res}

