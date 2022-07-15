from tkinter import *
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd


############################################################################
#####   Backend   ##########################################################
############################################################################


### Data processing functions
############################################################################

def dataset_process_basic():
	"""
	Dataproc step1: Import and clean the data
	"""
	try:
		currDir = os.path.dirname(__file__)
		df = pd.read_csv(f'{currDir}/Finance_ver2.tsv', sep='\t')
		print(f"{currDir}/Finance_ver2.tsv")
	except NameError:
		df = pd.read_csv('Finance_ver2.tsv', sep='\t')
	dfHeader = df[df['Date'] == '#'].copy()
	dfMain   = df[df['Date'] != '#'].copy()
	dfMain['Date'] = pd.to_datetime(dfMain['Date'], format='%d.%m.%Y')
	# Reset index to compensate for not including Header rows (ones with '#'):
	dfMain.reset_index(inplace=True) 
	return dfHeader, dfMain

def convert(df, finalCurrency):
	"""
	Dataproc step2: Convert the currency into desired currency 
	\nprocFunction to convert your spendings 
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

def add_extra_dates(dfMain):
	"""
	Dataproc step3 (optional): add extra datetime formats to the dataset
	"""
	dfMain['DDMM']   = dfMain['Date'].dt.strftime('%d.%m')
	dfMain['DDMMYY'] = dfMain['Date'].dt.strftime('%d.%m.%y')
	dfMain['YYYY']   = dfMain['Date'].dt.strftime('%Y')
	dfMain['MMYY']   = dfMain['Date'].dt.strftime('%m.%y')
	return dfMain

### Data summarisation and visualisation
############################################################################

def function1():
	"""
	Print unique counts of spending categories
	"""
	dfHeader, df2 = dataset_process_basic()
	array = df2['Category'].unique()
	textOutput = ''
	textOutput += f"Spending categories:\n"
	c=1; 
	for i in array: textOutput += f"  {c}) {i}\n"; c+=1
	return textOutput

def plot1():
	"""
	Toy plot
	"""
	x = np.arange(0, 10+1, 1)
	# axes.plot(x, x + 5)
	graph1 = sns.regplot(x, x*2)
	plt.show()


# Plot2 - plot totals per month (all time)
def plot2():
	"""
	Print totals per month (all-time)
	"""
	dfHeader, dfMain = dataset_process_basic()
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	# Graph
	graph = sns.catplot(x='MMYY', y=f'Converted_{currency}', data=dfMain2, kind='bar', color='grey')
	graph.set_xticklabels(rotation=90, horizontalalignment='right')
	plt.xlabel(''); plt.ylabel(f'Spending ({currency})')
	sns.set_style('whitegrid')
	sns.set_context('poster')
	plt.show()

def plot2_ver2():
	dfHeader, dfMain = dataset_process_basic()
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	# Graph
	plt.figure(figsize=(8, 6))
	graph = sns.barplot(x='MMYY', y=f'Converted_{currency}', data=dfMain2, hue='YYYY', dodge=False)
	plt.xticks(rotation=90)
	plt.xlabel(''); plt.ylabel(f'Spending ({currency})')
	plt.legend([], [], frameon=False)
	sns.set_style('whitegrid')
	sns.set_context('poster')
	plt.show()


def plot3(year):
	dfHeader, dfMain = dataset_process_basic()
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	dfMain2
	df3 = dfMain2[dfMain2['YYYY'] == year]
	df3['MM'] = dfMain2['Date'].dt.strftime('%b')
	# df3 = df2[ (df2['Date'] < endDate) & (df2['Date'] > startDate) ]
	# Check that between the two dates the distance is less than 6 months
	# startDateDT = datetime.datetime(int(startDate.split('-')[0]), int(startDate.split('-')[1]), int(startDate.split('-')[2]))
	# endDateDT = datetime.datetime(int(endDate.split('-')[0]), int(endDate.split('-')[1]), int(endDate.split('-')[2]))
	# delta = endDateDT - startDateDT
	# deltaDays = (delta.total_seconds() /(3600*24))
	# assert deltaDays < 181, 'the number is higher than 6 months!'
	# Plot the figure
	plt.figure(figsize=(8, 6))
	sns.barplot(x='MM', y=f'Converted_{currency}', data=df3, color='grey')
	plt.xlabel('Date')
	plt.legend([], [], frameon=False)
	plt.suptitle(f'Monthly spendings in {year}')
	sns.set_context('poster')
	plt.show()
	# return df3

def plot4(startDate, endDate):
	dfHeader, dfMain = dataset_process_basic()
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	dfMain2
	df3 = dfMain2[ (dfMain2['Date'] <= endDate) & (dfMain2['Date'] >= startDate) ]
	# Check that between the two dates the distance is less than 6 months
	startDateDT = datetime.datetime(int(startDate.split('-')[0]), int(startDate.split('-')[1]), int(startDate.split('-')[2]))
	endDateDT = datetime.datetime(int(endDate.split('-')[0]), int(endDate.split('-')[1]), int(endDate.split('-')[2]))
	delta = endDateDT - startDateDT
	deltaDays = (delta.total_seconds() /(3600*24))
	assert deltaDays < 181, 'the number is higher than 6 months!'
	# Plot the figure
	plt.figure(figsize=(10, 8))
	sns.barplot(x='DDMMYY', y=f'Converted_{currency}', data=df3, hue='YYYY', dodge=False)
	plt.xlabel('Date')
	plt.legend([], [], frameon=False)
	plt.show()
	# return df3

###########################

window = Tk()
window.title('Finance manager ver 5.0.0')
window.geometry('1300x600')

font='Helvetica 15'
pad = [10, 10]

# Frame 1
# Description
frame1 = LabelFrame(window, text="Welcome!", padx=50, pady=50)
frame1.grid(row=0, column=0)
Label(frame1, text='This program allows to visualise your spendings in nice graphs.').grid(row=0, column=0)
exit_button = Button(frame1, text="EXIT", command=window.quit, padx=30) # command=window.destroy
exit_button.grid(row=1, column=0)

# btn1_1 = Button(frame1, text="Press this to print unique spending categories"); btn1_1.grid(row=3, column=0)

# Frame 2
def printCats():
	# # os.system('python ./Main.py')
	# #
	# print(os.getcwd())
	# currDir = os.path.dirname(__file__)
	# print(currDir)
	# os.system(f'python {currDir}/Main.py')
	#
	a = function1()
	global frame2_cats_label 
	frame2_cats_label = Label(frame2, text=a).grid(row=2, column=0)


frame2 = LabelFrame(window, text="Spending categories", padx=50, pady=50, font=font)
frame2.grid(row=0, column=1, padx=10, pady=10)
Label(frame2, text="This feature allows you to print the unique spending categories \npresent in the indicated file").grid(row=0, column=0)
btn2_1 = Button(frame2, text='RUN', command=printCats); btn2_1.grid(row=1, column=0)

# Frame 3
frame3 = LabelFrame(window, text="Finance graphs", padx=50, pady=50, font=font)
frame3.grid(row=0, column=2)
Label(frame3, text="Create different graphs").grid(row=0, column=0)
btn3_1 = Button(frame3, text='Print totals per month (all time)', command=plot2_ver2); btn3_1.grid(row=1, column=0)

e1 = Entry(frame3, width=20); e1.grid(row=2, column=2)
btn3_2 = Button(frame3, text='Print totals per month (specified year)', command=lambda: plot3(e1.get())); btn3_2.grid(row=2, column=0)
Label(frame3, text='Example: 2021').grid(row=2, column=1)

Label(frame3, text='e2').grid(row=4, column=1)
e2 = Entry(frame3); e2.grid(row=4, column=2)
Label(frame3, text='e3').grid(row=5, column=1)
e3 = Entry(frame3); e3.grid(row=5, column=2)
btn3_3 = Button(frame3, text='Print totals per month in the specified range', command=lambda: plot4(e2.get(), e3.get())); btn3_3.grid(row=4, column=0)

window.mainloop()
