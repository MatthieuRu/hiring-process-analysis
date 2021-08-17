# I- Introduction of Hiring

The typical recruiting pipeline looks something like this:
1. Recruiter Phone Screen (optional)
2. Phone Screen #1
3. Phone Screen #2
4. Onsite 
5. Offer
6. Offer Accept


Because of interview performance and other factors, the shape of this pipeline looks like a funnel 


The Onsite round contains 4 interview questions: 
- Onsite Coding Question #1
- Onsite Coding Question #2
* 2 Onsite Value Fit Question *(the A/B/C/D prefix are used to denote different Value Fit Questions asked by different interviewers)*



Note that some interviews have multiple engineers conducting them, so you might see 2 “Phone Screen #1”s for the same candidate. 

The aim is to answer to the question:

**how we can improve university recruiting for future seasons?**


1. KPI Creation - How should we evaluate whether this University Recruiting season went well?  
2. Advice A - What can we do to improve University Recruiting in the future? 
3. Advice B - What can we do to improve our interviewing process? 


##### The client of this analysis is the **Head of Engineering** to help them understand how well the university recruiting season has been going, and what we can do better for future seasons. 

### What's the data

1. interviews: a table that contains interview feedback for many intern and new grad candidates
2. tags: : a table that contains candidates and tags for where the candidate was sourced 
3. offers: a table that contains candidates who received offers
4. offer_accepts: a table that contains candidates that accepted their offers

## II- Results


### Before to start

- ```git clone git@github.com:MatthieuRu/hiring-process-analysis.git``` *Git clone the project from Github.*
- ```./start.sh``` *Launch the docker images including the postgre server*
- ```conda env create``` *Create the conda environment based on the environment.yml.*
- ```conda activate hiring-process``` *Activate the conda environment.*
- ```python app.py``` *Run the app on your local machine*


### 1. Create the database & Run the app

A Postgre database is runing on a docker container and a app Hiring Process Insights has been created.


```python
from src.hiring_process_analysis.db_manager.server import Server
# Connection to the server
server = Server(
    ip='0.0.0.0',
    user='application',
    passwd='secretpassword',
    database='application'
) 
```


```python
# Create the schema
server._create_schema('src/hiring_process_analysis/db_manager/hiring_process.sql')
```


```python
# Delete the schema (if needed)
server._delete_schema()
```


```python
from src.hiring_process_analysis.db_manager.migration import Migration
import pandas as pd

## Load the different files and send them to the databases
migration = Migration(
    interview=pd.read_csv('./assets/interviews.csv'),
    candidate_tags=pd.read_csv('./assets/candidate_tags.csv'),
    offer_accepts=pd.read_csv('./assets/offer_accepts.csv'),
    offers=pd.read_csv('./assets/offers.csv'),

)

migration.send_to_databases(server=server)
```

### 2 - Get the differents KPI tables from the database

All the SQL query has been added to a function file. Each function is a query returning a pandas dataframe.


```python
from src.hiring_process_analysis.db_manager.get_kpi import get_kpi_conversion_overall
from src.hiring_process_analysis.db_manager.get_kpi import get_kpi_conversion_details
from src.hiring_process_analysis.db_manager.get_kpi import get_kpi_offers
from src.hiring_process_analysis.db_manager.get_kpi import get_onsite_question_overview
from src.hiring_process_analysis.db_manager.get_kpi import get_tag_candidate_overview
from src.hiring_process_analysis.db_manager.get_kpi import get_inferviews_table

# Get from the server to a DataFrame
kpi_convertion_overall = get_kpi_conversion_overall(server)
kpi_conversion_details = get_kpi_conversion_details(server)
kpi_offers = get_kpi_offers(server)
onsite_question_overview = get_onsite_question_overview(server)
tag_candidate_overview = get_tag_candidate_overview(server)

```

### 3 - Get the differents Graph and Indicators from the KPI tables

A Class has been created containing all the graph and indicators needed for the analysis and the app.


```python
from src.hiring_process_analysis.app.vizualisation import Vizualisation

# Class with all information needed
vizualisation = Vizualisation(
        get_kpi_conversion_overall(server),
        get_kpi_conversion_details(server),
        get_kpi_offers(server),
        get_onsite_question_overview(server),
        get_tag_candidate_overview(server),
        get_inferviews_table(server)
)

# Example
vizualisation.kpi_conversion_overall_graph
```


<div>                            <div id="b96b1b91-08cb-4598-ae77-50fec3213fe9" class="plotly-graph-div" style="height:525px; width:100%;"></div>            <script type="text/javascript">                require(["plotly"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById("b96b1b91-08cb-4598-ae77-50fec3213fe9")) {                    Plotly.newPlot(                        "b96b1b91-08cb-4598-ae77-50fec3213fe9",                        [{"alignmentgroup":"True","hovertemplate":"=%{x}<br>Number of Candidates=%{y}<extra></extra>","legendgroup":"","marker":{"color":"#636efa","pattern":{"shape":""}},"name":"","offsetgroup":"","orientation":"v","showlegend":false,"textposition":"auto","type":"bar","x":["Total of Candidates","Accepted Offers"],"xaxis":"x","y":[239,8],"yaxis":"y"}],                        {"barmode":"relative","legend":{"tracegroupgap":0},"paper_bgcolor":"#F2F6FC","plot_bgcolor":"#F2F6FC","template":{"data":{"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"choropleth"}],"contour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"contour"}],"contourcarpet":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"contourcarpet"}],"heatmap":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmap"}],"heatmapgl":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmapgl"}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"histogram2d":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2d"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2dcontour"}],"mesh3d":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergeo"}],"scattergl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermapbox"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolar"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolargl"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]],"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]},"colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"geo":{"bgcolor":"white","lakecolor":"white","landcolor":"#E5ECF6","showlakes":true,"showland":true,"subunitcolor":"white"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"light"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"bgcolor":"#E5ECF6","radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"ternary":{"aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"bgcolor":"#E5ECF6","caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"title":{"x":0.05},"xaxis":{"automargin":true,"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","zerolinewidth":2},"yaxis":{"automargin":true,"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","zerolinewidth":2}}},"title":{"text":"Overall Conversion"},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":""}},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"Number of Candidates"},"visible":false}},                        {"responsive": true}                    ).then(function(){

var gd = document.getElementById('b96b1b91-08cb-4598-ae77-50fec3213fe9');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })                };                });            </script>        </div>

