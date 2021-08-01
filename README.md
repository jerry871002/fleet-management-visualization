# Fleet Management Visualization

Visualizing fleet data using Plotly

## Usage
1. Run `python index.py` to start the app
2. Enter figure name (`/graphs/<figure_name>`) in the URL to see the graph, e.g. `http://127.0.0.1:8050/graphs/F01-1`
3. Use parameters to see different results, try `http://127.0.0.1:8050/graphs/F01-1?new_v_datetime=2019-8-4&voyage_route=2`!

## Graphs

### F01-1: Voyage Real-Time Monitoring

> Parameters:
> - `new_v_datetime`
> - `voyage_route`

![F01-1](https://i.imgur.com/FWFVhU9.png)


### F02-1: Voyage Review

> Parameters:
> - `new_v_datetime`
> - `voyage_route`

![F02-1](https://i.imgur.com/Sl6Ksqe.png)

### F03-1: Hull Perfermance

> Parameters:
> - `oldstartdatetime`

![F03-1](https://i.imgur.com/N0Wwicc.png)

### F03-1-2: Hull Perfermance Combined

> Parameters:
> - `oldstartdatetime`

![F03-1-2](https://i.imgur.com/Pv75DSF.png)

### F03-3: Wind Speed and Direction Diagram

![F03-3](https://i.imgur.com/MokIDXw.png)

### F04-1: Propeller Performance

> Parameters:
> - `oldstartdatetime`

![F04-1](https://i.imgur.com/h80aj8K.png)

### F04-1-2: Propeller Performance Combined

> Parameters:
> - `oldstartdatetime`

![F04-1-2](https://i.imgur.com/toErSls.png)

### F04-2: SOG Power BF Head

![F04-2](https://i.imgur.com/LiPDhV3.png)

### F04-3: Ship Speed Impact Factor

> Parameters:
> - `voyage_route`
    
![F04-3](https://i.imgur.com/BGd5ktn.png)

### F04-4: Current Direction & Speed

![F04-4](https://i.imgur.com/8Gu8R1b.png)

### F05-1-all: SOG/Current Speed/BF/RPM% Combined

> Parameters:
> - `new_v_datetime`
> - `voyage_route`

![F05-1-all](https://i.imgur.com/k9DgsBO.png)


### F05-2-all: RPM/SLIP/ME LOAD% Combined

> Parameters:
> - `new_v_datetime`
> - `voyage_route`

![F05-2-all](https://i.imgur.com/ypEwTFN.png)

### F05-3-all: Fuel Consumption Combined

![F05-3-all](https://i.imgur.com/sBnaYSY.png)


