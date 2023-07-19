from django.shortcuts import render, redirect
from . import urls
from .models import Topic
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """The home page for learning log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics."""
    topics=Topic.objects.order_by('date_added')
    context={'topics':topics}
    return render(request, 'learning_logs/topics.html',context)

def topic(request,topic_id):
    """Show a single topic and all its entries"""
    topic=Topic.objects.get(id=topic_id)
    entries=topic.entry_set.order_by('date_added')
    context={'topic':topic,'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Let a user add a new topic"""
    if request.method != 'POST':
        #no data submitted; create a blank form
        form= TopicForm()
    else:
        #POST data submitted, process data
        form=TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    #Display a blank or invalid form
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

def new_entry(request, topic_id):
    """"Let a user add a new entry"""
    topic=Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)
    context={'topic':topic,'form':form}
    return render(request, 'learning_logs/new_entry.html',context)
