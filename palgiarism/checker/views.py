from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from pathlib2 import Path
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Create your views here.
def Check(request):
   if request.method=='POST':
    f1=request.FILES['File1'].read().decode('utf-8')
    f2=request.FILES['File2'].read().decode('utf-8')
    # fs=FileSystemStorage()
    # filepathname=fs.save(f1.name,f1)
    # filepathname=fs.url(filepathname)
    # file='.'+filepathname
    # contents = f1.read_text()
    print('file contents read')
    tokens_o=word_tokenize(f1)
    tokens_p=word_tokenize(f2)
    tokens_o = [token.lower() for token in tokens_o]
    tokens_p = [token.lower() for token in tokens_p]
    stop_words=set(stopwords.words('english'))
    punctuations=['"','.','(',')',',','?',';',':',"''",'``']
    filtered_tokens_o = [w for w in tokens_o if not w in stop_words and not w in punctuations]
    filtered_tokens_p = [w for w in tokens_p if not w in stop_words and not w in punctuations]
    #Trigram Similiarity measures
    trigrams_o=[]
    for i in range(len(tokens_o)-2):
        t=(tokens_o[i],tokens_o[i+1],tokens_o[i+2])
        trigrams_o.append(t)

    s=0
    trigrams_p=[]
    for i in range(len(tokens_p)-2):
        t=(tokens_p[i],tokens_p[i+1],tokens_p[i+2])
        trigrams_p.append(t)
        if t in trigrams_o:
            s+=1

    #jaccord coefficient = (S(o)^S(p))/(S(o) U S(p))
    J=s/(len(trigrams_o)+len(trigrams_p)) 
    print('jaccard coefficient is',J)
    if J>0:
       q='Palgiarism Detected'
    else:
       q='No Palgiarism Detected'

    #containment measure
    C=s/len(trigrams_p)
    print(C)


    return render(request,'check.html',{'file1content':f1,'file2content':f2,'q':q})
   else:
     return render(request,'check.html')