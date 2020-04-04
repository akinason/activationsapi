import json
import datetime
from workers.gearman import JSONGearmanWorker as GearmanWorker
from contrib.mailer import Message, mail, render_template

today = datetime.datetime.today()


class JobsHelper:

    def __init__(self):
        self.gm_worker = GearmanWorker(["localhost:4730"])
        self.gm_worker.register_task("mail.license_key", self._license_key_email)

        try:
            print('Gearman worker registered and ready for work.')
            self.gm_worker.work()
        except Exception as e:
            print('Gearman worker exiting with error:  %s' % e)

    def _license_key_email(self, gm_worker, gm_job):
        data = gm_job.data
        name = data.get('name', '')
        email = data.get('email', '')
        license_key = data.get('license_key', '')
        software = data.get("software", "")
        amount = data.get('amount', "")
        currency = data.get('currency', "")
        reference = data.get("reference", "")
        duration = data.get("duration", "")

        print(f"received  request to send license code to {name} <{email}> for order # {reference}")
        kwargs = {
            "amount": amount, "license_key": license_key, "current_year": today.year, "email": email,
            "software": software, "currency": currency, "duration": duration, "name": name
        }
        msg = Message(
            subject='License Key Purchase Successful.',
            recipients=[f"{name} <{email}>"]
        )
        # msg.html = render_template("license_key_email.html", **kwargs)
        msg.body = """
            Hello {name},
            Here is the information concerning your recent purchase:

            Order #     : {reference}
            Amount      : {amount} {currency}

            License Key : {license_key}
            Software    : {software}
            Duration    : {duration} days

            If you have any concerns, do well to contact our support team.

            Best Regards
            Activations Team
            """.format(
            name=name, reference=reference, amount=amount, currency=currency, license_key=license_key,
            software=software, duration=duration
        )
        try:
            r = mail.send(msg)
            return r
        except Exception as e:
            print('An error occurred during mail sending, here is the message: ', e)
