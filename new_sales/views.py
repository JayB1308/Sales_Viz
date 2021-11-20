from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
import pandas as pd
import json
from .models import Report
from .forms import FileUploadForm,CreateUserForm,LoginForm


def home(request):
	return render(request,'home.html')

def about(request):
	return render(request,'about.html')

def get_started(request):
	return render(request,'get_started.html')


def create_user(request):
	form = CreateUserForm()
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
		else:
			form = CreateUserForm()

	context = {
	'form':form
	}
	return render(request,'register.html',context)

def login_user(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
	else:
		form = LoginForm()

	context = {
	'form': form
	}
	return render(request,'login.html',context)

def logout_user(request):
	logout(request)
	return redirect('login')


def upload_file(request):
	form=FileUploadForm()
	if request.method =='POST':
		form = FileUploadForm(request.POST,request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			df = pd.read_excel(file)
			data=get_best_product(df)
			sales_list=get_Best_Customer(df)
			context = {
			'product_data': json.dumps(
		[
			{
				'Type':product['Type'],
				'Quantity':int(product['Quantity'])
			}
			for product in data
		]
		),
			'customer_data' : json.dumps(
		[
			{
				'Customer': customer['Customer'],
				'Sales': int(customer['Sales'])
			}
			for customer in sales_list
		])
		,
		'avg_sales':int(get_Average_Sales(df)),
		'total_sales':get_Total_Sales(df),
		'best_customer':best_customer(df),
		'best_product':best_product(df)
		}
			return render(request,'dashboard.html',context)
	else:
		form=FileUploadForm()
	return render(request,'file_upload.html',context={'form':form})

def generate_dashboard(request):
	print(context)
	return render(request,'dashboard.html',context)

def product_chart(df):
	new_context = {
		'product_data': json.dumps(
		[
			{
				'Type':product['Type'],
				'Quantity':int(product['Quantity'])
			}
			for product in data
		]
		),
	}
	context.update(new_context)

def customer_chart(df):

	new_context = {
	'customer_data' : json.dumps(
		[
			{
				'Customer': customer['Customer'],
				'Sales': int(customer['Sales'])
			}
			for customer in sales_list
		]
		)
	}
	context.update(new_context)

def get_best_product(df):
	product_list = []
	product_data = []
	for i in df.index:
		if df.at[i,'Product_Type'] not in product_list:
			product_list.append(str(df.at[i,'Product_Type']))
			product={
			'Type':str(df.at[i,'Product_Type']),
			'Quantity':0
			}
			product_data.append(product)

	for i in range(len(product_list)):
		for j in df.index:
			if str(df.at[j,'Product_Type']) == product_list[i]:
				product_data[i]['Quantity']+=df.at[j,'Quantity']

	return product_data


def get_Total_Sales(df):
	total_sales=0
	for i in df.index:
		total_sales+=df.at[i,'Total']
	return total_sales

def get_Average_Sales(df):
	number_of_records=len(df)
	sales=get_Total_Sales(df)
	average_sales=sales/number_of_records
	return average_sales


def get_Best_Customer(df):
	customer_list = []
	sales_list = []
	for i in df.index:
		if df.at[i,'Customer_Name'] not in customer_list:
			customer_list.append(str(df.at[i,'Customer_Name']))
			sales_list.append(
				{
				'Customer':str(df.at[i,'Customer_Name']),
				'Sales': 0
				})
	for i in range(len(customer_list)):
	 	for j in df.index:
	 		if str(df.at[j,'Customer_Name']) == customer_list[i]:
	 			sales_list[i]['Sales'] += int(df.at[j,'Total'])
	return sales_list

def best_customer(df):
	data = get_Best_Customer(df)
	customer = data[0]
	for i in range(len(data)):
		if data[i]['Sales'] > customer['Sales']:
			customer = data[i]

	return customer

def best_product(df):
	sales_list = get_best_product(df)
	product = sales_list[0]
	for i in range(len(sales_list)):
		if sales_list[i]['Quantity'] > product['Quantity']:
			product = sales_list[i]

	return product