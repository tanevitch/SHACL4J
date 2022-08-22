from src.jira import xlsxTojson
from src.populator import populate_graph
from src.validator import validate_graph
if __name__ == "__main__":
    # xlsxTojson()
    populate_graph()
    validate_graph()



