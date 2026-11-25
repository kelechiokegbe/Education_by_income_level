import os
import pandas as pd
import xlsxwriter 

def create_excel_doc_test(excel_doc):

    """
    Creates an excel doc with the given name as long as there is not already a doc. with that name

    Args: excel_doc(string): The name of the excel document where the outputs from the QA checks will be saved

    Outputs: xlsx: An excel file saved in the CDSW project area you are working in
    """

    directory_name = excel_doc.split('_')  # splits excel name into list based on presence of underscore
    directory = directory_name[0]  # Zeroth element of list == directory name - so HESA_QA_2025 will be saved to HESA

    file_exists = os._exists(excel_doc)

    if file_exists:
        print("!!!!! " + excel_doc + " already exists. No new file created!!!!!")

    elif os.path.isdir(directory):
        print(f"{directory} already exists")  # checks if directory exists, and prints message if it does
        save_path = f"D:/python/Hackathon_v2/Education_by_income_level/outputs/{directory}/"  # makes custom save path
        full_path = os.path.join(save_path, excel_doc)  # file path you want to save the file to e.g /home/cdsw/{directory}/filename
        writer = pd.ExcelWriter(full_path, engine='xlsxwriter')  # If you are returning to a QA you have already started do not run this line
        writer.close

    else:
        os.mkdir(directory)  # makes directory if it doesn't exist
        save_path =f"D:/python/Hackathon_v2/Education_by_income_level/outputs/{directory}/"  # makes custom save path
        full_path = os.path.join(save_path, excel_doc)  # file path you want to save the file to e.g /home/cdsw/{directory}/filename
        writer = pd.ExcelWriter(full_path, engine='xlsxwriter')  # If you are returning to a QA you have already started do not run this line
        writer.close()



excel_doc = "Education_by_Income_2017.xlsx"
create_excel_doc_test(excel_doc)




def exportItNoIndex(table, sheetName, excel_doc):
    """
    Exports data to excel doc created if the dataframe's index does not include relevant data.
    This is where some checks are coded without adapting the default row index to include relevant
    information and therefore this function runs the export without including the default row index.

    Args: table(Pandas df): The output table from the QA checks that are being run on a DataFrame
          sheetName(string): The name of the excel sheet in the excel document you are exporting
          excel_doc(string): The name of the Excel Doc. where the outputs from the QA checks will be saved

    Outputs: xlsx: Saves table to the excel file, formats column width to match the length of the text in the column
    """

    table = table.map(
        lambda x: x.encode('unicode_escape').decode('utf-8')
        if isinstance(x, str)
        else x
    )

    wb = openpyxl.load_workbook(
        excel_doc,
        data_only=True
    )  # opens the excel doc in an editable format

    if sheetName in wb.sheetnames:
        some_sheet = wb[sheetName]  # if the sheet name exists, open it
    else:
        some_sheet = wb.create_sheet(sheetName)  # if sheet doesn't exist, create it

    rows = dataframe_to_rows(
        table,
        index=False
    )  # converts pandas dataframe with index to a format that will allow passing into workbook

    to_enumerate = 2 + len(list(some_sheet.rows))
    # to calculate the row index that the table starts on, +2 as standard gap between table

    for r_idx, row in enumerate(rows, to_enumerate):
        # creates a list of row index and row value pairs

        for c_idx, value in enumerate(row, 1):
            # creates a list of column index and cell value pairs

            standard_format(
                some_sheet,
                r_idx,
                c_idx,
                value,
                thin_border
            )  # adds a border to cells

            header_format(
                some_sheet,
                r_idx,
                c_idx,
                value,
                thin_border,
                to_enumerate
            )  # adds header fill and bold

            number_format(
                some_sheet,
                r_idx,
                c_idx,
                value,
                thin_border
            )  # rounds all numbers to 2dp

    dims = {}

    for row in some_sheet.rows:
        for cell in row:
            if cell.value:  # if there is a value in the cell that's being read
                dims[cell.column_letter] = max(
                    (
                        dims.get(cell.column_letter, 0),
                        len(str(cell.value))
                    )
                )

    for col, value in dims.items():
        some_sheet.column_dimensions[col].width = value
        # set column width to the width of the cell being input

    wb.save(excel_doc)
    # closes the workbook in a way that makes it editable in the next function