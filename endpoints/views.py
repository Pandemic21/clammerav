import datetime
import uuid
import tarfile
import os
from secrets import token_hex

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.backends import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, FileResponse
from django.urls import reverse, reverse_lazy

from endpoints.models import Asset, RawLog, Task, Ingest
from endpoints.forms import FormAssetSendRawLog


def index(request):
    context = {}
    '''
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_chainsaw': num_chainsaw,
        'num_visits': num_visits,
    }
    '''

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# allow assets to POST new logs to the server
def AssetSendRawLog(request, pk):
    asset_instance = get_object_or_404(Asset, pk=pk)

    # if the logged in user is trying to send logs to a different UUID, send 403
    if not str(asset_instance.asset_id) == request.user.username:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = FormAssetSendRawLog(request.POST)

    # if the client isn't using the POST method, return 405 (only POST allowed)
    else:
        return HttpResponseNotAllowed(['POST'])

    # get data from the form
    log = RawLog(asset_id=asset_instance, log_data=form.data['log_data'])
    log.save()

    return render(request, 'index.html')



### Asset Views ###
class AssetListView(generic.ListView):
    model = Asset
    paginate_by = 10

class AssetDetailView(generic.DetailView):
    model = Asset


### Log Views ###
class RawLogListView(generic.ListView):
    model = RawLog
    paginate_by = 10

class RawLogDetailView(generic.DetailView):
    model = RawLog


### Ingest Views ###
class IngestListView(generic.ListView):
    model = Ingest
    paginate_by = 10

class IngestDetailView(generic.DetailView):
    model = Ingest

class IngestCreate(UserPassesTestMixin,generic.CreateView):
    # this verifies the user has the permissions to perform create an author
    def test_func(self):
        return True

        # TODO: lock this function down to admins only
        #if 'catalog.can_mark_returned' in self.request.user.get_all_permissions():
        #    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    model = Ingest
    fields = '__all__'

class IngestDelete(DeleteView):
    model = Ingest
    success_url = reverse_lazy('ingest')

class IngestAgent(View):
    def get(self, request, *args, **kwargs):
        tar_dir = "./endpoints/agent/"
        tar_name = "agent.tar.gz"

        # generate .tar.gz file
        files = os.listdir(tar_dir)
        tar = tarfile.open(tar_dir + tar_name, "w:gz")
        for file in files:
            tar.add(tar_dir + file)
        tar.close()

        # send the tar file as a response
        response = FileResponse(open(tar_dir + tar_name, 'rb'))
        return response

def IngestJoin(request, pk):
    ingest_instance = get_object_or_404(Ingest, pk=pk)

    # if the ingest isn't active anymore, return 403
    if not ingest_instance.active:
        return HttpResponseForbidden()

    # if GET, provide the bash install script
    # the asset should POST after the install from GET is complete
    if request.method == 'GET':
        # if the create_user header is set
        # this happens in the clammer_agent.py script in the first initalization
        if 'HTTP_CREATE_USER' in request.META:
            new_asset = Asset()
            new_asset.save()

            # create user
            new_user = str(new_asset.asset_id)
            new_pass = str(token_hex())
            print("New user: " + new_user)
            print("New pass: " + new_pass)
            user_obj = User.objects.create_user(username=new_user, password=new_pass)
            user_obj.save()

            # give the agent the info to create its clammer.conf file
            response = {
                'username': new_user,
                'password': new_pass,
                'existing_clamav': ingest_instance.existing_clamav,
                'login_url': ingest_instance.login_url,
                'logout_url': ingest_instance.logout_url,
                'rawlog_url': ingest_instance.rawlog_url,
                'log_files': ingest_instance.log_files,
                'config_files': ingest_instance.config_files,
                'home': ingest_instance.home,
                'log_level': ingest_instance.log_level
            }
            return JsonResponse(response)

        # else it's just a normal GET request.
        # serve the install.sh file
        else:
            print("Getting...")
            # curl method
            context = {
                'ingest_agent_url': 'http://127.0.0.1:8000/endpoints/ingest/' + str(pk) + '/agent.tar.gz',
                'ingest_join_url': 'http://127.0.0.1:8000/endpoints/ingest/' + str(pk) + '/join/',
            }

            # Render the HTML template index.html with the data in the context variable
            return render(request, 'ingest_join.html', context=context)

    # if POST, create asset instance
    elif request.method == 'POST':
        # TODO: make this section include adding stuff to the asset, like hostname and IPs
        return render(request, 'index.html')


    # only GET and POST allowed, otherwise return 405
    else:
        print("Else, method: " + request.method)
        return HttpResponseNotAllowed(['GET', 'POST'])

    # TODO: create the asset and do other stuff here

    return render(request, 'index.html')
