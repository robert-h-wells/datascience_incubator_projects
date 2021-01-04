from bokeh.plotting import figure, show, output_file, save
from bokeh.models.widgets import Tabs, Panel
from math import pi
from bokeh.palettes import Category10
from bokeh.transform import cumsum
from bokeh.models import Legend


def ticker_plot(df,symbol,stock_val,start,end):

    p0 = figure(plot_width=800, plot_height=600, background_fill_color="#fafafa")

    x_nam = list(df.index)
    x = list(range(len(df['Close'].values)))

    x_nam_dict = {}
    for i in x:
        x_nam_dict[i] = x_nam[i].strftime('%b-%d-%y')
    
    legend_list = []
    if stock_val[0] == True:
        r0 = p0.line(x,list(df['Close'].values), line_width =2, color='blue', 
            legend=str(symbol+': Close'))

    if stock_val[1] == True:
        r1 = p0.line(x,list(df['Adj Close'].values), line_width =2, color='red',
            legend=str(symbol+': Adj close'))

    if stock_val[2] == True:
        r2 = p0.line(x,list(df['Open'].values), line_width =2, color='green',
            legend=str(symbol+': Open'))

    diviser = 1
    if len(x) > 20:
        for i in range(1,20):
            diviser = i
            if float(len(x)/i) <= 20.0:
                break

    p0.title.text = ('Share Price Data Between '+start.strftime('%m-%d-%Y')+' and '+end.strftime('%m-%d-%Y'))

    p0.xaxis.ticker = x[::diviser]
    p0.xaxis.major_label_overrides = x_nam_dict
    p0.xaxis.major_label_orientation = pi/4
    p0.xaxis.major_label_text_font_style = "bold"
    p0.yaxis.major_label_text_font_style = "bold"

    p0.yaxis.axis_label = 'Share Price ($)'
    p0.yaxis.axis_label_text_font_style = "bold"

    return(p0)