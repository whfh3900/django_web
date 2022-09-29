from django.forms import ModelForm
from .models import DataTable

class FileUploadForm(ModelForm):
    class Meta:
        model = DataTable
        fields = ['member_id', 'file_name', 'new_file_name', 'pro_dtime', 'data_len', 'pro_result', 'note',]