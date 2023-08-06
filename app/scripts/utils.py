from requests_ntlm import HttpNtlmAuth
from django.utils import timezone
from django.conf import settings
import requests


class BookingData:
    def __init__(self, destination):
        self.destination = destination
        self.ssrs_url = f"http://95.211.42.206/ReportServer_SSR?/{destination} Reports/Reservations/Bookings Data"
        self.ssrs_usr = settings.SSRS_USERNAME
        self.ssrs_pwd = settings.SSRS_PASSWORD

    def _format_ts(self, ts):
        self.ts_format = "%m/%d/%Y %H:%M:%S"
        timezone.activate("Asia/Dubai")

        return timezone.localtime(ts).strftime(self.ts_format)

    def set_params(self, date_fr, date_to):
        self.params = {
            "from:isnull": True,
            "to:isnull": True,
            "d1:isnull": True,
            "d2:isnull": True,
            "MaxProcessDate_from": self._format_ts(date_fr),
            "MaxProcessDate_to": self._format_ts(date_to),
            "ReportParameter1": True,
            "RefIDs:isnull": True,
            "rs:ParameterLanguage": "",
            "rs:Command": "Render",
            "rs:Format": "CSV",
            "rc:ItemPath": "table1",
        }

    def get(self, errors=None):
        try:
            response = requests.get(
                self.ssrs_url,
                params=self.params,
                stream=True,
                auth=HttpNtlmAuth(self.ssrs_usr, self.ssrs_pwd),
            )
            response.raise_for_status()

            data = response.content.decode("utf8")
            if len(data) > 424:
                return data
        except requests.exceptions.HTTPError as e:
            errors.append(f"HTTP error occurred: {str(e)}")
        except requests.exceptions.RequestException as e:
            errors.append(f"An error occurred while making the request: {str(e)}")

        return None
