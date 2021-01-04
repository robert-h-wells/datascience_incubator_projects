from flask import current_app as app
from flask import Flask, render_template, session 
from flask import redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from bokeh.embed import components
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, validators
from datetime import datetime, date, timedelta
from dateutil import relativedelta
import pandas_datareader.data as web

import plots as pl


class SymbolForm(FlaskForm):
    symbol = StringField('Ticker symbol:', validators=[validators.DataRequired()])
    begin_date = DateField('Beginning Date (MM-DD-YYYY):', format='%m-%d-%Y')
    end_date = DateField('End Date (Blank for current date):',format='%m-%d-%Y',
        validators=[validators.Optional()])
    close_price = BooleanField('Closing price')
    adj_close_price = BooleanField('Adjusted closing price')
    open_price = BooleanField('Open price')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SymbolForm()
    if form.validate_on_submit():
        session['symbol'] = form.symbol.data
        session['close'] = form.close_price.data
        session['adj_close'] = form.adj_close_price.data
        session['open'] = form.open_price.data
        session['begin'] = form.begin_date.data
        session['end'] = form.end_date.data

        print(session['begin'])
        print(session['end'])

        return redirect(url_for('graph'))
    return render_template('index.html', form=form, symbol=session.get('symbol'))

@app.route('/graph/')
def graph():

    # Get data information to lookup
    symbol = session['symbol']
    hist_days = 100

    # Get dates for stock data
    if not session['end']:  # left blank, current date
      end = datetime.strptime(date.today().strftime('%Y-%m-%d'),
              '%Y-%m-%d')
    else:
      end = datetime.strptime(session['end'],'%a, %d %b %Y %H:%M:%S %Z')

    start = datetime.strptime(session['begin'],'%a, %d %b %Y %H:%M:%S %Z')

    # Dataframe made from yahoo stock prices
    df = web.DataReader(symbol, 'yahoo', start, end)

    # Make plot figure
    plot_vals = [session['close'],session['adj_close'],session['open']]
    plot = pl.ticker_plot(df,symbol,plot_vals,start,end)
    script, div = components(plot)

    return render_template('graph.html', script=script, div=div)