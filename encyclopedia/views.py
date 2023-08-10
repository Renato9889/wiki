from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.contrib import messages
import markdown
import random
from . import util

def index(request):
    ordem_list = sorted(util.list_entries())
    return render(request, "encyclopedia/index.html", {
        "entries": ordem_list
    })


def search(request, title=""):
    title = title
    if not title:
        return redirect('index')
    
    entries = util.list_entries()

    title2 = title[0].upper() + title[1:]

    search_title = title2 in entries
    
    if not search_title:
        return redirect("search_substring", title=title)

    
    result_search = markdown.markdown(util.get_entry(title))
    result_search = mark_safe(result_search)
    
    return render(request, 'encyclopedia/search.html', {
                "entry": result_search,
                "title": title,
        })

def search_title(request, title):
    title =  request.GET.get('title',"")
    if not title:
        return redirect('index')
    return redirect('search', title = title)
    
def search_substring(request, title=""):
    substring = title
    list_entries = util.list_entries()
    substring_lower = substring.lower()
    list_entries = list(filter(lambda x: substring_lower in x.lower(), list_entries))
    if not list_entries:
        return redirect(not_found)
    ordem_list = sorted(list_entries)
    return render(request, 'encyclopedia/search_substring.html', {
                "title": substring,
                'entries': ordem_list
        })


def not_found(request):
     title = "Not Found!"
     text = "Sorry, not found !!!"
     return render(request, 'encyclopedia/not_found.html', {
                "entry": text,
                "title": title,
        })

def create_newpage(request):
    list_title = util.list_entries()
    title = request.POST.get('title',"")
    text = request.POST.get('text',"")
    result = title in list_title
    if request.method == 'POST' and text != "" and result == False and title != "":
        title = title[0].upper() + title[1:]
        util.save_entry(title,text)
        return redirect('search', title=title)
    else:
        if result == True:
            error = "Error, invalid title!"
            return render(request, 'encyclopedia/create_newpage.html', {'error_input': error})
        else:
            if 'submit' in request.POST and (text == "" or title == ""):
                error = "Error, one of the entries is empty!"
                return render(request, 'encyclopedia/create_newpage.html', {'error_input': error})
  
    return render(request,'encyclopedia/create_newpage.html')


def search_random(request):
    title = random.choice(util.list_entries())
    return redirect('search', title = title)

def edit_page(request):
   if 'save' in request.POST:
        title = request.POST.get('title',"")
        text = request.POST.get('text',"")
        util.save_entry(title,text)
        return redirect('search', title=title)
   else:
       title = request.POST.get('title', '')
       result_search = util.get_entry(title)
       return render(request, 'encyclopedia/edit_page.html', {
                        "title_editvalue": title,
                        "text_editvalue": result_search,
                        }) 
