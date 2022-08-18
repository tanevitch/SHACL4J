import pandas as pd
import json


excel_sheet = pd.read_excel('data/DatasetStories.xlsx')
json_sheet = excel_sheet.to_json(orient='records')
with open("data/stories.json", "w", encoding='utf-8') as file:
    json.dump(json.loads(json_sheet), file, ensure_ascii=False, indent=4)



