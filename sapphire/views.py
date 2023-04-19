from django.shortcuts import render, redirect
from sapphire.models import User, OTP, Website
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from .forms import CustomPasswordChangeForm, ScrapeForm, PDFScrapeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.contrib import messages
from scrapy_project.scrapyproject.scrapyproject.spiders.spider_runner import run_spider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_project.scrapyproject.scrapyproject.spiders.lawspider import MySpider
from scrapy_project.scrapyproject.scrapyproject.spiders.pdfspider import PDFSpider
from scrapy.utils.log import configure_logging
import os, difflib 

configure_logging()

runner = CrawlerRunner()



# Create your views here.

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # generate OTP
            otp = get_random_string(length=6, allowed_chars='0123456789')
            # save OTP to database
            OTP.objects.create(user=user, otp_code=otp)
            # send OTP to user's email
            subject = 'Your OTP for Sapphire Login'
        
            message = f'Hello {user.first_name},<br><br>Your login OTP is <b>{otp}</b>. Please do not share this with anyone.<br><br>Best Regards,<br><br><b>Sapphire Admin</b>'
            recipient_list = [user.email]
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, strip_tags(message), from_email, recipient_list, html_message=message, fail_silently=False)
            return redirect('otp')
        else:
            return render(request,'base/index.html', {'error': 'Invalid credentials'})
    return render(request, 'base/index.html')

@login_required
def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_otp = OTP.objects.filter(user=request.user, otp_code=otp).first()
        if user_otp:
            # delete OTP from database after successful login
            user_otp.delete()
            return redirect('home')
        else:
            return render(request,'base/otp.html', {'error': 'Invalid OTP!'})
    return render(request, 'base/otp.html')

@login_required
def home(request):
    # if request.user.first_login:
    #     # if user is logging in for the first time, show the modal
    #     request.user.first_login = False
    #     request.user.show_modal = False
    #     request.user.save()
        return render(request, 'base/home.html', {'show_modal': True})
    # else:
    #     return render(request, 'base/home.html')
    

def run_spider(url):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(MySpider, start_url=url)

    crawl()
    reactor.run()
    items = {}
    path = os.path.join(django_settings.STATICFILES_DIRS[0], 'files')
    for file_name in os.listdir(path):
        if file_name.endswith('.txt'):
            with open(os.path.join(path, file_name), 'r') as f:
                rule_name = file_name[:-4]  # remove the '.txt' extension
                data = f.read()
                items[rule_name] = data

    return items


def spider_runner_pdf(url):
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(PDFSpider, start_url=url)

    crawl()

def search(request):
    main_url_form = ScrapeForm(request.POST or None, prefix='main_url')
    pdf_url_form = PDFScrapeForm(request.POST or None, prefix='pdf_url')

    if request.method == 'POST':
        if main_url_form.is_valid():
            main_url = main_url_form.cleaned_data['main_url']
            if main_url:
                request.session['scraped_data_main'] = run_spider(main_url)
                messages.success(request, 'The crawl is successful.')
                print('The crawl successful.')
            else:
                messages.error(request, 'Please enter a URL for main page.')
                return redirect('search')
            
    if request.method == 'POST':
        if pdf_url_form.is_valid():
            pdf_url = pdf_url_form.cleaned_data['pdf_spider_url']
            if pdf_url:
                spider_runner_pdf(pdf_url)
                messages.success(request, 'PDF crawl successful.')
                print('PDF crawl successful.')
            else:
                messages.error(request, 'Please enter a URL for PDF.')
        return redirect('search')

    return render(request, 'base/searchtool.html', {
        'main_url_form': main_url_form,
        'pdf_url_form': pdf_url_form
    })



def comparing(request):
    file1 = None
    file2 = None
    diff = None
    mapping = None

    if request.method == 'POST':
        if 'file1' in request.FILES and 'file2' in request.FILES:
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']

            # Read the contents of the files with the Windows-1252 encoding
            file1_contents = file1.read().decode('Windows-1252')
            file2_contents = file2.read().decode('Windows-1252')

            file1_lines = file1_contents.split('\n')
            file2_lines = file2_contents.split('\n')

            # Generate the HTML diff
            diff = difflib.HtmlDiff(wrapcolumn=85).make_file(file1_lines, file2_lines)

            # Generate the unified diff
            unified_diff = difflib.unified_diff(file1_lines, file2_lines)

            # Generate the mapping of changes
            mapping = '<br>'.join([line.strip() for line in unified_diff])

        elif 'file1' in request.POST and 'file2' in request.POST:
            file1 = request.POST['file1']
            file2 = request.POST['file2']
            file1_lines = file1.split('\n')
            file2_lines = file2.split('\n')

            # Generate the HTML diff
            diff = difflib.HtmlDiff().make_file(file1_lines, file2_lines)

            # Generate the unified diff
            unified_diff = difflib.unified_diff(file1_lines, file2_lines)

            # Generate the mapping of changes
            mapping = '<br>'.join([line.strip() for line in unified_diff])

    return render(request, 'base/comparingtool.html', {'file1': file1, 'file2': file2, 'diff': diff, 'mapping': mapping})

# @login_required
def url(request):
    websites = Website.objects.all()
    return render(request, 'base/url.html', {'websites': websites})

@login_required
def signout(request):
    logout(request)
    return redirect('index')


@login_required
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    loggedUser = request.user

    # Handle password change form submission
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=loggedUser, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userProfile', pk=pk)
    else:
        form = CustomPasswordChangeForm(user=user)

    return render(request, 'base/profile.html', {'user': user, 'form': form})
    
