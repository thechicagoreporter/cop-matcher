import csv

def dump(qs, outfile_path):
    """
    Takes in a Django queryset and spits out a CSV file.
    
    Usage::
        >> from utils import dump2csv
        >> from dummy_app.models import *
        >> qs = DummyModel.objects.all()
        >> dump2csv.dump(qs, './data/dump.csv')
    
    Based on snippets by zbyte64, palewire:
        http://www.djangosnippets.org/snippets/790/
        http://palewi.re/posts/2009/03/03/django-recipe-dump-your-queryset-out-as-a-csv-file/
    
    Added dictwriter, serialization call to support foreign key IDs
    """
    model   = qs.model
    headers = [x.name for x in model._meta.fields] 
    outfile = open(outfile_path,'w')
    writer  = csv.DictWriter(outfile,headers)
    writer.writeheader()
    
    for obj in qs:
        row = {}
        for header in headers:
            val = obj.serializable_value(header)
            if callable(val):
                val = val()
            if type(val) == unicode:
                val = val.encode("utf-8")
            row[header] = val
        writer.writerow(row)
    
    outfile.close()
