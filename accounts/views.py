from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import date, datetime

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
	# if request.user.is_authenticated:
	# 	return redirect('home')
	# else:
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)

			return redirect('login')
			
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

class PasswordChangeView(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('password_success')

def PasswordSuccess(request):
	return render(request, 'accounts/password_success.html', {})



def loginPage(request):
	# if request.user.is_authenticated:
	# 	return redirect('index')
	# else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, 'Successfully logged in')
				return redirect('index')
				
			else:
				messages.error(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

# #####################################################
@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('home')



# @login_required(login_url='login')
# def profile(request):
# 	profile = UserData.objects.filter(status=True)
# 	marriage = Marriage.objects.filter(status = True)
# 	child = childdata.objects.all()
# 	# for i in marriage:
# 	# 		if (i.user == request.user):
# 	# 			print(i.your_cid )
# 	# 			print(i.Spousecid)
# 	# 		else:
# 	# 			for x in profile:
# 	# 				if (x.user == request.user):
# 	# 					print("jjdfh")
# 	# 					cids = str(i.Spousecid)
# 	# 					cids2 = str(request.user)
# 	# 					print(cids, cids2)
# 	# 					if cids == cids2:
# 	# 						print("sdhdfbjdh")
# 	# if request.method == "POST":
# 	# 	x = request.POST.get('name')
# 	# 	print(x)
# 	# product = get_object_or_404(UserData, id=product_id)

# 	return render(request, 'accounts/profile.html', 
# 	 {'profile': profile, 'marriage': marriage, 'child': child}
# 	)

@login_required(login_url='login')
def profile(request, user_id):
	profile = UserData.objects.filter(status=True)
	marriage = Marriage.objects.filter(status = True)
	child = childdata.objects.all()

	# print(child)
	# for i in child:
	# 	for x in marriage:
	# 		if i.user == x.Spousecid.user and x.user == request.user:
	# 				print(i.childname)
			

		
	
	for x in marriage:
		for i in child:
				if i.user == x.Spousecid.user and x.user == request.user:
					print(i.childname)
					print("if", request.user)
				elif request.user == i.user and request.user == x.Spousecid.user:
						print(i.childname)
				elif request.user == i.user and request.user == x.user:
					print(i.childname)
				elif i.user == x.user and request.user == x.Spousecid.user:
					print(i.childname)
				
				
		
			

	# for x in marriage:
	# 	for i in child:
	# 		if i.user == x.user:
	# 			if i.user == request.user:
	# 				print(i.childname, i.DOB)
					# print(x.Spousecid.user, i.childname)

				# elif i.user == x.Spousecid:
				# 	print(i.childname, i.DOB)

				
					

	if request.method == 'POST':
		x= request.POST['name']
		y= request.POST['village']
		z= request.POST['chiwog']
		u= request.POST['thramno']
		v= request.POST['houseno']
		c= request.POST['phone']

		print(x)

		
	
		UserData.objects.filter(user = request.user).update(
			Name = x,
			Village = y,
			Chiwog =z,
			ThramNo = u,
			HouseHoldNo = v,
			contact_number = c
		)
	
	return render(request, 'accounts/profile.html', 
	 {'profile': profile, 'marriage': marriage, 'child': child}
	)
	
	
# #####################################################
@login_required(login_url='login')
def update(request, user_id):
	# user = UserData.objects.get(pk=user_id)
	if request.method == 'POST':
		x= request.POST['name']
		y= request.POST['village']
		z= request.POST['chiwog']
		u= request.POST['thramno']
		v= request.POST['houseno']
		c= request.POST['phone']
	
		name = UserData.objects.filter(user = request.user)
		# .update(
		# 	Name = x,
		# 	Village = y,
		# 	Chiwog =z,
		# 	ThramNo = u,
		# 	HouseHoldNo = v,
		# 	contact_number = c
		# )
		print(name)

	
	return render(request, 'accounts/update.html', 
	 
	)



def navigation(request):
	profile = UserData.objects.filter(status=True)
	# for i in profile:
	# 	print(i.profile.url)
	return render(request, 'accounts/navbar1.html', {'profile': profile}
	)


@login_required(login_url='login')
def index(request):
	return render(request, 'accounts/index.html')

@login_required(login_url='login')
def passview(request):
	passview = Passdata.objects.all()
	return render(request, 'accounts/passview.html', {'passview': passview})

@login_required(login_url='login')
def Childdata(request):
	marriage = Marriage.objects.filter(status = True)
	if request.method == 'POST':
		childname = request.POST.get('childname')
		DOB = request.POST.get('DOB')
		gender = request.POST.get('gender')
		parent = request.POST.get('parent')
		birth = request.FILES['certificate']

		for i in marriage:
			print('marriage', i.MarriageId)
			print('parent', parent)
			if str(i.MarriageId) == str(parent):

				data1 = childdata(
						user = request.user,
						childname = childname,
						DOB = DOB,
						Gender = gender,
						parentsid = i.MarriageId,
						birth_certificate = birth
				)
				data1.save()

				

				email1 = EmailMessage(
						"Gewog Management System",
						"Hello " + str(data1.user) + " you have successfully posted the data of your child into our system. Please wait for few hours, we have to process your request. THANK YOU",
						settings.EMAIL_HOST_USER,
						[request.user.email],)
				email1.fail_silently = False
				email1.send()
				
				
				messages.success(request, 'You have successfully added child data')
				return redirect('index')

			else:
				messages.error(request, 'Your Marriage id was not in the database')
				

	return render(request, 'accounts/childdata.html')

@login_required(login_url='login')
def passdata(request):
	if request.method == 'POST':
		review_user = request.user
		reason = request.POST.get('option')
		em = Passdata( 
		user = review_user,
		reason = reason
		)
		email1 = EmailMessage(
            "Gewog Management System",
            "Hello " + str(em.user) + " you have successfully request your pass with our system. Please wait for few hours, we have to process your request. THANK YOU",
            settings.EMAIL_HOST_USER,
            [review_user.email],)
		email1.fail_silently = False
		email1.send()
		em.save()

		messages.success(request, 'You have successfully request for the pass')
	
	

		return redirect('index')


	return render(request, 'accounts/pass.html')

def exploremore(request):
	return render(request, 'accounts/exploremore1.html')

def timeshow(request):
	return render(request, 'accounts/time.html')


def main(request):
	return render(request, 'accounts/main.html')



# #####################################################
@login_required(login_url='login')
def annouce(request):
	annouce = Annoucement.objects.all()
	for i in annouce:
		print(i.image.url)
	return render(request, 'accounts/Annoucement.html', {'annouce': annouce})

	

# #####################################################
@login_required(login_url='login')
def explore(request):
	return render(request, 'accounts/exploremore.html')

# @login_required(login_url='login')
# def marriage(request):
# 	return render(request, 'accounts/marriage.html')

################################################################################################





##############################################################################################
@login_required(login_url='login')
def marriage(request):
	marriages = Marriage.objects.filter(status=True)
	userdata = UserData.objects.filter(status=True)

	# for x in userdata:
	# 	for i in marriages:
	# 		if i.user == request.user:
	# 			print("user "+ str(request.user))
	# 			print("dfhdfbbjsdhfvdhs")

				

	# 			if i.Spousecid in userdata:
	# 				print("spouse " + str(i.Spousecid))

	# 				# print("me " + str(userdata.CID))
	# 			# elif i.user in userdata:
	# 			# 	print('elif', i.user)
	# 			# 	# print('elif', x.CID)
	# 		if i.user == x.user :
	# 			print("jjjjjjjjjsjhdjhs")


	review_query = Marriage.objects.filter(user=request.user)
	if review_query.exists():
		messages.error(request, 'You have already added data')

	review_query = UserData.objects.filter(status=True)
	if review_query.exists() == False:
		messages.error(request, 'Your Data is not approved yet.')	

	
	
	if request.method == 'POST':
		review_user = request.user
		mid = request.POST.get('MarriageId')
		scid = request.POST.get('Spousecid')
		ucid = request.user.username
		marriagecert = request.FILES['MarriageCertificate']

		print(scid)
		
		
		for i in userdata:
			print('ur cid from i', i.CID)
			print('ur cid', ucid)
			print('spouce cid ', scid)

			if (str(i.CID) == str(scid) and scid != ucid):
				em = Marriage(
				MarriageId= mid, 
				user = review_user, 
				Spousecid = UserData.objects.get(CID = scid),
				your_cid = request.user.username,
				MarriageCertificate = marriagecert
				)
				em.save()

				email1 = EmailMessage(
				"Gewog Management System",
				"Hello "+ str(em.user) + "you have successfully added Your Marriage  Data in our system. Please wait for few hours, we have to process your details. THANK YOU",
				settings.EMAIL_HOST_USER,
				[review_user.email],)
				email1.fail_silently = False
				email1.send()

				
				messages.info(request, 'You have successfully added your marriage data')
				return redirect('index')


			elif (scid == ucid):
				print(scid)
				print(ucid)
				messages.error(request, 'You cannot have same CID as your spouse')
				break
			# else:
			# 	print(scid)
			# 	print(ucid)
			# 	messages.error(request, 'your the given cid of the spouse was invalid')
			
			
				

		# print(UserData.objects.all())
		

	return render(request, 'accounts/marriage.html', {'userdata': userdata,'marriages': marriages})
########################################################################################################
def userProfile(request, pk):
	profile = UserData.objects.get(CID = pk)
	return render(request, 'accounts/userprofile.html', {'profile': profile})

###########################################################################################################
# #####################################################
@login_required(login_url='login')
def search(request, pk):
	if request.method == 'POST':
		search = request.POST.get('search')
		venue = UserData.objects.filter(Name__contains = search, status=True)
		# child = childdata.objects.filter(Name_contains = search)
		return render(request, 'accounts/search.html', {'search': search, 'venue': venue})

	return render(request, 'accounts/search.html', {})

def searchdetail(request, pk):
	userdata = UserData.objects.filter(status=True, id=pk)
	return render(request, 'accounts/search_detail.html', {'userdata': userdata})


def footer(request):
	return render(request, 'accounts/footer1.html')

	


#completed
@login_required(login_url='login')
def personal(request):
	# today.strftime("%Y")
	
	review_query = UserData.objects.filter(user=request.user)
	if review_query.exists():
		messages.error(request, 'You have already added data')

	elif request.method == 'POST':
		review_user = request.user
		
		# review_query = User.objects.filter(user=review_user)
		# if review_query.exists():
        #     raise ValidationError("You have already reviewed")
		Name = request.POST.get('Name')
		DOB = request.POST.get('DOB')
		Cid = request.user.username
		Chiwog = request.POST.get('Chiwog')
		Village = request.POST.get('Village')
		HouseHoldNo = request.POST.get('HouseholdNumber')
		ThramNo = request.POST.get('ThramNumber')
		upload = request.FILES['ProfilePhoto']
		phone = request.POST.get('phone')
		marriage = request.POST.get('marriage')
		gender = request.POST.get('gender')

		# print(date.today().strftime("%Y"))
		now = int(date.today().strftime("%Y"))
		# date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
		# dob = datetime.strftime(DOB, '%Y-%m-%d').date()
		dob = DOB[0:4]
		print(DOB)
		print(type(DOB))

		print(dob)
		dob = int(dob)
		print(type(dob))
		print(now)
		if (now - dob >= 18):
			em = UserData( Name=Name, DOB=DOB,
			user = review_user,
				CID=Cid,Chiwog=Chiwog,
				Village=Village, 
				HouseHoldNo= HouseHoldNo, 
				gender=gender,
				ThramNo= ThramNo, 
				profile= upload, 
				contact_number= phone, 
			email = review_user.email)
			em.save()

		


			email1 = EmailMessage(
					"Gewog Management System",
					"Hello " + em.Name + " you have successfully added Your Data in our system. Please wait for few hours, we have to process your details. THANK YOU",
					settings.EMAIL_HOST_USER,
					[em.email],)
			email1.fail_silently = False
			email1.send()
			

			if(marriage == 'Yes'):
				messages.success(request, 'You have successfully added data')
				return redirect('marriage')
			else:
				messages.success(request, 'You have successfully added data')
				return redirect('index')

		else:
			messages.error(request, 'Your are not eligible to register, you have to be atleast 18 years old')
			

	return render(request, 'accounts/personalinfo.html')




def home(request):
	return render(request, 'accounts/dashboard.html', context)

def delete(request):
	return render(request, 'accounts/message.html')





@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)
