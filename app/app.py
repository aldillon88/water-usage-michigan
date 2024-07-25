import streamlit as st
import sys
import os
import pandas as pd

# Add the project root to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
	sys.path.append(project_root)

from backend import *


def main():

	st.set_page_config(layout="wide")
	data = load_data()
	melted = data.melt(id_vars=["year", "industry", "county"], value_vars=["megalitres_from_great_lakes", "megalitres_from_groundwater", "megalitres_from_inland_surface"], var_name="source")
	industry_list = data["industry"].unique()
	year_list = data["year"].unique()
	county_list = data["county"].unique()

	st.title('Water usage in the state of Michigan')

	with st.sidebar:
		
		st.header("Project Introduction")
		st.write("This project aims to provide insight into water usage in the state of Michigan from 2013 to 2022. Some questions to answer include: Where is the water coming from? Where is it going? How is water usage trending over time?")
		
		st.header("Dashboard Mode")
		mode = st.radio("Choose your view:", options=["Snapshot", "Over Time"], index=0)

		st.header("Filters")
		industry = st.multiselect("Industry", industry_list)
		county = st.multiselect("County", county_list)
		if mode == "Snapshot":
			year = st.multiselect("Year", year_list)

	if mode == "Snapshot":
		
		st.subheader("Proportion of water by source", divider=True)
		left, right = st.columns([0.3, 0.7], gap="large", vertical_alignment="center")
		left.write("This pie chart shows the contribution of each of the recorded water sources for the given filters on the left.")
		left.write("In most cases, the majority of the water used in the state of Michigan was sourced from the Great Lakes. This is not a surprise given how much of the state sits on the shores of the Great Lakes.")
		left.write("Some exceptions are present, such as water used in the Irrigation and Livestock industries, for which Groundwater and Surface Water are the main contributers. This is possibly due to geographical limitations, such as proximity to the Great Lakes, making transportation of water less feasible. More domain knowledge would help here.")
		right.write(plot_pie_chart(melted, values='value', names='source', industry=industry, county=county, year=year))

		st.subheader("Water usage by county", divider=True)
		left, right = st.columns([0.3, 0.7], gap="large", vertical_alignment="center")
		left.write("This choropleth plot shows the water usage by county based on the filters on the left.")
		left.write("Water usage for Irrigation and Livestock appears to be higher in the southwest of the state, which goes against the assumption made above.")
		left.write("Water usage for Electric Power Generation, the main consumer of water in Michigan, is also highest in the south of the state, mainly in the southwest and southeast, particularly around the populus Detroit area.")
		left.write("While comparatively low vs. other industries, water usage in the Commercial-Institutional industry is also at its highest in the south of the state, wit a couple of significant outliers in the north, in the counties of Iron and Charlevoix.")
		right.write(plot_choropleth_chart(data, industry=industry, year=year))


	if mode == "Over Time":
		st.subheader("Water usage by source over time", divider=True)
		left, right = st.columns([0.3, 0.7], gap="large", vertical_alignment="center")
		left.write("In this chart we can see the water usage over time across all three recorded water sources - The Great Lakes, Groundwater and Inland Surface Water. Using the filter on left left, we can drill down by industry and country to get a better understanding of their respective trends from 2013 to 2022.")
		left.write("Electric Power Generation, the biggest water consumer, appears to be trending slightly downwards during this period of time. This is likely due to a shift to renewable energy and less water intensive energy sources, such as natural gas.")
		right.write(plot_line_chart(melted, industry=industry, county=county))
		



if __name__ == '__main__':
	main()



