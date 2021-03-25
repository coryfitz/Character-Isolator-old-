from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse
from django.http import Http404
def index(request):
    success = 0
    if success == 1:
        success = 2
    if request.POST and request.FILES:
        txtfile = request.FILES['txt_file']
        def char_isolate():

            ur_text = txtfile.read().decode("utf-8")

            #finding unique
            unique = []
            for char in ur_text:
                if char not in unique:
                    unique.append(char)
            unique = str(unique)

            #cleaning
            import string
            nopunct_unique = unique.translate(str.maketrans('', '', string.punctuation))
            nodigit_unique = nopunct_unique.translate(str.maketrans('', '', string.digits))
            clean_unique = nodigit_unique.translate(str.maketrans('', '', string.ascii_letters))

            #finding unique
            really_unique = []
            for char in clean_unique:
                if char not in really_unique:
                    really_unique.append(char)
            really_unique = str(really_unique)

            #cleaning 2
            clean_reallyunique = really_unique.translate(str.maketrans('', '', string.punctuation))

            #remove Chinese punctuation
            final_text = clean_reallyunique.translate({ord(c): None for c in '。；：！？，、'})

            #remove spaces
            final_text4real = final_text.translate({ord(c): None for c in string.whitespace})

            #write to file
            f= open("text.txt","w+")
            for char in final_text4real:
                f.write('\n'+char)
            f.close()

            #write to file
            tmp_path = os.path.join(settings.MEDIA_ROOT, 'tmp/text.txt')
            with open(tmp_path, 'w') as f:
                item = iter(final_text4real)
                for _ in range(len(final_text4real)-1):
                    f.write('%s\n' % next(item))
                f.seek(0)
                f.write('%s' % next(item))
            f.close()
        char_isolate()
        success = 1
    context = {}
    return render(request, "converter/index.html", locals())

def download(request):
    path = "tmp/text.txt"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
            except Exception:
                raise Http404
