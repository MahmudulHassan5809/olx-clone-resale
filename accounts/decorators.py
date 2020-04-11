from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib import messages


def active_user_required():
	def decorator(view_func):
		def wrap(request, *args, **kwargs):
			username = request.POST.get('username')
			password = request.POST.get('password')
			if username != '' and password != '':
				user = authenticate(request, username=username, password=password)
				if user is not None and  user.user_profile.active:
					return view_func(request, *args, **kwargs)
				else:
					messages.error(request, ('Please Login Or May Be Your Account Is Not Active'))
					return redirect('accounts:login')
			else:
				messages.error(request, ('Please Input All The Fields'))
				return redirect('accounts:login')
		return wrap
	return decorator