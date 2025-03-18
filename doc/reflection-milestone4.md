# Reflection on Dashboard Development

## Implemented Features

Our dashboard has seen significant improvements, making it more intuitive and effective for analyzing police officer fatalities. We have enhanced interactivity, refined visualizations, and improved statistical summaries to provide a more informative user experience.

### Improved Summary Statistics

We have enhanced the statistical summary to dynamically reflect key metrics based on the user's selected time range. The statistics now dynamically adjust based on the user-selected time range, ensuring that insights are always relevant to the specified period without requiring additional manual calculations.

The summary includes:

- Total Deaths within the selected period.
- Average Deaths Per Year calculated based on the selected time range.
- Deaths in the Last 10 Years within the selected period (e.g., if the selected range is 2000–2015, this metric reflects deaths from 2006–2015).
- Deaths in the Last 5 Years within the selected period (e.g., for 2000–2015, this covers deaths from 2011–2015).

### Enhanced Filtering & Selection Logic

The dashboard’s filtering system has been optimized for better usability. The "Select All" feature for states and causes allows users to efficiently manage selections. Additionally, the improved selection logic for officer types ("All", "Human", and "Canine") provides clearer tracking of selected categories, enhancing the overall user experience.

### Visualization Refinements

- **U.S. Choropleth Map:** The map now ensures that unselected states remain visible in gray, improving clarity without losing context.
- **Refined Bar Charts:** Tooltips now display formatted numbers, and y-axis labels are clearer, making comparisons easier.
- **Time Series Chart:** The x-axis dynamically adjusts to different time spans, improving readability and trend analysis.
- **Dashboard Descriptions:** We have added clear explanations about the dashboard’s purpose and data sources, helping users interpret the information more effectively.

### Recent Officers Table

A new "Recent Officers" table dynamically displays the five most recently fallen officers. This section is automatically hidden when no relevant data is available, keeping the dashboard clean and informative.

### Layout & Styling Improvements

- **Responsive Card Layout:** The summary statistics section now adapts seamlessly to different screen sizes.
- **User-Friendly Design:** Improved button groups and interactive elements make the dashboard easier to navigate and interact with.

## Final Thoughts

Through iterative refinements, we have significantly improved our dashboard’s usability and clarity. Feedback has been instrumental in shaping these enhancements, leading to a more accessible and effective tool for analyzing police officer fatalities. While there are always opportunities for future improvements, we believe this version provides a well-structured and insightful user experience. We have addressed all the points raised in the feedback and successfully implemented all the originally planned features.

