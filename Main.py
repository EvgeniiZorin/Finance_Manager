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
import settings as st


class Application:
	def __init__(self, window, test:bool):
		self.window = window
		self.test = test
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
		frame1 = Label(self.window, text="Welcome to the Finance Manager!\nHere, you can visualise your spendings in nice graphs!", font=st.font_title )
		frame1.grid(columnspan=5, column=0, row=1, padx=30)
		# SELECT FILE button
		self.select_file_button()
		# EXIT button
		self.exit_button()
		# TEST condition - if True, choose a pre-selected file
		if self.test == True:
			self.open_file(True)
		Label(window, text="").grid(columnspan=5, column=0, row=5)

	def select_file_button(self):
		browse_text = StringVar()
		browse_text.set('loading...')
		select_file_btn = Button(
			window, command=lambda:self.open_file(False), 
			bg=st.button_colour, width=st.button_width, relief='flat', 
			textvariable=browse_text, font=st.button_font1, fg=st.button_text_colour
		)
		browse_text.set('Select File')
		select_file_btn.grid(columnspan=5, column=0, row=2)

	def exit_button(self):
		exit_btn = Button(
			window, command=window.quit, 
			bg = st.button_colour, width=st.button_width, relief='flat',
			text='Exit', font=st.button_font1, fg='#AF0000'
		)
		exit_btn.grid(columnspan=5, column=0, row=3, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])

	def B2_newWindow(self, file):
		newWindow = Toplevel(window)
		newWindow.title('New window')
		newWindow.geometry("380x170")
		newWindow.resizable(False, False)
		Label(
			newWindow, 
			bg=st.frame_colour,
			text='Print totals per month (specified year)', font=st.frame_text_font
		).grid(columnspan=4, column=0, row=2, padx=st.newWin_pad_outside[0], pady=st.newWin_pad_outside[1])
		e1 = Entry(
			newWindow, justify='center', 
			width=15
		)
		e1.grid(columnspan=4, column=0, row=3, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])
		btn3_2 = Button(
			newWindow, command=lambda: B2_totals_specificYear(file, e1.get()),
			bg=st.button_colour, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
			text='RUN', font=st.button_font2, fg=st.button_text_colour
		); 
		btn3_2.grid(column = 3, row=3, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])

	def B3_newWindow(self, file):
		newWindow = Toplevel(window)
		newWindow.title('New window')
		newWindow.geometry("330x170")
		newWindow.resizable(False, False)
		Label(
			newWindow, 
			bg=st.frame_colour, 
			text='Print totals per month in a range', font=st.frame_text_font
		).grid(columnspan=3, column=0, row=0, padx=st.newWin_pad_outside[0], pady=st.newWin_pad_outside[1])
		Label(
			newWindow, 
			# bg=st.frame_colour,
			text='Example: 2021.09 - 2021.12\n', font=st.frame_text_font2
		).grid(columnspan=3, column=0, row=1)
		x1=50; y1=120; delta=80
		e2 = Entry(newWindow, justify='center', width=10)
		e2.place(x=x1, y=y1)
		Label(
			newWindow,
			# bg=st.frame_colour, 
			text='-'
		# ).grid(column=2, row=3)
		).place(x=x1+delta, y=y1)
		e3 = Entry(newWindow, justify='center', width=10)
		e3.place(x=x1+delta*1.4, y=y1)
		# e2.grid(column=3, row=3)
		btn3_3 = Button(
			newWindow, command=lambda: B3_totals_specificRange(file, e2.get(), e3.get()),
			bg=st.button_colour, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
			text='RUN', font=st.button_font2, fg=st.button_text_colour
		)
		btn3_3.place(x=x1+delta*2.4, y=y1)

	def B4_newWindow(self, file):
		newWindow = Toplevel(window)
		newWindow.title('New window')
		newWindow.geometry("450x220")
		# newWindow.resizable(False, False)
		x1=50; y1=10; delta=80
		Label(
			newWindow, 
			bg=st.frame_colour,
			text='Print totals per month for a chosen category', font=st.frame_text_font
		).grid(columnspan=4, column=0, row=7, padx=st.newWin_pad_outside[0], pady=st.newWin_pad_outside[1])
		Label(
			newWindow, 
			text='E.g. "bills", 2022.01 - 2022.09', font=st.frame_text_font2
		).place(x=x1, y=y1+50)
		categories1 = unique_spending_categories(file)
		clicked = StringVar()
		clicked.set(categories1[0])
		drop = OptionMenu(newWindow, clicked, *categories1).place(x=x1,     y=y1+100)
		e2_4_a = Entry(newWindow, justify='center'); e2_4_a.place(x=x1,     y=y1+160, width=80)
		Label(
			newWindow, 
			text=' - ', font=st.frame_text_font
		).place(x=x1+90, y=y1+150)
		e2_4_b = Entry(newWindow, justify='center'); e2_4_b.place(x=x1+130, y=y1+160, width=80)
		btn3_4 = Button(
			newWindow, command=lambda: dropdown(file, clicked.get(), e2_4_a.get(), e2_4_b.get()),
			bg=st.button_colour, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
			text='RUN', font=st.button_font2, fg=st.button_text_colour
		).place(x=x1+230, y=y1+150)


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
			# window.geometry('1070x900')
			window.geometry('900x900')
			Label(window, text=f"You have selected: {file}").grid(columnspan=5, column=0, row=4, pady=15)
			# Got the filename, now can put it to all the functions
			browse_text.set('Select File')
			### 
			# FRAME 1
			# Canvas(window, height=500, width=500, bg=st.button_colour).grid(column=0, row=5)
			Canvas(window, height=450, width=450).grid(column=0, row=5)
			frame1 = LabelFrame(
				window, padx=50, pady=10, 
				bg=st.frame_colour, relief='flat',
				text='Information', font=st.font_frame_title, 
			)
			frame1.grid(column=0, row=5, padx=50)
			##############################################################
			#####   A1: Print unique spending categories   ###############
			##############################################################
			btn1_1 = Button(
				frame1, command=lambda: A1_unique_spending_categories(file, frame1),
				bg=st.button_colour, width=st.button_width, relief='flat', padx=st.button_pad_inside[0], pady=st.button_pad_inside[1],
				text="Print unique spending categories", font=st.button_font2, fg=st.button_text_colour
			)
			btn1_1.grid(row=0, column=0, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])
			##############################################################################
			#####   A2: Print period for which finance data is available   ###############
			##############################################################################
			btn1_2 = Button(
				frame1, command=lambda: A2_data_available(file, frame1), 
				bg=st.button_colour, width=st.button_width, relief='flat', padx=st.button_pad_inside[0], pady=st.button_pad_inside[1],
				text='Print period for which \nfinance data is available', font=st.button_font2, fg=st.button_text_colour, 
			)
			btn1_2.grid(row=3, column=0, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])
			# c2 = Text(frame1, height=2, width=st.button_width, padx=15, pady=15, font=st.font_body )
			# c2.grid(column=0, row=4)
			# FRAME 2
			frame2 = LabelFrame(
				window, padx=50, pady=50, 
				bg=st.frame_colour, relief='flat',
				text="Graphs", font=st.font_frame_title,
			)
			frame2.grid(column=1, row=5)
			##############################################################
			#####   B1: Print totals per month (all time)   ##############
			##############################################################
			Button(
				frame2, command=lambda: B1_totals_allTime(file),
				bg=st.button_colour, width=st.button_width, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
				text='Print totals per month\n(all time)', font=st.button_font2, fg=st.button_text_colour, 
			).grid(columnspan=4, column=0, row=0)
			####################################################################
			#####   B2: Print totals per month (specified year)   ##############
			####################################################################
			# In the new window, need to make an error that doesn't print the plot if you don't input a year
			Button(
				frame2, command=lambda: self.B2_newWindow(file),
				bg=st.button_colour, width=st.button_width, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
				text='Print totals per month\n(specific year)\ne.g. 2022', font=st.button_font2, fg=st.button_text_colour
			).grid(columnspan=4, column = 0, row=1, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])
			####################################################################
			#####   B3: Print totals per month (specified range)   #############
			####################################################################
			Button(
				frame2, command=lambda: self.B3_newWindow(file),
				bg=st.button_colour, width=st.button_width, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
				text='Print totals per month\n(specified range)\ne.g. 01.2022 - 09.2022', font=st.button_font2, fg=st.button_text_colour
			).grid(columnspan=4, column = 0, row=2, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])
			x1=50; y1=240
			################################################################################################
			#####   B4: Print totals per month for a chosen category, for a specified range   ##############
			################################################################################################
			Button(
				frame2, command=lambda: self.B4_newWindow(file),
				bg=st.button_colour, width=st.button_width, relief='flat', padx=st.button_pad_inside[0], pady= st.button_pad_outside[1],
				text='Print totals per month\n(for a chosen category)\ne.g. "bills"', font=st.button_font2, fg=st.button_text_colour
			).grid(columnspan=4, column = 0, row=3, padx=st.button_pad_outside[0], pady=st.button_pad_outside[1])







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
	categories_list = Text(frame1, height=10, width=st.button_width, padx=15, pady=15, font=st.font_body )
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
	text_available_dates = Text(frame1, height=2, width=st.button_width, padx=15, pady=15, font=st.font_body , wrap=WORD)
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
	###### DATA VISUALISATION
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
	plt.suptitle("Suptitle")
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
	###### DATA PROCESSING
	dfHeader, dfMain = dataset_process_basic(pathed_filename)
	currency = 'MXN'; 
	dfMain = convert(dfMain, currency)
	# Add extra time information
	dfMain2 = dfMain.groupby('Date')[f'Converted_{currency}'].sum().to_frame().reset_index()
	dfMain2 = add_extra_dates(dfMain2)
	df3 = dfMain2[dfMain2['YYYY'] == year]
	df3['MM'] = dfMain2['Date'].dt.strftime('%b')
	###### DATA VISUALISATION

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
	graph = sns.lineplot( x='MM', y=f'Converted_{currency}', data=df3, color='grey' )
	plt.xticks(rotation=90)
	plt.title(f"Spendings in {year}", fontweight='bold')
	plt.suptitle("Suptitle")
	plt.xlabel('   '); plt.ylabel(f'Spending ({currency})')
	# 
	mean_spend = df3[f'Converted_{currency}'].mean()
	plt.axhline(mean_spend, color='grey', ls='dotted')
	max_date = df3['Date'].max()
	print(max_date)
	max_date2 = max_date.strftime('%m.%y')
	print(max_date2)
	plt.text( max_date2 , mean_spend, 'Mean', horizontalalignment='left', verticalalignment='bottom', color='#717171' )
	#
	plt.legend([], [], frameon=False)
	graph.xaxis.grid()
	plt.show()



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
	# ---------------------------------------------------
	# Object of Application class
	# Normal run:
	obj = Application(window=window, test=False)
	# ## Test (to open a local file automatically):
	# obj = Application(window=window, test=True)
	# ---------------------------------------------------
	# End the program
	window.mainloop()