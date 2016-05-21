from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from exporter.models import Topic, Question
import paramiko
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth import authenticate, login

# Create your views here.

template = loader.get_template('exporter/index.html')


def index(request):
    if request.method == 'POST':
        auth(request)
    else:
        return render(request,'exporter/index.html')



def auth(request):
    context = get_task_info_from_db()
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    full_name = getFullName(username=username, password=password)

    if full_name is not None:
        context['full_name'] = full_name[0]
        return render(request,"exporter/index.html", context)

    else:
        return render(request, "exporter/invalid_login.html")

def get_task_info_from_db():
    # topic_list = Topic.objects.all()
    topic_list = Topic.objects.all()[:3]
    question_list = []
    for i in range(3):
        question_list.append(topic_list[i].question_set.all())
    answer = Question.objects.get(pk=1).answer
    context = {
        'topic_list': topic_list,
        'question_list': question_list,
    }
    return context

def getFullName(username,password):
    cacert = '/home/aligator/PycharmProjects/static_cdn/carcet/ca_labs.wmi.amu.edu.pl.pem'
    host = 'students.wmi.amu.edu.pl'
    data = []
    try:
        file = open(cacert, 'r')
        file.close()
    except IOError:
        print ('no file detected', cacert)
    else:
        try:
            ssh = paramiko.SSHClient()
            #if os.path.exists(cacert):
            #ssh.load_host_keys(os.path.expanduser(cacert))
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password, key_filename=cacert)
            stdin, stdout, stderr = ssh.exec_command('getent passwd `whoami` | cut -d : -f 5')
            name=(stdout.readlines()[0][:-1])
            #do zrobienia: poczekac na wykonanie polecenia przed wczytaniem wyjscia
            ssh.close()
            data = [name, username]
            return data
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to %s" % host)
            return None

        #dodac wyjatek dla nieprawidlowego hosta
        except:
            print("Could not connect with SSH to %s" % host)
