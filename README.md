<h1 align="center">Financial report data analysis</h1>

<h2>Description</h2>
Develop a consolidated report to track revenue, profit, employee performance daily, thereby painting a financial picture and proposing development strategies for the company. 

## 📑 Table of Contents

- [📊 Overview](#-overview)
- [🎯 Features](#-features)
- [🛠️ Installation](#️-installation)
- [🚀 Quick Start](#-quick-start)
- [📈 Data Sources](#-data-sources)
- [🔍 Analysis Methods](#-analysis-methods)
- [📋 Flowchart](#-report-types)
- [💡 How i do this project ?](#-project-method)
- [📊 Visualization](#-visualization)
- [⚙️ Configuration](#️-configuration)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)

<h2> Overview </h2>
This is my personal project with the goal of becoming a data analyst intern. Assuming a scenario where the Finance Department requested me to create two reports using the company's data — a summary report and an employee performance report — I utilized PostgreSQL and Power BI to complete the task. In addition to generating these two reports, I also visualized the data to help the management team better monitor and manage the company's overall performance.

<h2> Features</h2>

- Daily data processing is automated using a stored procedure.
- The data is organized using the star schema model.
- The procedure runs at high speed and stores all historical data.
- The reports are visually intuitive and directly connected to the database, automatically updating whenever the database changes.
  
<h2> Installation</h2>



<h2> Flowchart</h2>

![flowchart.drawio.png](https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/flowchart.drawio.png)


<h2> How i do this project ? </h2>

<h3> Step 1: Preprocessing data </h3>

- Fist of all, i need to clearly understand what my data represents, the meaning of each column, and the business context behind them.
- Next, the dimension tables were created based on the fact raw tables.
- After that, I processed the fact table by selecting the necessary columns, removing the irrelevant ones, transforming values based onto better fit my objectives.
- Finally, I encapsulated the entire process into a single procedure, so that by simply running it, all steps are executed automatically.

<h3> Step 2: Build a summary report.</h3>

- 


<h2> Contributing</h2>

Since this is my very first project, there are certainly unavoidable mistakes. If you have any feedback, I would sincerely appreciate it with all my gratitude.



### 🗄️ Databases
![PostgreSQL](https://img.shields.io/badge/POSTGRESQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### 🔧 Tools
![Power BI](https://img.shields.io/badge/POWER%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)




- **Context**: Receive request from the finance department to prepare 2 daily reports and finalize daily inventory numbers, write into an Excel file
- **Tech stack:** Power BI, PostgreSQL
- **How i do:** First, I process data using PostgreSQL, building dim and fact tables based on the star schema, and writing a procedure to continuously update data when new data is added. Next, I visualize the data using Power BI, presenting it with meaningful charts to explain the company's financial situation, thereby assisting the BOD in management and proposing development strategies for the company.
- **What i achieved**: Proficient in Power BI, skilled in DAX, capable of organizing and processing data using PostgreSQL to create continuously updated reports. 

