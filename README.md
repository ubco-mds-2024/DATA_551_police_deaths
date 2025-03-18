# DATA_551_police_deaths  
**Live Dashboard:** [https://police-death-033ead8472ee.herokuapp.com/](https://police-death-033ead8472ee.herokuapp.com/)
## **Dashboard Overview & Instructions**  

### **How to Run the Dashboard**  
To initiate the dashboard, simply run the following command in your terminal:  

```bash
python demo.py
```
Once executed, the dashboard will automatically launch in your **web browser**, providing an interactive interface for exploring the dataset.

---

## **Dashboard Preview**  
![dashboard](https://github.com/user-attachments/assets/5cbb71b1-d09f-46fd-a5f2-82e330509441)

---
## **Dashboard Features & Visualizations**

### **1. Geographic Analysis: U.S. Map**
- **Color-coded choropleth map** displaying the distribution of fallen officers by state.
- **Hover tooltips** provide state-specific fatality counts.
- **Filters allow refinement** of data based on time range, cause, and officer type.

### **2. Top Causes of Death: Bar Chart**
- **Highlights the top 10 causes of death** among fallen officers.
- **Dynamic updates** based on selected filters.
- **Tooltips display exact values** when hovering over bars.

### **3. Temporal Trends: Time-Series Chart**
- **Displays fluctuations in police fatalities over time**.
- **Interactive x-axis allows zooming and panning**.
- Identifies **spikes and declines in incidents**.

### **4. Department-Level Insights: Bar Chart**
- **Lists the top 10 law enforcement departments** with the highest number of fallen officers.
- **Sortable by count** for deeper department-specific analysis.

### **5. Summary Statistics**
Provides **key numerical insights** into fallen officers, dynamically updating based on the user-selected time range:
- **Total Deaths**: Number of fallen officers in the selected period.
- **Average Deaths Per Year**: Computed based on the user-defined time range.
- **Deaths in Last 10 Years of Selection**: Total deaths recorded in the most recent 10 years within the selected period.
- **Deaths in Last 5 Years of Selection**: Total deaths recorded in the most recent 5 years within the selected period.
- **Deaths in Last Year of Selection**: Total deaths recorded in the most recent year within the selected period.

### **6. Interactive Filtering Options**
Users can **refine the dataset** using multiple filtering tools:
- **Time Range Selector**: Adjustable slider to filter data by year.
- **Cause of Death Multi-Select**: Allows filtering by specific fatality causes.
- **State Selector**: Enables focus on individual or multiple U.S. states.
- **Officer Type Toggle**: Users can view **all officers, human officers only, or K9s only**.

### **7. Recently Fallen Officers**
- A **table displaying recent fallen officers** based on applied filters.
- Displays **names, departments, and End of Watch (EOW) dates**.

### **8. Informational Sections**
- **About Fallen Officers**: Educational section explaining **why** this data matters and **trends in police fatalities**.
- **About the Data**: Provides dataset details, source information (ODMP, FiveThirtyEight), and key variables.

---

## **Motivation and Purpose**  

### **Our Role**  
Student research group focused on historical trends in public service safety.  

### **Target Audience**  
Researchers, policymakers, and educators in public safety and law enforcement.  

Police deaths in the U.S. from **1791 to 2016** reflect historical challenges in public safety and law enforcement. Understanding trends in causes of deaths, geographic distribution, and agency-level patterns can inform policies to improve officer safety.  

To address this need, we developed a **data visualization dashboard**. Our goal is to empower researchers, policymakers, and educators to explore the dataset interactively. Users can **identify trends, evaluate the impact of causes of death over time, and understand incident distribution** across the U.S. This dashboard serves as a resource for **decision-making, public education, and improving workplace safety in law enforcement**.  

---

## **Description of the Data**  

Our dataset consists of **approximately 22,800 records** documenting **police deaths in the U.S. from 1791 to 2016**, sourced from the **Officer Down Memorial Page (ODMP)**. This dataset, publicly available on the **FiveThirtyEight GitHub repository**, was used in their analysis, *"The Dallas Shooting Was Among The Deadliest For Police In U.S. History."*  

### **Dataset Contents:**  
- **Officer Details:** Names, departments, ranks, and "End of Watch" (EOW) dates.  
- **Incident Information:** Causes of death (categorized and detailed).  
- **Geographic Data:** U.S. state, year, and department where incidents occurred.  
- **Canine Units:** Dataset includes deaths of **both human officers and police K9s**.  

This dataset allows for in-depth analysis of **historical trends in law enforcement fatalities** across different time periods, locations, and causes.  

---

## **Research Questions and Usage Scenarios**  

### **Proposed Research Questions**  
The dashboard is designed to answer key research questions that **uncover patterns, trends, and insights** related to police fatalities across the U.S.:  

1. **What are the primary causes of police fatalities, and how have they evolved over time?**  
2. **How do police fatality trends vary across different states, regions, and departments?**  
3. **How have annual police fatality rates fluctuated over the years, and what factors contribute to these changes?**  
4. **Are there discernible patterns in officer fatalities based on incident type (e.g., automobile accidents, gunfire) or temporal factors (e.g., seasonality, time of day)?**  
5. **What demographic trends exist among fallen officers, such as variations in age, rank, and years of service?**  

These questions provide both **exploratory insights and practical applications**. For instance:  
- **Understanding shifts in fatality causes** informs **modern safety protocols**.  
- **Geographic trends highlight regional disparities**, guiding resource allocation.  
- **Temporal patterns help optimize operational planning**, such as training or risk mitigation strategies.  

### **Usage Scenario: How This Dashboard Can Be Used**  

#### **Example: Crime Analyst Lisa's Workflow**  
Detective Lisa is a **crime analyst** working for a U.S. police department. Her team assesses **officer safety risks** and proposes **policy changes** to improve training and operational protocols.  

1. **Explores Geographic Trends**: Lisa starts with a **heatmap** showing police (including K9 officers) fatalities by state. She notices that certain regions have significantly higher fatality rates.  
2. **Identifies Leading Causes**: Using a **bar chart**, she examines the **top 10 causes of death**, filtering by **automobile-related and gunfire-related deaths**, the two leading causes.  
3. **Analyzes Temporal Patterns**: Lisa uses a **time-series graph** and discovers that **gunfire-related deaths have declined**, but **automobile-related fatalities have increased**.  
4. **Investigates Peak Years**: She applies a **yearly filter** and identifies **spikes in fatality rates** in certain years.  
5. **Forms Data-Driven Recommendations**: With these insights, Lisa compiles a report recommending:  
   - Enhanced **defensive driving training** for new officers.  
   - Improved **K9 transport safety measures**.  
   - Additional protocols for **high-risk assignments**.  

The dashboard’s **interactive design and dynamic filters** enable her to **efficiently uncover patterns** and support **data-driven decisions** for **improving officer safety**.  

---


## **User Experience & Design**  

- **Dynamic Panels**: Visualizations update **in real-time** based on filters.  
- **Interactive Elements**: Users can **hover, click, and explore data dynamically**.  
- **Multi-Visualization Integration**: Maps, bar charts, and time-series graphs provide a **holistic dataset analysis**.  

---
## Scratch
![PNG image-5765E9E27C24-1](https://github.com/user-attachments/assets/0d39dea6-3f95-4fa7-bed7-d1e6b1fd100c)
