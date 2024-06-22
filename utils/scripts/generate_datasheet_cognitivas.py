# generate a csv table with pandas
import pandas as pd

def generate_xlsx(disciplinas_info, competencias_info):
    data ={}
    # Define the data for the table
    # pd.set_option('display.max_columns', None)


    competencias_names = map(lambda competencia: competencia["name"], competencias_info)

    disciplinas_validas = filter(lambda disciplina: disciplina["serie_ano"] != 4, disciplinas_info)

    disciplinas_names = map(lambda disciplina: f"{disciplina["name"]} - {disciplina["serie_ano"]}", list(disciplinas_validas) )

    data['disciplinas'] = list(disciplinas_names)

    print('data',len(data['disciplinas']))

    for competencia in competencias_info:
        # create array of num 0.0 with competencias_names length
        inicial_array = [0.0] * len(data['disciplinas'])
        data[competencia["name"]] = inicial_array
        
    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_excel('data.xlsx', index=False)