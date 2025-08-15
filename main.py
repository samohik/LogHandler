import argparse
import json
import re
from typing import List, Any, final
from tabulate import tabulate


class LogHandler:
    def __init__(
        self, file: str | List[str,], report: str = "average", date: str | None = None
    ):
        self.file = file
        self.report = report
        self.date = date
        self.data = []

    def read_file(self, file) -> None:
        with open(file, "r") as f:
            for row in f:
                obj = json.loads(row)
                self.data.append(obj)

    def data_handler(self, unique_url):
        data_by_url = []
        for url in unique_url:
            structured_data = {
                "url": None,
                "timestamp": [],
                "response_time": [],
                "http_user_agent": [],
            }
            for item in self.data:
                if self.date:
                    regexp = r"(\d{4})-(\d{2})-(\d{2})"
                    match = re.findall(regexp, item["@timestamp"])
                    re_date = match[0]
                    date_from_log = f"{re_date[0]}-{re_date[2]}-{re_date[1]}"

                    if item["url"] == url and date_from_log == self.date:
                        self.json_handler(item, structured_data)
                else:
                    if item["url"] == url:
                        self.json_handler(item, structured_data)

            if structured_data["url"]:
                data_by_url.append(structured_data)

        return data_by_url

    def result_handler(self, data_by_url):
        data = []
        info_response = "avg_response_time"

        for id_item, val in enumerate(data_by_url):
            res_time = val["response_time"]
            try:
                avg_response = sum(res_time) / len(res_time)
            except ZeroDivisionError as e:
                avg_response = sum(res_time)

            if self.report == "max":
                avg_response = max(res_time)
                info_response = "max_response_time"

            elif self.report == "min":
                avg_response = min(res_time)
                info_response = "min_response_time"

            data_to_tabulate = [
                val["url"],
                len(res_time),
                format(
                    avg_response,
                    ".3f",
                ),
            ]
            if self.date:
                data_to_tabulate.append(
                    self.date,
                )

            data.append(data_to_tabulate)

        sorted_result = []
        for id_item, item in enumerate(sorted(data, key=lambda a: a[1], reverse=True)):
            item.insert(0, id_item)
            sorted_result.append(item)
        if self.date:
            print(
                tabulate(
                    sorted_result, headers=["id", "url", "total", info_response, "date"]
                )
            )
        else:
            print(
                tabulate(sorted_result, headers=["id", "url", "total", info_response])
            )

        return sorted_result

    def unique_url(self):
        unique_url = []
        for item in self.data:

            i = item["url"]
            if i in unique_url:
                continue
            else:
                unique_url.append(i)
        return unique_url

    def main(self):
        for file in self.file:
            try:
                self.read_file(file)
            except Exception as e:
                print(f"Path {file} is not correct.")

        unique_url = self.unique_url()
        data = self.data_handler(unique_url)
        result = self.result_handler(data)

        return result

    @staticmethod
    def json_handler(item, data):
        data["url"] = item["url"]
        data["timestamp"].append(item["@timestamp"])
        data["response_time"].append(item["response_time"])
        data["http_user_agent"].append(item["http_user_agent"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", nargs="+", help="Path to log file")
    parser.add_argument("--date", help="Search all occurrences by time")
    parser.add_argument("--report", help="Parameter for response time")

    args = parser.parse_args()

    a = LogHandler(
        file=args.file,
        report=args.report,
        date=args.date,
    )
    a.main()
