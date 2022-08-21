from jira import xlsxTojson
from populator import populate_graph
from validator import validate_graph
if __name__ == "__main__":
    xlsxTojson()
    populate_graph()
    validate_graph()



