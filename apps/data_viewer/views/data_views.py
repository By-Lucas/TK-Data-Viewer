import os
import json
import pandas as pd

from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


def import_csv_xlsx(request):
    original_filename = ''
    table_data = None
    page_obj = None
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
        
        columns = df.columns.tolist()
        
        # Criar o objeto Paginator e obter a página atual
        paginator = Paginator(df.to_dict(orient='records'), 15)  # Exibir 15 linhas por página
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        # Converter as linhas da página atual em uma lista de dicionários
        table_data = [row for row in page_obj]
        
        # Armazene os dados da tabela e colunas na sessão
        request.session['table_data'] = table_data
        request.session['columns'] = columns
    
    context = {
        'original_filename': original_filename,
        'table_data': table_data,
        'columns': columns,
        'page_obj':page_obj
    }
    return render(request, 'data_viewer/csv_xlsx_upload_display.html', context)


def ajax_data_pagination(request):
    original_filename = ''
    page_obj = None

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = request.GET.get('page')

        # Recupere os dados da tabela e colunas da sessão
        table_data = request.session.get('table_data', [])
        columns = request.session.get('columns', [])

        df = pd.DataFrame(table_data, columns=columns)

        # Criar o objeto Paginator e obter a página atual
        paginator = Paginator(df.to_dict(orient='records'), 10)  # Exibir 10 linhas por página
        page_obj = paginator.get_page(page)

        # Converter as linhas da página atual em uma lista de dicionários
        table_data = [row for row in page_obj]

        context = {
            'table_data': table_data,
            'columns': columns,
            'page_obj': page_obj
        }

        html = render_to_string('data_viewer/csv_xlsx_upload_display.html', context)

        return JsonResponse({'html': html})
    else:
        return HttpResponseRedirect(reverse('upload_data'))



def clean_dataframe(df, selected_columns):
    # Remover espaços em branco extras
    if not selected_columns:
        return df
    for col in selected_columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    # Padronizar formatos de dados (por exemplo, converter todos os dados de data para o mesmo formato)
    # Implemente aqui suas próprias regras de padronização de formatos de dados, se necessário
    return df


def remove_duplicates(request):
    if request.method == 'POST':
        # Recrie o DataFrame com os dados e colunas recebidos
        table_data = json.loads(request.POST.get('table_data'))
        columns = json.loads(request.POST.get('columns'))
        original_filename = request.POST.get('original_filename')
        df = pd.DataFrame(table_data, columns=columns)

        # # Verifica quais colunas devem ter duplicatas removidas
        # selected_columns = request.POST.getlist('selected_columns')

        remove_duplicates = request.POST.get('remove_duplicates') == 'on'
        replace_duplicates = request.POST.get('replace_duplicates') == 'on'
        remove_column = request.POST.get('remove_column') == 'on'
        clean_data = request.POST.get('clean_data')
        
        # Verifica quais colunas devem ter duplicatas removidas
        selected_columns = [column for column in columns if column in request.POST]
        
        if remove_column:
            df = df.drop(selected_columns, axis=1)
        if clean_data:
            df = clean_dataframe(df, selected_columns)
        elif replace_duplicates:
            for col in selected_columns:
                duplicates = df.duplicated(subset=col, keep='first')
                df.loc[duplicates, col] = ''
        elif remove_duplicates:
            if selected_columns:
                df = df.drop_duplicates(subset=selected_columns, keep='first')
            else:
                df = df.drop_duplicates(keep='first')

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
        clean_data = request.POST.get('clean_data') == 'true'
        
        # Adiciona o prefixo TK_ ao nome do arquivo
        new_filename = f"TK_{filename}"
        
        # Remover espaçoes em branco
        if clean_data:
            df = clean_dataframe(df)

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
    
