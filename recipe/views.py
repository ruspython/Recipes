from django.shortcuts import render, HttpResponse, render_to_response, Http404, redirect, RequestContext, \
    get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from recipe.models import Recipe, Tag
from recipe.forms import RecipeForm
from random import randint
import datetime
from django.contrib.syndication.views import Feed


def get_random_recipe(recipes):
    return recipes[randint(0, len(recipes) - 1)]


def home(request, page_number=1):
    args = {}
    recipes = Recipe.objects.all()
    cur_page = Paginator(recipes, 7)
    if auth.get_user(request).is_authenticated():
        args['user'] = auth.get_user(request)
    args['recipes'] = cur_page.page(page_number)
    args['user'] = auth.get_user(request)
    return render_to_response('home.html', args)


def searchbytag(request, tag_name, page_number=1):
    args = {}
    recipes = [recipe for recipe in Recipe.objects.all() for tag in recipe.tags.all() if tag_name == tag.name]
    cur_page = Paginator(recipes, 7)
    args['recipes'] = cur_page.page(page_number)
    if auth.get_user(request).is_authenticated():
        args['user'] = auth.get_user(request)
    args['tag_name'] = tag_name
    return render_to_response('home.html', args)


def recipe(request, recipe_id):
    user = auth.get_user(request)
    args = {}
    username = ''
    if auth.get_user(request).is_authenticated():
        args['user'] = auth.get_user(request)
        username = args['user'].username
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        if user.is_superuser or recipe.author.username == username:
            args['wrong_author'] = False
        else:
            args['wrong_author'] = True
        args['recipe'] = recipe
        args['tags'] = recipe.tags.all()
    except ObjectDoesNotExist as e:
        raise Http404

    return render_to_response('recipe.html', args)


def addrecipe(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RecipeForm()
    if auth.get_user(request).is_authenticated():
        args['user'] = auth.get_user(request)
        if request.POST:
            form = RecipeForm(request.POST)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.author = args['user']
                form.save()
                return redirect('/recipes/' + str(recipe.id))
            args['form'] = form
    else:
        return redirect('/auth/login/')
    return render_to_response('addrecipe.html', args, context_instance=RequestContext(request))


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    args = {}
    args['recipe'] = recipe
    args['form'] = form = RecipeForm(request.POST or None, instance=recipe)
    args['user'] = auth.get_user(request)
    user = auth.get_user(request)
    if not user.is_superuser:
        print(recipe.author, user.username)
        if recipe.author != user:
            return redirect('/recipes/' + str(recipe.id))
    if form.is_valid():
        # form = RecipeForm(request.POST)
        recipe = form.save(commit=False)

        recipe.timestamp = now()

        recipe.save()
        form.save_m2m()
        print('saving')

        return redirect('/recipes/' + str(recipe.id))
    print('just enter')
    return render_to_response('editrecipe.html', args, context_instance=RequestContext(request))


def getdate(request):
    tags = Tag.objects.all()
    random_tag = tags[randint(0, len(tags)-1)]
    return render_to_response("date.html", {'getdate': datetime.datetime.now(), 'random_tag': random_tag.name});

class RecipeFeed(Feed):
    title = 'RSS feed - recipes'
    link = '/feeds/recipes/'
    description = 'RSS feed recipes'

    def items(self):
        return Recipe.objects.order_by('-timestamp')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text


def search(request):
    args = {}
    args['user'] = auth.get_user(request)
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if query:
        results = Recipe.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    else:
        results = None

    pages = Paginator(results, 5)
    try:
        returned_page = pages.page(page)
    except EmptyPage:
        returned_page = pages.page(pages.num_pages)
    args['page_obj'] = returned_page
    args['object_list'] = returned_page.object_list
    args['search'] = query

    return render_to_response('search.html', args)