import json

from http_content_parser.generate_api_file import GenerateApiFile


def test_curl():
    gaf = GenerateApiFile()
    # with open("./postman.json", "r") as f:
    #     json_dict = json.load(f)
    # gaf.produce_api_yaml_for_postman(json_dict, "./test.yaml")
    curl_file = ""
    res = gaf.produce_api_yaml_for_curl(curl_file=curl_file, yaml_file="api.yaml")


def test_for():
    data = {"name": "John", "age": 30, "city": "New York"}
    temp = '{    "job_id":{{job_id}},    "product_id": 4,    "local_user_id": 0}'
    temp = json.dumps(data)
    temp = json.loads(temp)
    print(temp)
