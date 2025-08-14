import json
from typing import List
from tabulate import tabulate


class LogHandler:
    def __init__(
            self,
            file: str| List[str, ],
            report: str = "Test",
            date: str| None = None
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

    def main(self) -> None:
        for file in self.file:
            self.read_file(file)
        unique_url = self.unique_url()
        self.data_ex(unique_url)

    def data_ex(self, unique_url):
        data_by_url = []
        for url in unique_url:
            j_data = {
                "url": str,
                "timestamp": [],
                "response_time": [],
                "http_user_agent": [],
            }
            for item in self.data:
                if item["url"] == url:
                    j_data["url"] = item["url"]
                    j_data["timestamp"].append(item["@timestamp"])
                    j_data["response_time"].append(item["response_time"])
                    j_data["http_user_agent"].append(item["http_user_agent"])
            data_by_url.append(j_data)

        result = []
        for id_item, val in enumerate(data_by_url):
            res_time = val["response_time"]
            avg_response = sum(res_time) / len(res_time)

            data_to_tabulate = [id_item, val["url"], len(res_time), format(avg_response, ".3f")]
            result.append(data_to_tabulate)

        print(tabulate(
            sorted(result, key=lambda a: a[2], reverse=True),
            headers=["id", "url", "total", "avg_response_time"]
        ))

    def unique_url(self):
        unique_url = []
        for item in self.data:
            i = item["url"]

            if i in unique_url:
                continue
            else:
                unique_url.append(i)
        return unique_url


if __name__ == "__main__":
    name_file1 = "examples/example1.log"
    name_file2 = "examples/example2.log"

    a = LogHandler(file=[name_file1, name_file2], )
    a.main()
    pass
