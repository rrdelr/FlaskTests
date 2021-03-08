import plotly
import plotly.express as px
import numpy as np
import pandas as pd
import json

def custom_round(x, base):
    return int(base * round(float(x)/base))

def num2dir(d):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

def num2range(d,index=False):
    ranges = ['< 2.0', '2.0 - 4.0', '4.0 - 6.0', '6.0 - 8.0', '8.0 - 10.0', '10.0 - 12.0', '12.0 - 14.0', '14.0 - 16.0', '16.0 >']
    if d < 2:
        lx = 0
    elif d < 4:
        lx = 1
    elif d < 6:
        lx = 2
    elif d < 8:
        lx = 3
    elif d < 10:
        lx = 4
    elif d < 12:
        lx = 5
    elif d < 14:
        lx = 6
    elif d < 16:
        lx = 7
    else:
        lx = 8

    if index:
        return lx
    else:
        return ranges[lx]

def plotrose():
    df = pd.read_excel('temp_test.xlsx')

    # u = eastward
    # v = northward

    vmagn = (df['v'] ** 2 + df['u'] ** 2) ** 0.5

    angle = np.arctan2(df['u'] * -1, df['v'] * -1)
    angle = np.degrees(angle)

    dfnew = {'Direction': angle, 'Interval': vmagn}
    df = pd.DataFrame(data=dfnew)

    # df['angle'] %= 360

    # df = df.round(decimals=1)
    df['Indexes'] = df['Interval'].apply(lambda x: num2range(x, index=True))
    df['Interval'] = df['Interval'].apply(lambda x: num2range(x))
    df['Direction'] = df['Direction'].apply(lambda x: num2dir(x))
    print(df.head())

    grp = df.groupby(["Indexes", "Direction", "Interval"]).size().reset_index(name="frequency")
    grp.sort_values(by='Indexes')
    totals = grp['frequency'].sum()
    grp['Percentiles'] = grp['frequency'].apply(lambda x:
                                                100 * x / totals)
    grp['Percentiles'] = pd.Series(["{0:.2f}%".format(val) for val in grp['Percentiles']], index=grp.index)

    print(grp.head())

    # Dirs

    fig = px.bar_polar(grp, r='frequency', theta="Direction", hover_data=["Percentiles"],
                       color="Interval", template="plotly_dark",
                       color_discrete_sequence=px.colors.sequential.Plasma_r,
                       category_orders={
                           "Direction": ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W',
                                         'WNW', 'NW', 'NNW']}
                       )
    #fig.show()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON