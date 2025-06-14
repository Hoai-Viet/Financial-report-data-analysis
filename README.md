<h1 align="center">Financial monthly report data analysis</h1>

<h2>Description</h2>
Develop a consolidated report to track revenue, profit, employee performance monthky, thereby painting a financial picture and proposing development strategies for the company. 

## Table of Contents

- [1. Overview](#-overview)
- [2. Tech stack](#-tech-stack)
- [3. Flowchart](#-report-types)
- [4. Data collection](#-data-collection)
- [5. How I did this project ?](#-project-method)
- [6. Visualization](#-visualization)
- [7. How to view this dashboard](#️-installation)
- [8. Conclusion](#-conclusion)

<h2> 1. Overview </h2>

I was assigned by upper management to create reports for monitoring and managing the company's financial situation. To effectively manage the overall company performance, I focused on analyzing the performance of each region and the Area Sales Managers (ASMs) responsible for them. After identifying the target subjects for analysis, the next step is data collection, which will be explained in more detail in the following sections.

The two preliminary reports that I have outlined:

<div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/mockup_os_report.png" alt="Mô tả">
  <p><em>Figure1. mock up summary report</em></p>
</div>


<div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/mockup_os_asm_rank.png" alt="Mô tả">
  <p><em>Figure 2. mock up asm rank report</em></p>
</div>


<h2> 2. Tech stack </h2>

![PostgreSQL](https://img.shields.io/badge/POSTGRESQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/POWER%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Dbeaver](https://img.shields.io/badge/dbeaver-382923?style=for-the-badge&logo=dbeaver&logoColor=white)

<h2> 3. Flowchart</h2>

<div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/flowchart.drawio.png" alt="Mô tả">
  <p><em>Figure 3. Flowchart</em></p>
</div>

<h2> 4. Data collection </h2> 

- Step 1: After identifying the key indicators, I needed to determine the components of the funding sources by contacting the Accounting – Finance department, IT department, Human resource department to obtain the necessary data.
- Step 2: Next, I imported the data into PostgreSQL using DBeaver and performed several verification steps to ensure the data was imported accurately and completely
- Step 3: At this stage, the data consisted of isolated transactions. I had to apply business knowledge along with basic SQL commands to transform them into fact tables. Although these tables were processed, they were still raw and not yet ready for direct use.
- The result of step 3:

<div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/fact_raw_tables.png" alt="Mô tả">
  <p><em>Figure 4. fact raw tables </em></p>
</div>
  
<h2> 5. How i did this project ? </h2>

<h3> 5.1. Preprocessing data </h3>

- Step 1:  With the three raw fact files just created, I began transforming them into fact tables containing only the necessary data, along with their corresponding dimension tables. I continued working with PostgreSQL via DBeaver and performed import validation steps to ensure the data was displayed accurately and completely.
- Step 2: Next, I created dimension tables based on the star schema to enable more efficient data storage as the dataset grows, include:
  - dim_funding_structure: Stores information about a fund, including id, parent_id, and other relevant details.
  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/dim_funding_structure.png" alt="Mô tả">
  <p><em>Figure 5. dim_funding_structure </em></p>
  </div>
  
  - dim_area: Stores information such as region name, region code, and so on.
  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/dim_area.png" alt="Mô tả">
  <p><em>Figure 6. dim_area </em></p>
  </div>
    
  - dim_date: Contains information about the reporting date.
  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/dim_date.png" alt="Mô tả">
  <p><em>Figure 7. dim_date </em></p>
  </div>

  - dim_staff: Stores information about ASMs.
  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/dim_staff.png" alt="Mô tả">
  <p><em>Figure 8. dim_staff </em></p>
  </div>

  - dim_city: Stores information about cities.
  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/dim_city.png" alt="Mô tả">
  <p><em>Figure 9. dim_city </em></p>
  </div>

- Step 3: At this stage, I will update the fact tables based on information from the dimension tables, such as changing the data type from varchar to int to improve data retrieval speed. Additionally, I will remove unnecessary columns to avoid clutter.

  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/fact_txn_before_and_after.png" alt="Mô tả" width=3000px>
  <p><em>Figure 10. fact_txn before and after modification </em></p>
  </div>

- Step 4: Finally, i created two tables: fact_summary_report and asm_rank_report. These are the final tables that store the processed data. Reports can be generated directly from these tables using SQL queries.
  
  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/fact_summary_report.png" alt="Mô tả">
  <p><em>Figure 11. fact_summary_report </em></p>
  </div>

  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/asm_rank_report.png" alt="Mô tả">
  <p><em>Figure 12. asm_rank_report </em></p>
  </div>

<h3> 5.2. Build summary monthly report </h3>

- Step 1: After understanding the business logic and the allocation method of each expense, I created temporary tables to store the information at each calculation step, the temporary tables include:. 
  - tmp_report_gl_by_area_monthly: the original funds allocated from the head office at the end of the period.
  - tmp_total_dbt_staff_each_area_and_month: the end-of-period outstanding balance for each area.
  - tmp_total_dist_debt_staff_monthly: the average end-of-period outstanding balance for each area.
  - tmp_ratio_each_area_to_all_area: the allocation ratio of funds to each area at the end of the period.
  - fact_summary_report_monthly: the final amount of funds allocated to each area at the end of the period.
    
- Step 2: After all the calculations are completed, the final data will be loaded into the fact_summary_report table, the summary report can be generated simply by using SQL queries."

<h3> 5.3. Build a monthly business performance ranking report </h3>

- Step 1: For this report, I created the asm_rank_report table to store the information.
- Step 2: I applied business logic to calculate the contribution values of each employee to the company.
- Step 3: Employee's rank is determined by a total score, which is the sum of two main components: the scale score and the financial score. These two main scores are further broken down into several sub-scores. Therefore, I calculated these sub-scores by ranking the indicators computed in step 1.
- Step 4: Similar to the previous report, the desired ranking report can be retrieved simply using SQL queries."

<h3> 5.3. Ensure that the procedure continues to run even if an error occurs within a block </h3>

I also created a procedure_log table to record each time the procedure is executed. It helps with error handling by logging error details without stopping the procedure from running.

  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/procedure_log.png" alt="Mô tả">
  <p><em>Figure 13. procedure_log </em></p>
  </div>

<h2> 6. Visualization </h2>

To present the company's situation to the leadership team, manually using SQL for reporting is not practical, as it's difficult to provide a comprehensive overview. Therefore, I used Power BI to visualize the data.

<h3> 6.1. Prepare data </h3>

- Step 1: Connecting Power BI to my database to retrieve the required tables.

  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/choosing_database.png" alt="Mô tả">
  <p><em>Figure 14. choosing database </em></p>
  </div>

  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/choosing_database.png" alt="Mô tả">
  <p><em>Figure 15. connecting database </em></p>
  </div>


- Step 2: I need to verify and modify the relationships between the tables to ensure that the star schema is correctly maintained, just as it is in the database.

  <div align="center">
  <img src="https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/choosing_database.png" alt="Mô tả">
  <p><em>Figure 16. model relationship </em></p>
  </div>
  
- Step 3: Present the tables as intended, I also needed to adjust the source data to align with how Power BI operates.

<h3> Step 2: Define my goals </h3>

- Every business aims for sustainable growth, which is why I focused on four key objectives in each dashboard page: increasing profit, increasing revenue, reducing costs, and minimizing risks.
- I also needed to consider who would be reviewing my dashboards, so I designed them in a way that both business professionals and those without an economics background could easily understand the insights being conveyed.

<h3> Step 3: Define metrics and slicers </h3>

- The key metrics used are aligned with the objectives mentioned in step 2, such as revenue, profit, and non-performing loan ratio, all calculated using DAX.
- For slicers, there are two main ones: region and time, allowing viewers to filter the financial data by specific region and time period, or view it for all regions and all time periods.
- After identifying the metrics and slicers, I needed to select appropriate charts and colors to effectively represent those figures.

<h3> Step 4: Turn ideas into reality </h3>

- First, I chose the Z-pattern as the main layout structure.
- Determine the placement of charts based on the chosen pattern, prioritizing general overviews first, followed by more detailed insights.
- Finally, I provided some insights and verified the accuracy of the data by cross-checking it directly with the database.
- Some pages from my dashboard:
![tong_quan_page.png](https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/tong_quan_page.png)
![xu_huong_page.png](https://github.com/Vietzzzz/Financial-report-data-analysis/blob/main/image/xu_huong_page.png)


<h2> 7. How to view this dashboard ?</h2>

Check my Power BI link:

<h2> 8. Conclusion </h2>

Through this personal project, I not only improved my SQL skills, but also learned how to organize data, store it efficiently, and retrieve it when needed. In addition, I gained experience in data visualization by connecting to a database and using DAX formulas. Most importantly, I developed a clearer understanding of how data analysis can benefit a business. This allowed me to present data in a way that delivers the most valuable insights to viewers, especially the management team.

Since this is my very first project, there are certainly unavoidable mistakes. If you have any feedback, I would sincerely appreciate it with all my gratitude.



