from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .forms import UsernameForm
from .models import SteamUser

def input_username(request):
	if request.method == "POST":
		form = UsernameForm(request.POST)
		if form.is_valid():
			steam_user = form.save(commit=False)
			steam_user.refresh()
			steam_user.save()
			return redirect('cheevo.views.user_games_list', pk=steam_user.pk)
	else:
		form = UsernameForm()
	return render(request, 'cheevo/input_username.html', {'form': form})
	
def user_games_list(request, pk):
	steam_user = get_object_or_404(SteamUser, pk=pk)
	return render(request, 'cheevo/user_games_list.html', {'steam_user': steam_user})