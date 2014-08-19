from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from ota.models import Rom
from ota.forms import RegistrationForm, RomForm


def index(request):
    return render_to_response(
        'index.html',
        RequestContext(request, {
            'roms': Rom.objects.all(),
            'no_rom_msg': "No ROMS",
        })
    )


def user(request, username):
    try:
        _user = User.objects.get(username=username)
    except:
        raise Http404('Can\'t find User : %s' % username)

    return render_to_response(
        'user.html',
        RequestContext(request, {
            'roms': _user.rom_set.all(),
            'username': username,
            'no_rom_msg': "No ROMS for %s" % username,
        })
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, label_suffix='')
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/')

    form = RegistrationForm(label_suffix='')
    return render_to_response(
        'registration/register.html',
        RequestContext(request, {
            'form': form,
        })
    )


def addrom(request):
    if request.method == 'POST':
        form = RomForm(request.POST, label_suffix='')
        if form.is_valid():
            try:
                user = User.objects.get(username=request.user.username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')

            create = False
            try:
                rom = Rom.objects.get(device=form.cleaned_data['device'],
                                      version=form.cleaned_data['version'])
            except ObjectDoesNotExist:
                create = True

            if not create:
                raise ValueError("device %s, version %d is already exist" %
                                 (form.cleaned_data['device'],
                                  form.cleaned_data['version']))

            rom = Rom.objects.create(
                device=form.cleaned_data['device'],
                name=form.cleaned_data['name'],
                ota_id=form.cleaned_data['ota_id'],
                download_url=form.cleaned_data['download_url'],
                md5sum=form.cleaned_data['md5sum'],
                version=form.cleaned_data['version'],
                date=form.cleaned_data['date'],
                change_log=form.cleaned_data['change_log'],
                user=user
            )
            rom.save()

            return HttpResponseRedirect('/')
    else:
        form = RomForm(label_suffix='')
        return render_to_response(
            'rom.html',
            RequestContext(request, {
                'form': form,
                'page_type': 'new',
            })
        )


def check_same(rom, form):
    if rom.device == form.cleaned_data['device'] and \
       rom.name == form.cleaned_data['name'] and \
       rom.ota_id == form.cleaned_data['ota_id'] and \
       rom.download_url == form.cleaned_data['download_url'] and \
       rom.md5sum == form.cleaned_data['md5sum'] and \
       rom.version == form.cleaned_data['version'] and \
       rom.date == form.cleaned_data['date'] and \
       rom.change_log == form.cleaned_data['change_log']:
        return True
    else:
        return False


def check_valid(form, myid):
    '''check form data:
        search : not myid, device, ota_id, version is same'''

    try:
        rom = Rom.objects.exclude(pk=myid).filter(
            device=form.cleaned_data['device'],
            ota_id=form.cleaned_data['ota_id'],
            version=form.cleaned_data['version']
        )
        rom_id = rom.id
        rom_id = rom_id
    except AttributeError:
        return True

    return False


def editrom(request, id):
    if request.method == 'POST':
        form = RomForm(request.POST, label_suffix='')
        if form.is_valid():
            try:
                User.objects.get(username=request.user.username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')

            create = False
            try:
                rom = Rom.objects.get(pk=id)
            except ObjectDoesNotExist:
                create = True

            if create:
                raise ValueError("device %s, version %d is not exist" %
                                 (form.cleaned_data['device'],
                                  form.cleaned_data['version']))

            if check_same(rom, form):
                return HttpResponseRedirect('/')

            if not check_valid(form, id):
                return HttpResponseRedirect('/')

            rom.device = form.cleaned_data['device']
            rom.name = form.cleaned_data['name']
            rom.ota_id = form.cleaned_data['ota_id']
            rom.download_url = form.cleaned_data['download_url']
            rom.md5sum = form.cleaned_data['md5sum']
            rom.version = form.cleaned_data['version']
            rom.date = form.cleaned_data['date']
            rom.change_log = form.cleaned_data['change_log']
            rom.save()

            return HttpResponseRedirect('/')
    else:
        rom = Rom.objects.get(pk=id)
        form = RomForm({
            'device': rom.device,
            'name': rom.name,
            'ota_id': rom.ota_id,
            'download_url': rom.download_url,
            'md5sum': rom.md5sum,
            'version': rom.version,
            'date': rom.date,
            'change_log': rom.change_log
        }, label_suffix='')
        return render_to_response(
            'rom.html',
            RequestContext(request, {
                'form': form,
                'page_type': 'edit',
            })
        )


def deleterom(request, id):
    try:
        rom = Rom.objects.get(pk=id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/')

    rom.delete()
    return HttpResponseRedirect('/')


def query_update(request, device, ota_id, version):
    roms = Rom.objects.filter(device=device,
                              ota_id=ota_id,
                              version__gt=version).order_by('version')
    rom = roms[0]
    try:
        rom_id = rom.id
        rom_id = rom_id
    except AttributeError:
        raise Http404('Can\'t find update for %s' % device)

    return render_to_response(
        'query_update.json',
        RequestContext(request, {
            'name': rom.name,
            'download_url': rom.download_url,
            'md5sum': rom.md5sum,
            'version': rom.version,
            'date': '%04d%02d%02d-%02d%02d' % (rom.date.year, rom.date.month, rom.date.day, rom.date.hour, rom.date.minute),
            'changelog': rom.change_log,
        })
    )
