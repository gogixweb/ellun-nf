import configparser
import os
import sys
import datetime
import urllib.parse
from decimal import Decimal
from pathlib import Path
from typing import Optional


def format_brl(value):
    return (
        "{:0,.2f}".format(value).replace(",", " ").replace(".", ",").replace(" ", ".")
    )


class NFSubmission:
    amount: str
    company: str
    client: str
    company_data: Optional[str]
    month: Optional[str]
    services: Optional[str]
    transfer_fee: Decimal

    def __init__(self, company, client, amount, services, tax, transfer_fee):
        self.company = company
        self.client = client
        self.tax = tax
        self.transfer_fee = transfer_fee
        self.company_data = "N/A"
        self.month = datetime.datetime.now().strftime("%m/%Y")

        self._handle_values(amount, services)

    def _handle_values(self, amount, services):
        percent_fee = amount * self.transfer_fee / 100
        amount_before_fees = amount - percent_fee

        final_amount = (amount_before_fees + percent_fee) * amount / amount_before_fees
        self.amount = final_amount

        total_share = 0
        for _, ratio in services:
            total_share += float(ratio)

        services_with_amounts = []
        for service, ratio in services:
            services_with_amounts.append(
                (service, round(self.amount * float(ratio) * 100 / total_share))
            )
        self.services = services_with_amounts

    @property
    def tax_url(self):
        if self.tax == "LP":
            return (
                "https://docs.google.com/forms/d/1dBGShgdzpmT59FvhHWv8JAszQnS6Vxz0IvYNrNa5Vbk/"
                "viewform?edit_requested=true"
            )
        else:
            return (
                "https://docs.google.com/forms/d/e/1FAIpQLScka6qGMHsIpZgXh8YyMirELA9QFVz53EsRzNKMQkRG7QJAuw/"
                "viewform?edit_requested=true"
            )

    @property
    def services_formatted(self):
        return ", ".join(
            f"{service} - R$ {format_brl(value / 100)}"
            for service, value in self.services
        )

    @property
    def amount_formatted(self):
        return f"{self.amount:.2f}"

    def __str__(self):
        text = (
            f"{self.company}\n"
            f"{self.client}\n"
            f"{self.company_data}\n"
            f"{self.month}\n"
            f"{self.services_formatted}\n"
            f"{self.amount_formatted}"
        )

        return text

    @property
    def url(self):
        entries_map = {
            self.company: "1333919565" if self.tax == "LP" else "499001639",
            self.company_data: "1237336356" if self.tax == "LP" else "8368098",
            self.month: "1300311341" if self.tax == "LP" else "2082727643",
            self.services_formatted: "1014169847" if self.tax == "LP" else "1722216398",
            self.amount_formatted: "1026240558" if self.tax == "LP" else "1139889955",
        }

        url = self.tax_url
        for attribute, entry in entries_map.items():
            url += f"&entry.{entry}={urllib.parse.quote_plus(str(attribute))}"

        client = "1185762637" if self.tax == "LP" else "335116049"
        url += f'&entry.{client}={urllib.parse.quote_plus("Para a mesma empresa da nota anterior")}'
        return url


def main():
    ini_file = os.environ.get(
        "ELLUNNF_INI", Path(os.path.dirname(__file__)) / "ellunnf.sample.ini"
    )

    config = configparser.ConfigParser()
    config.read(ini_file)

    company = config["company"]["name"]
    tax = config["company"]["tax"]

    client = config["client"]["name"]
    transfer_fee = config.getfloat("client", "transfer_fee")

    services = list(config["services"].items())

    if len(sys.argv) < 2:
        sys.exit("You need to specify the value")

    try:
        amount = float(sys.argv[1].replace(",", ""))
    except (IndexError, ValueError):
        sys.exit("You need a number for the amount")

    try:
        transfer_fee = float(sys.argv[2])
    except:
        pass

    submission = NFSubmission(
        company=company,
        client=client,
        amount=amount,
        services=services,
        tax=tax,
        transfer_fee=transfer_fee,
    )
    print(submission)
    print(submission.url)


if __name__ == "__main__":
    main()
