import os
import json
import pandas as pd

from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def import_csv_xlsx(request):
    original_filename = ''
    table_data = None
    columns = None

    if request.method == 'POST':
        file = request.FILES['file']
        file_ext = str(file).split('.')[-1]
        original_filename = file.name

        if file_ext == 'csv':
            df = pd.read_csv(file)
        elif file_ext == 'xlsx':
            df = pd.read_excel(file, engine='openpyxl')
        else:
            return HttpResponse("Formato de arquivo não suportado. Por favor, use .csv ou .xlsx")
        
        table_data = df.to_dict(orient="records")
        columns = df.columns.tolist()

        
    context = {
        'original_filename': original_filename,
        'table_data': table_data,
        'columns': columns,
    }
    return render(request, 'data_viewer/csv_xlsx_upload_display.html', context)


def remove_duplicates(request):
    if request.method == 'POST':
        # Recrie o DataFrame com os dados e colunas recebidos
        table_data = json.loads(request.POST.get('table_data'))
        columns = json.loads(request.POST.get('columns'))
        original_filename = request.POST.get('original_filename')
        df = pd.DataFrame(table_data, columns=columns)

        # Verifica quais colunas devem ter duplicatas removidas
        selected_columns = request.POST.getlist('selected_columns')

        remove_duplicates = request.POST.get('remove_duplicates') == 'on'
        replace_duplicates = request.POST.get('replace_duplicates') == 'on'
        remove_column = request.POST.get('remove_column') == 'on'

        if remove_column:
            df = df.drop(selected_columns, axis=1)
        elif replace_duplicates:
            for col in selected_columns:
                duplicates = df.duplicated(subset=col, keep='first')
                df.loc[duplicates, col] = ''
        elif remove_duplicates:
            df = df.drop_duplicates(subset=selected_columns, keep='first')

        # Converte o DataFrame atualizado em um formato adequado para o template
        table_data = df.to_dict(orient="records")

        context = {
            'table_data': table_data,
            'columns': df.columns.tolist(),
            'original_filename': original_filename,
        }

        return render(request, 'data_viewer/csv_xlsx_upload_display.html', context)
    else:
        return HttpResponseRedirect(reverse('upload_data'))


def save_changes(request):
    if request.method == 'POST':
        # Recrie o DataFrame com os dados e colunas recebidos
        table_data = json.loads(request.POST.get('table_data'))
        columns = json.loads(request.POST.get('columns'))
        filename = request.POST.get('filename')  # Use o nome do arquivo fornecido pelo usuário
        file_type = request.POST.get('file_type')  # Use o tipo de arquivo selecionado pelo usuário
        
        # Adiciona o prefixo TK_ ao nome do arquivo
        new_filename = f"TK_{filename}"
        
        # Crie um novo DataFrame com os dados e colunas recebidos
        df = pd.DataFrame(table_data, columns=columns)
        
        # Salve o DataFrame modificado em um novo arquivo
        if file_type == 'csv':
            new_filename += '.csv'
            df.to_csv(new_filename, index=False)
        elif file_type == 'xlsx':
            new_filename += '.xlsx'
            df.to_excel(new_filename, index=False)
        else:
            return HttpResponse("Formato de arquivo não suportado. Por favor, use .csv ou .xlsx")
        
        # Envia o arquivo como resposta
        with open(new_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{new_filename}"'
            return response
    else:
        return HttpResponseRedirect(reverse('upload_data'))
