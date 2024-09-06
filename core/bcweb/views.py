from django.shortcuts import render
from django.db.models import Count
from .models import User, Certificate, Company

def mainpage(request):
    # Kullanıcıları sertifika sayısına göre sıralayıp en çok sertifikaya sahip 5 kişiyi getiriyoruz
    top_users = User.objects.annotate(cert_count=Count('certificates')).order_by('-cert_count')[:5]
    popular_companies = Company.objects.annotate(cert_count=Count('certificates')).order_by('-cert_count')[:6]
    users = User.objects.all()
    users = User.objects.all()
    certificates = Certificate.objects.all()
    companies = Company.objects.all()

    context = {
        'users': users,
        'certificates': certificates,
        'companies': companies,
        'top_users': top_users,
        'popular_companies': popular_companies,
    }
    return render(request, 'mainpage/index.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CertificateUploadForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = CertificateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the new user
            user = User.objects.create(
                name=form.cleaned_data['first_name'],
                surname=form.cleaned_data['last_name'],
                birthday=form.cleaned_data['birthday'],
                e_mail=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
            )
            # Save the certificate and associate with the new user
            certificate = form.save(commit=False)
            certificate.user = user
            certificate.save()

            messages.success(request, 'Certificate uploaded successfully, and user created!')
            return redirect('mainpage')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CertificateUploadForm()

    return render(request, 'registerpage/register.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Certificate

def verify_certificate(request):
    uuid = request.GET.get('uuid')
    certificate = None
    result = None
    
    if uuid:
        try:
            certificate = get_object_or_404(Certificate, id=uuid)
            result = "Approved" if certificate.approved else "Not Approved"
        except:
            result = "Certificate not found."
    
    return render(request, 'searchcertificate/certificate_result.html', {
        'result': result,
        'uuid': uuid,
    })

def search_certificate(request):
    return render(request, 'searchcertificate/search_certificate.html')