from mimetypes import init
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from random import randint

from . import util

markdowner = Markdown()

class PageForm(forms.Form):

    def __init__(self, v_title, v_content, *args,**kwargs):
        super().__init__(*args, **kwargs)
       
        if (v_title != ""):
            self.fields['title'] = forms.CharField(label="Title", initial=v_title, widget = forms.TextInput(attrs={'readonly':'readonly'}));
        else:
            self.fields['title'] = forms.CharField(label="Title", initial=v_title);

        self.fields['content'] = forms.CharField(label="Content", initial=v_content,
        required=True,   
        widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "type": "index"
    })

# Wiki page
def getwiki(request, page):
    entry = util.get_entry(page.capitalize());
    if entry != None :
        entry = markdowner.convert(entry)

    return render(request, "encyclopedia/wiki.html", {
        "entry": entry, "title": page.capitalize()
    })

# New Page
def newpage(request):
    if request.method == "POST":        
        form = PageForm("", "", request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #verify exists entry
            entry = util.get_entry(title)
            #if exists entry, then redirect
            if (entry == None) :
                # not exists
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:getwiki", args=[title]))
            else:
                # exists
                return render(request, "encyclopedia/newpage.html", {"form": form, 'alert_flag': True}) 

        else :
           return render(request, "encyclopedia/newpage.html", { "form": form}) 

    return render(request, "encyclopedia/newpage.html", { "form": PageForm("", "")})    

# New Page
def editpage(request, page):
    entry = util.get_entry(page.capitalize());

    if request.method == "POST":        
        form = PageForm(page, entry, request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #verify exists entry
            entry = util.get_entry(title)
            #if exists entry, then redirect
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:getwiki", args=[title]))
        else :
           return render(request, "encyclopedia/editpage.html", { "form": form}) 

    return render(request, "encyclopedia/editpage.html", { "form": PageForm(page, entry), "title" : page})   

# Random Page
def random(request):
    entries = util.list_entries()
    size = len(entries)    
    idx = randint(1, size-1)
    return HttpResponseRedirect(reverse("wiki:getwiki", args=[entries[idx]]))

#Search Page
def search(request):    
    if request.method == 'POST':
        #get param
        query = request.POST["q"].capitalize()
        #verify exists entry
        entry = util.get_entry(query)
        #if exists entry, then redirect
        if (entry != None) :
            return HttpResponseRedirect(reverse("wiki:getwiki", args=[query]))
        else :
            #not found, then search subquery
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries_search(query)
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "type": "search"
    })




