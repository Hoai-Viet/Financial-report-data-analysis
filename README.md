<h1 align="center">Financial report data analysis</h1>

<h2>Description</h2>
Develop a consolidated report to track revenue, profit, employee performance daily, thereby painting a financial picture and proposing development strategies for the company. 

## 📑 Table of Contents

- [📊 Overview](#-overview)
- [🎯 Features](#-features)
- [💡 How i do this project ?](#-project-method)
- [📋 Flowchart](#-report-types)
- [📊 Visualization](#-visualization)
- [🛠️ Installation](#️-installation)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)

<h2> 📊 Overview </h2>
This is my personal project with the goal of becoming a data analyst intern. Assuming a scenario where the Finance Department requested me to create two reports using the company's data — a summary report and an employee performance report — I utilized PostgreSQL and Power BI to complete the task. In addition to generating these two reports, I also visualized the data to help the management team better monitor and manage the company's overall performance.

<h2> 🎯 Features</h2>

- Daily data processing is automated using a stored procedure.
- The data is organized using the star schema model.
- The procedure runs at high speed and stores all historical data.
- The reports are visually intuitive and directly connected to the database, automatically updating whenever the database changes.
  
<h2> 💡 How i do this project ? </h2>

<h3> Step 1: Preprocessing data </h3>

- Fist of all, i need to clearly understand what my data represents, the meaning of each column, and the business context behind them.
- Next, the dimension tables were created based on the fact raw tables.
- After that, I processed the fact table by selecting the necessary columns, removing the irrelevant ones, transforming values based onto better fit my objectives.
- Finally, I encapsulated the entire process into a single procedure, so that by simply running it, all steps are executed automatically.

<h3> Step 2: Build a summary report.</h3>

- After understanding the business logic and the allocation method of each expense, I created temporary tables to store the information at each calculation step.
- The temporary tables include:
  - tmp_report_gl_by_area_monthly: the original funds allocated from the head office at the end of the period.
  - tmp_total_dbt_staff_each_area_and_month: the end-of-period outstanding balance for each area.
  - tmp_total_dist_debt_staff_monthly: the average end-of-period outstanding balance for each area.
  - tmp_ratio_each_area_to_all_area: the allocation ratio of funds to each area at the end of the period.
  - fact_summary_report_monthly: the final amount of funds allocated to each area at the end of the.
- From the fact_summary_report_monthly table, the summary report can be generated simply by using SQL queries."

<h3> Step 3: Build a monthly business performance ranking report.</h3>

- For this report, I created the asm_rank_report table to store the information.
- First, I applied business logic to calculate the contribution values of each employee to the company.
- Each employee's rank is determined by a total score, which is the sum of two main components: the scale score and the financial score. These two main scores are further broken down into several sub-scores. Therefore, I calculated these sub-scores by ranking the indicators computed in step 1.
- Finally, similar to the previous report, the desired ranking report can be retrieved simply using SQL queries."

<h3> Step 4: Ensure that the procedure continues to run even if an error occurs within a block.</h3>

- I also created a procedure_log table to record each time the procedure is executed. It helps with error handling by logging error details without stopping the procedure from running.

<h2> 📊 Visualization </h2>

To present the company's situation to the leadership team, manually using SQL for reporting is not practical, as it's difficult to provide a comprehensive overview. Therefore, I used Power BI to visualize the data.

<h3> Step 1: Prepare data </h3>

- First, I need to connect Power BI to my database to retrieve the required tables.
- Next, I need to verify the relationships between the tables to ensure that the star schema is correctly maintained, just as it is in the database.
- Additionally, to present the tables as intended, I also needed to adjust the source data to align with how Power BI operates.

<h3> Step 2: Define my goals </h3>

- Every business aims for sustainable growth, which is why I focused on four key objectives in each dashboard page: increasing profit, increasing revenue, reducing costs, and minimizing risks.
- I also needed to consider who would be reviewing my dashboards, so I designed them in a way that both business professionals and those without an economics background could easily understand the insights being conveyed.

<h3> Step 3: Define metrics and slicers </h3>

- The key metrics used are aligned with the objectives mentioned in step 2, such as revenue, profit, and non-performing loan ratio, all calculated using DAX.
- For slicers, there are two main ones: region and time, allowing viewers to filter the financial data by specific region and time period, or view it for all regions and all time periods.
- After identifying the metrics and slicers, I needed to select appropriate charts and colors to effectively represent those figures.

<h3> Step 4: Turn ideas into reality. </h3>

- First, I chose the Z-pattern as the main layout structure.
- Determine the placement of charts based on the chosen pattern, prioritizing general overviews first, followed by more detailed insights.
- Finally, I provided some insights and verified the accuracy of the data by cross-checking it directly with the database.
- Some pages from my dashboard:
![tong_quan_page.png](https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/tong_quan_page.png)
![xu_huong_page.png](https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/xu_huong_page.png)

<h2> 📋 Flowchart</h2>

![flowchart.drawio.png](https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/flowchart.drawio.png)

<h2> 🛠️ Installation</h2>
There are two ways to view this dashboard:

1. Download the file final project.pbix, install Power BI Desktop, and simply open the file to view the dashboard.
2. Check my powerbi link:

<h2> Contributing </h2>

Since this is my very first project, there are certainly unavoidable mistakes. If you have any feedback, I would sincerely appreciate it with all my gratitude.



### 🗄️ Databases
![PostgreSQL](https://img.shields.io/badge/POSTGRESQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### 🔧 Tools
![Power BI](https://img.shields.io/badge/POWER%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)




- **Context**: Receive request from the finance department to prepare 2 daily reports and finalize daily inventory numbers, write into an Excel file
- **Tech stack:** Power BI, PostgreSQL
- **How i do:** First, I process data using PostgreSQL, building dim and fact tables based on the star schema, and writing a procedure to continuously update data when new data is added. Next, I visualize the data using Power BI, presenting it with meaningful charts to explain the company's financial situation, thereby assisting the BOD in management and proposing development strategies for the company.
- **What i achieved**: Proficient in Power BI, skilled in DAX, capable of organizing and processing data using PostgreSQL to create continuously updated reports. 

