import pandas as pd, numpy as np, os, sys
import matplotlib.pyplot as plt, seaborn as sns
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from matplotlib.dates import DateFormatter

def dataset_process_basic():
	try:
		currDir = os.path.dirname(__file__)
		df = pd.read_csv(f'{currDir}/Finance_ver2.tsv', sep='\t')
	except NameError:
		df = pd.read_csv('Finance_ver2.tsv', sep='\t')
	# currDir = os.path.dirname(__file__)
	# df = pd.read_csv(f'{currDir}/Finance_ver2.tsv', sep='\t')
	dfHeader = df[df['Date'] == '#'].copy()
	dfMain   = df[df['Date'] != '#'].copy()
	dfMain['Date'] = pd.to_datetime(dfMain['Date'], format='%d.%m.%Y')
	# Reset index to compensate for not including Header rows (ones with '#'):
	dfMain.reset_index(inplace=True) 
	return dfHeader, dfMain

def convert(df, finalCurrency):
	"""Function to convert your spendings 
	(written in different currencies)
	into whatever one currency you want. 
	E.g. RUB, MXN
	"""
	newColName = f'Converted_{finalCurrency}'
	df[newColName] = 0
	exchangeRate = {'RUB-MXN': 0.25, 'MXN-RUB': 4}
	for iter, i in enumerate(df['Currency']):
		if i == finalCurrency:
			# print( dfMain['Amount'].iloc[iter] )
			df[newColName].loc[iter] = df['Amount'].iloc[iter]
		else:
			a = i + '-' + finalCurrency
			df[newColName].loc[iter] = df['Amount'].iloc[iter] * exchangeRate[a]
	return df


def function1():
	"""
	Print unique counts of spending categories
	"""
	dfHeader, df2 = dataset_process_basic()
	# currDir = os.path.dirname(__file__)
	# df = pd.read_csv(f'{currDir}/Finance_ver2.tsv', sep='\t')
	# df2 = df[df['Date'] != '#']
	array = df2['Category'].unique()
	textOutput = ''
	textOutput += f"Spending categories:\n"
	c=1; 
	for i in array: textOutput += f"  {c}) {i}\n"; c+=1
	return textOutput
	# print("Spending categories:")
	# c=1; 
	# for i in array: print(f"  {c}) {i}"); c+=1

def plot1():
	"""
	Toy plot
	"""
	x = np.arange(0, 10+1, 1)
	# axes.plot(x, x + 5)
	graph1 = sns.regplot(x, x*2)
	plt.show()

def plot2():
	"""
	Print totals per month (all-time)
	"""
	dfHeader, dfMain = dataset_process_basic()
	currency = 'MXN'
	dfMain = convert(dfMain, currency)
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2['DDMM']   = dfMain2['Date'].dt.strftime('%d.%m')
	dfMain2['DDMMYY'] = dfMain2['Date'].dt.strftime('%d.%m.%y')
	dfMain2['YYYY']   = dfMain2['Date'].dt.strftime('%Y')
	dfMain2['MMYY']   = dfMain2['Date'].dt.strftime('%m.%y')
	dfMain2

	# Ver 2


	def plotTotals(df):
		# df2 = df.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
		# df2['DateProc'] = df2['Date'].dt.strftime('%d.%m.%y')
		# print(df2)
		graph = sns.catplot(x='MMYY', y=f'Converted_{currency}', data=df, kind='bar', color='grey')
		graph.set_xticklabels(rotation=90, horizontalalignment='right')
		sns.set_style('whitegrid')
		sns.set_context('talk')
		plt.show()
	#
	plotTotals(dfMain2)

def plot3():
	"""
	To plot totals per month in a specified year"""
	dfHeader, dfMain = dataset_process_basic()
	currency = 'MXN'
	dfMain = convert(dfMain, currency)
	dfMain

	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2['DDMM']   = dfMain2['Date'].dt.strftime('%d.%m')
	dfMain2['DDMMYY'] = dfMain2['Date'].dt.strftime('%d.%m.%y')
	dfMain2['YYYY']   = dfMain2['Date'].dt.strftime('%Y')
	dfMain2['MMYY']   = dfMain2['Date'].dt.strftime('%m.%y')
	dfMain2
	import datetime

	def plotTotals_2_1(df2, year):
		df3 = df2[df2['YYYY'] == year]
		df3['MM'] = dfMain2['Date'].dt.strftime('%b')
		# df3 = df2[ (df2['Date'] < endDate) & (df2['Date'] > startDate) ]
		# Check that between the two dates the distance is less than 6 months
		# startDateDT = datetime.datetime(int(startDate.split('-')[0]), int(startDate.split('-')[1]), int(startDate.split('-')[2]))
		# endDateDT = datetime.datetime(int(endDate.split('-')[0]), int(endDate.split('-')[1]), int(endDate.split('-')[2]))
		# delta = endDateDT - startDateDT
		# deltaDays = (delta.total_seconds() /(3600*24))
		# assert deltaDays < 181, 'the number is higher than 6 months!'
		# Plot the figure
		plt.figure(figsize=(10, 8))
		sns.barplot(x='MM', y=f'Converted_{currency}', data=df3, color='grey')
		plt.xlabel('Date')
		plt.legend([], [], frameon=False)
		plt.suptitle(f'Monthly spendings in {year}')
		plt.show()
		return df3

	plotTotals_2_1(dfMain2, '2021')
