import streamlit as st
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json



def load_data():
	path = "data/clean/water_usage.csv"
	df = pd.read_csv(path, dtype={"fips": str, "year": str})
	return df


def plot_pie_chart(data, values, names, industry=None, county=None, year=None):

	if industry and county and year:
		data = data[data["industry"].isin(industry)]
		data = data[data["county"].isin(county)]
		data = data[data["year"].isin(year)]

	elif industry and not county and not year:
		data = data[data["industry"].isin(industry)]

	elif year and not industry and not county:
		data = data[data["year"].isin(year)]

	elif county and not industry and not year:
		data = data[data["county"].isin(county)]

	color_map = {
		"megalitres_from_great_lakes": "#83c9ff",
		"megalitres_from_inland_surface": "#2568c9",
		"megalitres_from_groundwater": "#f9abab"
	}

	category_order = ["megalitres_from_great_lakes", "megalitres_from_inland_surface", "megalitres_from_groundwater"]
	
	fig = px.pie(data, values=values, names=names, color=names, color_discrete_map=color_map, category_orders={names: category_order})

	fig.update_layout(height=500,
					  uniformtext_minsize=9,
					  uniformtext_mode='hide')

	return fig


def plot_choropleth_chart(data, industry=None, year=None):

	with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
		counties = json.load(response)

	if industry and year:
		data = data[data["industry"].isin(industry)]
		data = data[data["year"].isin(year)]

	elif industry and not year:
		data = data[data["industry"].isin(industry)]

	elif year and not industry:
		data = data[data["year"].isin(year)]

	data = data.pivot_table(
			index=["fips", "county"],
			values="total_megalitres_all_sources",
			aggfunc="sum").reset_index()

	fig = px.choropleth(data, geojson=counties, locations='fips', color='total_megalitres_all_sources',
							   color_continuous_scale="Viridis_r", hover_data=["county"],
							   labels={'total_megalitres_all_sources':'total megalitres'}
							  )
	fig.update_geos(fitbounds="locations", visible=False)
	fig.update_layout(
		autosize=False,
		height=500,
		margin={"r":0,"t":0,"l":0,"b":0},
		geo=dict(bgcolor= 'rgba(0,0,0,0)'),
		coloraxis_colorbar=dict(
			thicknessmode="pixels",
			thickness=15,
			lenmode="fraction",
			len=0.75,
			yanchor="middle",
			y=0.5))

	return fig


def plot_line_chart(data, industry=None, county=None):

	if industry and county:
		data = data[data["industry"].isin(industry)]
		data = data[data["county"].isin(county)]

	elif industry and not county:
		data = data[data["industry"].isin(industry)]

	elif county and not industry:
		data = data[data["county"].isin(county)]

	data = data.pivot_table(
		index=["year", "source"],
		values="value",
		aggfunc="sum").reset_index()

	fig = px.line(data, x="year", y="value", color="source")
	return fig

x = ["year", "industry", "source", "value"]
	