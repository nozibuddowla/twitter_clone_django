from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
import logging

# Create your views here.
logger = logging.getLogger(__name__)

def index(request):
    tweets = Tweet.objects.all().order_by('-created_at')

    search_query = request.GET.get('search', '').strip()
    logger.debug(f"Searched for: {search_query}")
    if search_query:
        tweets = tweets.filter(text__icontains=search_query)
        logger.debug(f"Number of tweets found: {tweets.count()}")

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = TweetForm(request.POST, request.FILES)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('index')
        else:
            return redirect('login')
    else:
        form = TweetForm()
    
    return render(request, 'index.html', {'tweets': tweets, 'form': form})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('index')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, 'tweet_detail.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})