from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
from dash_extensions.javascript import assign
import numpy as np
import seaborn as sns
from mappings import *



def get_severity(death, heavy, light):
    if death:
        return 3
    if heavy:
        return 2
    if light:
        return 1
    return 0

# Preprocess the data into geobuf.
df = pd.read_csv("crashes2020_new.csv")
mapCZ = json.load(open("mapCR.json", "r", encoding="utf8"))

df['date'] = pd.to_datetime(df['date'])
df['road_type_leg'] = df['road_type'].map(road_type_dict)
df['severity'] = df.apply(lambda x: get_severity(x['deaths'], x['heavily_injured'], x['lightly_injured']), axis=1)
df['road_type'] = df['road_type'].apply(lambda x: x if x < 5 else 5)
# df[df['road_type'] > 5]['road_type'] = 5

times = [date for date in df['date'].unique()]
times.sort()

label_months_abv = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# Geojson rendering logic, must be JavaScript as it is executed in clientside.
point_to_layer = assign("""function(feature, x_cory_cor, context){
    const {min, max, circleOptions, colorProp} = context.props.hideout;
    //console.log('feature', feature);
    let colors = ["brown", "blue", "green", "yellow", "orange", "red"];
    circleOptions.fillColor = colors[feature.properties['road_type']];  // set color based on color prop.
    return L.circleMarker(x_cory_cor, circleOptions);  // sender a simple circle marker.
}""")

cluster_to_layer = assign("""function(feature, x_cory_cor, index, context){
    const {min, max, circleOptions, colorProp, count, colors} = context.props.hideout;

    const leaves = index.getLeaves(feature.properties.cluster_id, feature.properties.point_count);
    //let colors = ["brown", "blue", "green", "yellow", "orange", "red"];
    let valueSum = new Array(count).fill(0)
    //let valueSum = [0,0,0,0,0,0];
    for (let i = 0; i < leaves.length; ++i) {
        valueSum[leaves[i].properties[colorProp]] += 1
    }

    for (let i = 0; i < valueSum.length; ++i){
        valueSum[i] /= leaves.length;
        valueSum[i] *= 100;
    }

    let cumSum = 0
    let gradient = 'background: conic-gradient(';
    //console.log('val ', valueSum);
    for (let i = 0; i < valueSum.length; ++i){
        if (valueSum[i] != 0){
            if (cumSum == 0){
                if (valueSum[i] == 100){
                    gradient += 'red 0.01%, ' + colors[i] + ' 0.01%';
                    break;
                }
                cumSum += valueSum[i];
                gradient += colors[i] + ' ' + cumSum.toString() + '%, ';
                continue;
            }
            gradient += colors[i] + ' ' + cumSum.toString() + '% ';
            
            if (100 - (cumSum  + valueSum[i]) < 0.000001){
                break;
            }
            cumSum += valueSum[i];
            gradient += cumSum.toString() + '%, '; 
        }
    }


    //console.log('grad: ', gradient);


    //const valueMean = valueSum / leaves.length;
    // Render a circle with the number of leaves written in the center.

    //console.log(leaves.length, valueSum);
    //console.log(feature);
    //console.log(index);
    //console.log(leaves);

    const icon = L.divIcon.scatter({
        html: '<div style="margin: 0; border-radius: 50%; padding-top: 6px; height: 34px; width: 40px; ' + gradient + ')"><div style="margin: 0; height: 28px; width: 28px; background-color:white; border-radius: 50%; margin-left: auto; margin-right: auto;"><span>' + feature.properties.point_count_abbreviated +'</span></div></div>',
        className: "marker-cluster",
        iconSize: L.point(40, 40),
    });
    return L.marker(x_cory_cor, {icon : icon});
}""")



# Create the app.
df_columns = pd.DataFrame({"cols": ['crash_type', 'substance', 'weather', 'road_type',]})

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Car crashes in Czech republic from 2020", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(id='map', style={'display':'block'}),
        html.Div(id='cluster-map', style={'margin': '20px'}),
        dcc.Slider(
            0,
            11,
            step=1,
            id='filter-date--slider',
            value=0,
            marks={i: {'label': label_months_abv[i], 'style': {'fontSize': '16px'}} for i in range(12)}, #'style':{'transform':'rotate(-90deg)', 'margin-left':'-20px', 'margin-top': '10px', 'font-size': '12px', 'font-weight': 'bold'}
        ),
    ], id='map-div', style={'width': '50%', 'display': 'inline-block'}),
    
    
    html.Div([
        html.Div([
            html.H3('Choose map representation:'),
            dcc.RadioItems(
                ['heatmap', 'clustered crashes'],
                'clustered crashes',
                id='map-type',
                inline=True,
            )
        ]),  
        html.Div([
            html.H3('Choose one of crash features:'),
            dcc.Dropdown(
                df_columns['cols'].unique(),
                'road_type',
                id='xaxis-column',
            ),
        ]),
        dcc.Graph(id='stat'),
    ], id='stat-div', style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
])


@app.callback(
    Output('map', 'figure'),
    Output('map', component_property='style'),
    Output('stat', 'figure'),
    Output('cluster-map', 'children'),
    
    Input('map-type', 'value'),
    Input('filter-date--slider', 'value'),
    Input('xaxis-column', 'value'))
def update_graph(map_type, chosen_date, stat_type):
    global colorbar
    current_df = df[df['date'] == times[chosen_date]]
    info = ['x_cor', 'y_cor', 'road_type', 'deaths', 'substance', 'weather', 'crash_type']
    info_heatmap = ['x_cor', 'y_cor', 'road_type_leg', 'deaths', 'substance_leg', 'weather_leg', 'crash_type_leg']
    current_df['road_type_leg'] = current_df['road_type'].map(road_type_dict)
    current_df['substance_leg'] = current_df['substance'].map(substance_dict)
    current_df['weather_leg'] = current_df['weather'].map(weather_dict)
    current_df['crash_type_leg'] = current_df['crash_type'].map(crash_type_dict)
    
    ## CREATE STAT GRAPH
    distinct_count = len(current_df[stat_type].unique())
    stat_df = current_df.groupby([stat_type, 'severity']).agg(count=('time', 'count')).reset_index()
    stat_df['severity'] = stat_df['severity'].map(severity_dict)
    fig2 = px.bar(stat_df, x=stat_type, y='count', color='severity', barmode='group', log_y=True)
    fig2.update_xaxes(tickmode='array', tickvals=[i for i in range(len(x_labels[stat_type]))], ticktext=x_labels[stat_type])

    
    ## CREATE HEAT MAP
    fig = px.density_mapbox(current_df, lat='y_cor', lon='x_cor', radius=5, custom_data=current_df[info_heatmap])

    fig.update_layout(height=530,
                      mapbox_style="open-street-map",
                      mapbox_zoom=5.9, 
                      mapbox_center = {"lat": 49.8175, "lon": 15.4730},
                      margin=dict(b=0, t=20, l=20, r=20),
                      coloraxis_showscale=False,
                      hoverlabel={'bgcolor': 'white','font': {'color': 'black'}}
                      )
    fig.update_traces(hovertemplate='coordinates: (%{customdata[0]}, %{customdata[1]}) <br>Road type: %{customdata[2]} <br>Deaths: %{customdata[3]} <br>Substance: %{customdata[4]} <br>Weather: %{customdata[5]}<br>Crash type: %{customdata[6]}<extra></extra>')

    # CREATE COLORBAR
    x = np.linspace(0, 1, distinct_count)
    classes = [legend_dictionaries[stat_type][i] for i in range(distinct_count)]
    if stat_type == "substance":
        c = px.colors.sample_colorscale('YlOrRd', list(x))
    elif stat_type == "crash_type" or stat_type == "weather":
        c = sns.color_palette("Set3").as_hex()[:distinct_count]
    else:
        x = np.linspace(0, 1, distinct_count-2)
        c = px.colors.sample_colorscale('YlOrRd', list(x)) + px.colors.sample_colorscale('Plotly3', [0, 1])

    print(c)
    colorscale = ["brown", "blue", "green", "yellow", "orange", "red",]
    # Create colorbar.
    ctg = ["{}".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}".format(classes[-1])]
    colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=c, width=20, height=150, style={'background-color':'rgba(255,255,255,0.9)'})

    ## CREATE CLUSTER MAP
    map_df = current_df[info]  # drop irrelevant columns
    dicts = map_df.to_dict('rows')
    for item in dicts:
        item["tooltip"] = f'coordinates: ({item["x_cor"]}, {item["y_cor"]})<br>Road type: {road_type_dict[item["road_type"]]}<br>Deaths: {item["deaths"]}<br>Substance: {substance_dict[item["substance"]]} <br>Weather: {weather_dict[item["weather"]]}<br>Crash type: {crash_type_dict[item["crash_type"]]}'
    geojson = dlx.dicts_to_geojson(dicts, lon="x_cor", lat="y_cor")  # convert to geojson
    geobuf = dlx.geojson_to_geobuf(geojson)  # convert to geobuf
    
    # Create geojson.
    geojson = dl.GeoJSON(data=geobuf, id="geojson", format="geobuf",
                        zoomToBounds=True,  # when true, zooms to bounds when data changes
                        cluster=True,  # when true, data are clustered
                        clusterToLayer=cluster_to_layer,  # how to draw clusters
                        zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. cluster) on click
                        options=dict(pointToLayer=point_to_layer),  # how to draw points
                        superClusterOptions=dict(radius=150),   # adjust cluster size
                        hideout=dict(colorProp=stat_type, count=distinct_count, colors=c, circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
                                    min=0, max=10))
    heatmap = {'display':'block'}
    clustermap = {'display':'none'}
    if map_type != 'heatmap':
        heatmap = {'display':'none'}
        clustermap = {'width': '100%', 'height': '520px', 'margin': "auto", "display": "block",}
    return fig, heatmap, fig2, dl.Map([dl.TileLayer(), geojson, colorbar], viewport={'center':[49.8175, 15.4730], 'zoom': 6.5}, style=clustermap)



if __name__ == '__main__':
    app.run_server(debug=True)
