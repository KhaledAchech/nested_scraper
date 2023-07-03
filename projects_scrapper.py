import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.eib.org/en/products/mandates-partnerships/efsi/efsi-projects/index.htm?q=&sortColumn=boardDate&sortDir=desc&pageNumber=0&itemPerPage=25&pageable=true&language=EN&defaultLanguage=EN&abstractProject=true&orabstractProject=true&yearFrom=&yearTo=2021&orCountries=true&orSectors=true"
response = requests.get(url)


soup = BeautifulSoup(response.content, "html.parser")
project_links = soup.find_all("a", class_="result-row")

descriptions = []
additionality_impacts = []
objectives = []
services = []   
proposed_eib_finances = []
total_costs = []

for link in project_links:
    project_url = "https://www.eib.org" + link["href"]
    project_response = requests.get(project_url)
    project_soup = BeautifulSoup(project_response.content, "html.parser")

    description = project_soup.find("div", class_="content-body project-description")
    additionality_impact = project_soup.find("div", class_="content-body project-additionality-impact")
    objective = project_soup.find("div", class_="content-body project-objective")
    service = project_soup.find("div", class_="content-body project-service")
    proposed_eib_finance = project_soup.find("div", class_="content-body project-proposed-eib-finance")
    total_cost = project_soup.find("div", class_="content-body project-total-cost")

    descriptions.append(description.get_text(strip=True) if description else "")
    additionality_impacts.append(additionality_impact.get_text(strip=True) if additionality_impact else "")
    objectives.append(objective.get_text(strip=True) if objective else "")
    services.append(service.get_text(strip=True) if service else "")
    proposed_eib_finances.append(proposed_eib_finance.get_text(strip=True) if proposed_eib_finance else "")
    total_costs.append(total_cost.get_text(strip=True) if total_cost else "")

data = {
    "Description": descriptions,
    "Additionality and Impact": additionality_impacts,
    "Objectives": objectives,
    "Services": services,
    "Proposed EIB Finance": proposed_eib_finances,
    "Total Cost": total_costs,
}
df = pd.DataFrame(data)
df.to_excel("project_details.xlsx", index=False)
