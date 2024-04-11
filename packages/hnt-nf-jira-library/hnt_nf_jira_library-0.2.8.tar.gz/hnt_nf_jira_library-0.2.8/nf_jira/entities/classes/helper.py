import json
from os import getcwd, makedirs, path

class JsonHelper:

    def save_json(self, filename, json_data):

        path_dir = path.join(getcwd(), 'output/json')
        if not path.exists(path_dir):
            makedirs(path_dir)

        with open(f"./output/json/{filename}.json", "w", encoding="utf-8") as json_file:
            json.dump( json_data, json_file, ensure_ascii=False, indent=4)

class JiraFieldsHelper:

    def remove_null_fields(self, fields):
        fields_data_without_nulls = {}

        for key, value in fields.items():
            if value is not None:
                fields_data_without_nulls[key] = value

        return fields_data_without_nulls
    
    def _rename_fields(self, fields):
        fields = self._fields
        new_fields_data = {}

        for key, value in self._jira_fields.items():
            if value in fields:
                if "text" in fields[value]:
                    new_value = fields[value].get("text")
                elif "date" in fields[value]:
                    new_value = fields[value].get("date")
                elif "value" in fields[value]:
                    new_value = fields[value].get("value")
                else:
                    new_value = fields[value]

                new_fields_data[key] = new_value

        return new_fields_data