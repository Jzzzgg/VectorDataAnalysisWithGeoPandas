import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from pathlib import Path

current_dir = Path(__file__)
data_dir = current_dir.parent.parent.parent.joinpath('data')
# Set high resolution for better quality plots
plt.rcParams['figure.dpi'] = 150


def read_file(file_name:str) -> gpd.GeoDataFrame:
    # read shape file 
    gdf = gpd.read_file(file_name)
    return gdf


def geometry_update(gdf:gpd.GeoDataFrame) -> None:
    gdf['area'] = gdf.area
    gdf['area_km2'] = gdf['area'] / 1000000
    gdf['boundary'] = gdf.boundary
    gdf['boundary_length'] = gdf['boundary'].length
    gdf['centroid'] = gdf.centroid
    gdf['centroid_x'] = gdf['centroid'].x
    gdf['centroid_y'] = gdf['centroid'].y


def main():
    # Reading Municipalities in philadelphia
    # Provide shp and shx file
    file_path = data_dir.joinpath('VectorDataAnalysisWithGeoPandas').joinpath('PaMunicipalities2024_03.shp')
    gdf = read_file(file_path)

    # Feature Engineering
    geometry_update(gdf)

    # Setting and Transforming CRS
    # Based on the coordinate magnitudes, we assume the CRS is Web Mercator (EPSG:3857)
    gdf.crs = 'EPSG:3857'
    # Verify the CRS has been set
    print("Original CRS:", gdf.crs)

    # Now that the CRS is set, we can transform it to EPSG:26910
    gdf_26910 = gdf.to_crs(epsg=26910)

    centroid_point = gdf_26910.loc[2]['centroid']
    gdf_26910['diff'] = gdf_26910['centroid'].distance(centroid_point)

    

    # Interactive visualization (folium map object 'm' would need to be saved to HTML for standalone viewing)
    # import folium # You'd need to install folium if not already present
    m = gdf.explore(
        column='area_km2',
        cmap='YlOrRd',
        tooltip='MUNICIPAL1',
        popup=True,
        legend=True,
        style_kwds={
            'color': 'black',
            'weight': 2
        }
    )
    m.save('interactive_map.html') # Save the interactive map to an HTML file


if __name__ == "__main__":
    main()