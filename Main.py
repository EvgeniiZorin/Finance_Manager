from tkinter import *
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename

# Aesthetics

bg1 = 'lightgrey'
bgButton='#a3a3a3'
btnWidth = 30
# window.config(bg=bg1)
# padx=30, # padding on the buttons
# Helvetica
fontTitle='Helvetica 15'
fontBody='Helvetica 12'
pad = [10, 10]
button_pad = [5, 5]
fontFrameTitle = 'Helvetica 10'


class Application:
	def __init__(self, window):
		self.window = window
		version = '3.4.0'
		self.window.title(f'Finance manager ver {version}')
		s = ttk.Style()
		s.configure('User.TLabelFrame', bordercolor='white')
		# Logo
		logo = Image.open('Media/dollar_house.png')
		logo = logo.resize((250, 155), Image.ANTIALIAS)
		logo = ImageTk.PhotoImage(logo)
		logo_label = Label(image=logo)
		logo_label.image = logo
		logo_label.grid(columnspan=5, column=0, row=0, pady=30)
		## Main Menu with description
		frame1 = Label(self.window, text="Welcome to the Finance Manager!\nHere, you can visualise your spendings in nice graphs!", font=fontTitle)
		frame1.grid(columnspan=5, column=0, row=1, padx=30)
		# EXIT button
		exit_btn = Button(window, text='EXIT', command=window.quit, font=fontBody, bg='#ff6459', width=btnWidth)
		exit_btn.grid(columnspan=5, column=0, row=2, padx=button_pad[0], pady=button_pad[1])
		# SELECT FILE button
		browse_text = StringVar()
		select_file_btn = Button(window, textvariable=browse_text, command=lambda:self.open_file(False), font=fontBody, bg=bgButton, width=btnWidth)
		browse_text.set('Select File')
		select_file_btn.grid(columnspan=5, column=0, row=3)
		# ## FOR TESTING ONLY
		# open_file(True)
		Label(window, text="").grid(columnspan=5, column=0, row=5)



	## Select File Prompt
	def open_file(self, pre_selected_file):
		browse_text = StringVar()
		if pre_selected_file == True:
			"""Option for testing only"""
			# file = 'C:/Users/evgen/Desktop/Python/Finance_manager/Finance_manager_v3.2.1/Finance_record.tsv'
			file = 'Finance_record.tsv'
		else:
			browse_text.set('loading...')
			file = askopenfilename(filetype=[("TSV file", "*.tsv")])
		if file:
			window.geometry('1070x900')
			Label(window, text=f"You have selected: {file}").grid(columnspan=5, column=0, row=4, pady=15)
			print(file)
			# Got the filename, now can put it to all the functions
			browse_text.set('Select File')
			### 
			# FRAME 1
			Canvas(window, height=425, width=410).grid(column=0, row=5)
			frame1 = LabelFrame(window, text="Information", padx=50, pady=10, font=fontFrameTitle)
			frame1.grid(column=0, row=5, padx=50)
			##############################################################
			#####   A1: Print unique spending categories   ###############
			##############################################################
			btn1_1 = Button(frame1, text="Print unique spending categories", command=lambda: A1_unique_spending_categories(file, frame1), font=fontBody, bg=bgButton, width=btnWidth)
			btn1_1.grid(row=0, column=0, padx=button_pad[0], pady=button_pad[1])
			##############################################################################
			#####   A2: Print period for which finance data is available   ###############
			##############################################################################
			btn1_2 = Button(frame1, text='Print period for which \nfinance data is available', command=lambda: A2_data_available(file, frame1), font=fontBody, bg=bgButton, width=btnWidth)
			btn1_2.grid(row=3, column=0, padx=button_pad[0], pady=button_pad[1])
			# c2 = Text(frame1, height=2, width=btnWidth, padx=15, pady=15, font=fontBody)
			# c2.grid(column=0, row=4)
			# FRAME 2
			frame2 = LabelFrame(window, text="Graphs", padx=50, pady=50, font=fontFrameTitle)
			frame2.grid(column=1, row=5)
			##############################################################
			#####   B1: Print totals per month (all time)   ##############
			##############################################################
			Label(frame2, text='Print totals per month (all time)', font='Helvetica 15 bold').grid(columnspan=4, column=0, row=0, pady=button_pad[1])
			btn3_1 = Button(frame2, text='RUN', command=lambda: B1_totals_allTime(file), font=fontBody, bg=bgButton, width=btnWidth)
			btn3_1.grid(columnspan=4, column=0, row=1)
			####################################################################
			#####   B2: Print totals per month (specified year)   ##############
			####################################################################
			Label(frame2, text='Print totals per month (specified year)', font='Helvetica 15 bold').grid(columnspan=4, column=0, row=2, pady=button_pad[1])
			e1 = Entry(frame2, width=btnWidth)
			e1.grid(columnspan=4, column=0, row=3, padx=button_pad[0], pady=button_pad[1])
			btn3_2 = Button(frame2, text='RUN', command=lambda: B2_totals_specificYear(file, e1.get()), font=fontBody, bg=bgButton); 
			btn3_2.grid(column = 3, row=3, padx=button_pad[0], pady=button_pad[1])
			####################################################################
			#####   B3: Print totals per month (specified range)   #############
			####################################################################
			Label(frame2, text='Print totals per month in the specified range', font='Helvetica 15 bold').grid(columnspan=4, column=0, row=4, pady=button_pad[1])
			Label(frame2, text='Example: 2021.09 - 2021.12').grid(columnspan=4, column=0, row=5)
			x1=50; y1=220
			e2 = Entry(frame2); e2.place(x=x1, y=y1)
			Label(frame2, text='-').place(x=x1+130, y=y1)
			e3 = Entry(frame2); e3.place(x=x1+150, y=y1)
			btn3_3 = Button(frame2, text='RUN', command=lambda: B3_totals_specificRange(file, e2.get(), e3.get()), font=fontBody, bg=bgButton)
			btn3_3.place(x=x1+290, y=y1-6)
			################################################################################################
			#####   B4: Print totals per month for a chosen category, for a specified range   ##############
			################################################################################################
			Label(frame2, text='').grid(column=10, row=6)
			Label(frame2, text='Print totals per month for a chosen category', font='Helvetica 15 bold').grid(columnspan=4, column=0, row=7, pady=button_pad[1]+20)
			categories1 = unique_spending_categories(file)
			clicked = StringVar()
			clicked.set(categories1[0])
			drop = OptionMenu(frame2, clicked, *categories1).place(x=x1-80, y=y1+90)
			e2_4_a = Entry(frame2); e2_4_a.place(x=x1+100, y=y1+95, width=80)
			e2_4_b = Entry(frame2); e2_4_b.place(x=x1+200, y=y1+95, width=80)
			btn3_4 = Button(frame2, text='RUN', command=lambda: dropdown(file, clicked.get(), e2_4_a.get(), e2_4_b.get()), font=fontBody, bg=bgButton).place(x=x1+300, y=y1+90)





############################################################################
#####   Functions   ########################################################
############################################################################

def dataset_process_basic(file_name):
	"""
	Dataproc step1: Import and clean the data
	"""
	# try:
	# 	currDir = os.path.dirname(__file__)
	# 	df = pd.read_csv(f'{currDir}/{file_name}', sep='\t')
	# 	print(f"{currDir}/{file_name}")
	# except NameError:
	# 	df = pd.read_csv('{file_name}', sep='\t')
	df = pd.read_csv(file_name, sep='\t')
	# print(f"{currDir}")
	# print(f"{file_name}")
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


############################################################################
#####   Data Visualisation   ###############################################
############################################################################

"""
Legend:
---
A = data summary
B = data graphs and visualisations
"""

def unique_spending_categories(pathed_filename:str) -> list:
	"""
	Generic function. 

	Returns a list of unique spendings categories. 
	"""
	dfHeader, df2 = dataset_process_basic(pathed_filename)
	array = df2['Category'].unique()
	return array

def A1_unique_spending_categories(file, frame1):
	"""
	Print unique spending categories
	
	This function activates upon pressing of a button, printing unique spending categories in the GUI field
	"""
	a_list = unique_spending_categories(file)
	a = ''
	a += "Spending categories:\n"
	c = 1; 
	for i in a_list: a += f"  {c}) {i}\n"; c+=1
	#
	global categories_list 
	categories_list = Text(frame1, height=10, width=btnWidth, padx=15, pady=15, font=fontBody)
	categories_list.insert(1.0, a)
	# Center the text
	categories_list.tag_configure('left', justify='left')
	categories_list.tag_add('left', 1.0, 'end')
	categories_list.grid(column=0, row=2)

def A2_data_available(file, frame1):
	dfHeader, dfMain = dataset_process_basic(file)
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	print(dfMain2['Date'].min().to_pydatetime().strftime('%d.%m.%Y'))
	print(dfMain2['Date'].max().to_pydatetime().strftime('%d.%m.%Y'))
	a = f"Data is available from {str(dfMain2['Date'].min().to_pydatetime().strftime('%d.%m.%Y'))} to {str(dfMain2['Date'].max().to_pydatetime().strftime('%d.%m.%Y'))}"
	# str(dfMain2['Date'].min().to_pydatetime().strftime('%d.%m.%Y')) + ' ' + str(dfMain2['Date'].max().to_pydatetime().strftime('%d.%m.%Y'))
	text_available_dates = Text(frame1, height=2, width=btnWidth, padx=15, pady=15, font=fontBody, wrap=WORD)
	text_available_dates.insert(1.0, a)
	text_available_dates.tag_configure('left', justify='left')
	text_available_dates.tag_add('left', 1.0, 'end')
	text_available_dates.grid(column=0, row=4)

def plot2(pathed_filename):
	"""
	Print totals per month (all-time)
	"""
	dfHeader, dfMain = dataset_process_basic(pathed_filename)
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

def B1_totals_allTime(pathed_filename):
	###### DATA PROCESSING
	dfHeader, dfMain = dataset_process_basic(pathed_filename)
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	# GRAPH STYLE
	plt.figure(figsize=(12, 6))
	sns.set_context('talk')
	sns.set_style('whitegrid', {
		# Axes text
		# Remove axis spines
		'axes.spines.left': False, 
		'axes.spines.right': False, 
		'axes.spines.top': False,
		# Y-axis Left
		'ytick.left': False,
		'ytick.color': '#717171',
		# X-axis bottom
		'xtick.bottom': True,
		'axes.edgecolor': '#D9D9D9',
		'xtick.color': '#717171',
		# Axes grid
		'grid.color': '#F3F3F3', 
	}) 
	sns.set_context('talk')
	# plt.tight_layout()
	plt.subplots_adjust(bottom=0.15)
	# graph = sns.barplot(x='MMYY', y=f'Converted_{currency}', data=dfMain2, hue='YYYY', dodge=False)
	graph = sns.lineplot( x='MMYY', y=f'Converted_{currency}', data=dfMain2, hue='YYYY' )
	plt.xticks(rotation=90)
	plt.title("All-time spendings", fontweight='bold')
	plt.xlabel('   '); plt.ylabel(f'Spending ({currency})')
	# 
	mean_spend = dfMain2[f'Converted_{currency}'].mean()
	plt.axhline(mean_spend, color='grey', ls='dotted')
	max_date = dfMain2['Date'].max()
	print(max_date)
	max_date2 = max_date.strftime('%m.%y')
	print(max_date2)
	plt.text( max_date2 , mean_spend, 'Mean', horizontalalignment='left', verticalalignment='bottom', color='#717171' )
	#
	plt.legend([], [], frameon=False)
	graph.xaxis.grid()
	# plt.style.use('')
	#
	plt.show()


def B2_totals_specificYear(pathed_filename, year):
	dfHeader, dfMain = dataset_process_basic(pathed_filename)
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	dfMain2
	df3 = dfMain2[dfMain2['YYYY'] == year]
	df3['MM'] = dfMain2['Date'].dt.strftime('%b')
	# Plot the figure
	plt.figure(figsize=(8, 6))
	sns.barplot(x='MM', y=f'Converted_{currency}', data=df3, color='grey')
	plt.xlabel('Date')
	plt.legend([], [], frameon=False)
	plt.suptitle(f'Monthly spendings in {year}')
	sns.set_context('poster')
	plt.show()
	# return df3

def B3_totals_specificRange(pathed_filename, startDate, endDate):
	"""
	startDate = '2022.03'
	endDate = '2022.05'
	"""
	dfHeader, dfMain = dataset_process_basic(pathed_filename)
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	df3 = dfMain2[ (dfMain2['Date'] >= startDate) & (dfMain2['Date'] <= endDate) ]
	# Plot the figure
	plt.figure(figsize=(10, 8))
	sns.barplot(x='DDMMYY', y=f'Converted_{currency}', data=df3, hue='YYYY', dodge=False)
	plt.xlabel('Date')
	plt.legend([], [], frameon=False)
	plt.show()


def dropdown(file, dropdown, entry1, entry2):
	# print('welp')
	# print(clicked.get())
	print(dropdown, entry1, entry2)
	B4_totals_specificRange_specificCategory(file, entry1, entry2, dropdown)


def B4_totals_specificRange_specificCategory(pathed_filename, startDate, endDate, category):
	dfHeader, dfMain = dataset_process_basic(pathed_filename)
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	dfMain = dfMain[dfMain['Category'] == category]
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	df3 = dfMain2[ (dfMain2['Date'] >= startDate) & (dfMain2['Date'] <= endDate) ]
	print(df3)
	# Plot the figure
	plt.figure(figsize=(10, 8))
	sns.barplot(x='DDMMYY', y=f'Converted_{currency}', data=df3, hue='YYYY', dodge=False)
	plt.xlabel('Date')
	plt.legend([], [], frameon=False)
	plt.show()


############################################################################
#####   GUI   ##############################################################
############################################################################



if __name__ == "__main__":
    # Instance of Tk class
    window = Tk()
    # Object of Application class
    obj = Application(window)
	# End the program
    window.mainloop()