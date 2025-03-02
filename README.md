# DATA_551_police_deaths  

## **Dashboard Overview & Instructions**  

### **How to Run the Dashboard**  
To initiate the dashboard, simply run the following command in your terminal:  

```bash
python demo.py
```
Once executed, the dashboard will automatically launch in your **web browser**, providing an interactive interface for exploring the dataset.

# DATA_551_police_deaths  

## **Dashboard Preview**  
![image](https://github.com/user-attachments/assets/0df86edd-87fd-4f5e-8b3e-e5ce3225b6df)  

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

## **Dashboard Features & Visualizations**  

### **1. Geographic Analysis: U.S. Map**  
- **Color-coded map** displays the geographic distribution of deaths.  
- **Hover tooltips** show state-specific statistics.  
- **Clickable states** allow users to drill down into detailed regional data.  

### **2. Top Causes of Death: Bar Chart**  
- Highlights **top 10 causes of death** with clear labels.  
- Includes **interactive tooltips** for additional context.  

### **3. Temporal Trends: Time-Series Histogram**  
- Visualizes **fluctuations in police fatalities over time**.  
- Identifies **spikes and declines in incidents**.  

### **4. Department-Level Insights: Bar Chart**  
- Displays **top 10 departments with the highest number of deaths**.  

### **5. Filters and Summary Statistics**  
- **Side panel** allows users to filter by:  
  - **Cause of Death**  
  - **Time Range** (interactive slider & input box)  
  - **Geographic Region** (states or departments)  
- Displays **summary statistics**, including:  
  - **Total deaths, monthly/yearly averages, and year-over-year percentage changes**.  

---

## **User Experience & Design**  

- **Dynamic Panels**: Visualizations update **in real-time** based on filters.  
- **Interactive Elements**: Users can **hover, click, and explore data dynamically**.  
- **Multi-Visualization Integration**: Maps, bar charts, and time-series graphs provide a **holistic dataset analysis**.  

---
## Scratch
![PNG image-5765E9E27C24-1](https://github.com/user-attachments/assets/0d39dea6-3f95-4fa7-bed7-d1e6b1fd100c)
