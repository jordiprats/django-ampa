import pandas

excel_data_df = pandas.read_excel('P5C.xls', sheet_name='Hoja1', )

excel_data_df = excel_data_df[6:] #take the data less the header row

excel_data_df.columns = [
                "id_nen",
                "nom",
                "cognom1",
                "cognom2",
                "naixement",
                "pare",
                "telf1",
                "mare",
                "telf2",
                "email",
                "cessio",
                "signatura"
            ]

excel_data_df = excel_data_df.dropna(subset=['id_nen', 'nom', 'cognom1'])

# print whole sheet data
print(excel_data_df)
