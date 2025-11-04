# PUBLIC-TRANSPORTION-PRO
helping greeley out with public transporttion
Dashboard
Interactive data visualization platform analyzing 11+ years of Greeley, Colorado public transit data (2014-2025).
COOLER BLAST Initiative - University of Northern Colorado
Show Image
Show Image

Project Overview
This dashboard analyzes Greeley Transit's ridership data to inform Bus Rapid Transit (BRT) planning and mobility development decisions. Built as part of the COOLER BLAST Initiative at UNC.
Key Findings

31% ridership decline in 2025 YTD compared to 2024 (requires investigation)
86% COVID recovery achieved by 2024 (relative to 2019 baseline)
Strong seasonal patterns: 70% swing between peak (October) and trough (June/July)
UNC student impact: 8-10% of total ridership during academic year


Quick Start
Prerequisites

Python 3.8 or higher
pip (Python package manager)

Installation
bash# Clone the repository
git clone https://github.com/YOUR-USERNAME/greeley-transit-dashboard.git
cd greeley-transit-dashboard

# Install required packages
pip install -r requirements.txt

# Ensure data file is present
# Place "New KPI Tracker.xlsx" in the project folder

# Run the dashboard
python greeley_dashboard_simple.py
Access Dashboard
Open your browser and navigate to: http://localhost:8050

Screenshots
Dashboard Overview
[Add screenshot of overview tab here]
Ridership Timeline
[Add screenshot of timeline tab here]
Seasonal Analysis
[Add screenshot of heatmap here]

Features

Interactive Timeline: Visualize 11+ years of ridership data with COVID period annotation
KPI Cards: Real-time metrics showing latest ridership, YoY change, and recovery percentage
Seasonal Heatmap: Identify monthly patterns and trends across years
Service Comparison: Compare Fixed Route, Paratransit, UNC, and Poudre Express services
Responsive Design: Works on desktop, tablet, and mobile devices
Export Capabilities: Download charts and data for presentations


Tech Stack

Python 3.8+ - Core programming language
Plotly - Interactive visualization library
Dash - Web application framework
Pandas - Data manipulation and analysis
Bootstrap - Responsive UI components
NumPy - Numerical computing


Project Structure
greeley-transit-dashboard/
├── greeley_dashboard_simple.py    # Main dashboard application
├── New KPI Tracker.xlsx            # Transit data (not in repo - add locally)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── screenshots/                    # Dashboard screenshots (optional)

Data Overview
Source: City of Greeley Transit Department
Time Period: January 2014 - September 2025 (141 months)
Update Frequency: Monthly
Metrics Analyzed

Monthly ridership by service type
Year-over-year growth rates
Seasonal patterns and trends
COVID-19 impact and recovery
Service efficiency metrics


Methodology
Data Processing

Load Excel data from KPI Tracker
Clean and validate ridership records
Calculate derived metrics (moving averages, YoY changes)
Handle missing values and outliers

Analysis Techniques

Time series decomposition
Seasonal pattern identification
Year-over-year comparison
Moving average trend analysis
Service type segmentation


Key Insights
The 2025 Decline Mystery
The dashboard reveals a concerning 31% YTD decline in 2025 versus 2024, contradicting the steady recovery trend since COVID. This requires immediate investigation into potential causes:

Service modifications
Route changes
External factors (construction, competition)
Data quality issues

Seasonal Patterns

Peak Season: September-October (start of UNC academic year)
Trough Season: June-July (summer break)
Variation: 70% swing between peak and trough months
Driver: Strong correlation with UNC academic calendar

COVID Recovery

Pre-COVID Peak: 820,000 annual riders (2018)
COVID Low: 354,000 riders (2020) - 56% decline
2024 Recovery: 702,000 riders - 86% of pre-pandemic levels
Projection: Full recovery estimated by 2026-2027


Team

[Your Name] - Lead Developer & Data Scientist
[Team Member 2] - Data Analyst
[Team Member 3] - Visualization Specialist
[Faculty Advisor] - Project Advisor

Faculty Advisor: [Advisor Name], University of Northern Colorado

Contributing
We welcome contributions! Areas for improvement:

Additional data sources integration
Machine learning forecasting models
GIS mapping capabilities
Mobile app development
Real-time data integration

See CONTRIBUTING.md for guidelines.

License
This project is licensed under the MIT License - see the LICENSE file for details.
Educational project developed for the COOLER BLAST Initiative at the University of Northern Colorado.

Contact
Project Lead: [Your Name]
Email: [your.email@unco.edu]
Institution: University of Northern Colorado
Initiative: COOLER BLAST
City Contact: Greeley Transit Department
Email: [transit@greeley.gov]

Acknowledgments

City of Greeley Transit Department - For providing comprehensive data and partnership
COOLER BLAST Initiative - For project support and funding
Felsburg Holt & Ullevig - For mobility development planning documents
University of Northern Colorado - For academic support and resources


Additional Resources

Greeley Mobility Development Plan
National Transit Database
APTA Transit Resources
Colorado Transit Data


Future Enhancements
Planned features:

 Real-time bus tracking integration
 Interactive GIS mapping
 Machine learning ridership forecasting
 Mobile application
 API for third-party developers
 Automated report generation
 Multi-city comparison dashboard


Impact
This dashboard directly informs:

$10-50M+ BRT investment decisions on Routes 1 & 5
9 mobility hub site selection and design
Service optimization recommendations
Equity analysis for transit access
Grant applications for federal funding


Star this repository if you find it useful!
Share: LinkedIn | Twitter | Email

Last Updated: November 2025
Version: 1.0.0
Status: Active Development
