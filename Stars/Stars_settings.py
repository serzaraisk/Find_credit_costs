import pandas as pd

import pyodbc
from Settings_and_helper_functions import Print_sub_functions


def create_connection():
    """Создает connection к серверу RUMSKDB25,1113, к БД STAR"""
    server_name = 'RUMSKDB25,1113'
    database_name = 'STAR'
    connection = pyodbc.connect(f'''
            Driver={{SQL Server Native Client 11.0}};
            Server={server_name};
            Database={database_name};
            Trusted_Connection=yes;
            ''')
    cursor = connection.cursor()
    return connection, cursor


def sql_get_account_statement_info(bank, account, debug_lvl):
    """Делает запрос в БД STAR по выгрузке выписки по счету и возврает выписку в DataFrame"""
    connection, cursor = create_connection()
    sql_get_account_statement = \
        f'''EXEC	[get.2.8].[Statements]
                @SearchBankName = N\'{bank}\',
                @SearchParameter = N'15',
                @SearchCondition = N\'{account}\''''
    Print_sub_functions.print_get_credit_accounts_list_query(sql_get_account_statement, debug_lvl)
    try:
        output_table = pd.read_sql_query(sql_get_account_statement, connection)
    except TypeError:
        Print_sub_functions.print_connection_for_statement_doesnt_work(account, debug_lvl)
        output_table = pd.DataFrame(columns=['Счёт'])
    cursor.close()
    connection.close()
    return output_table


def sql_get_accounts_based_on_INN(bank, INN, debug_lvl):
    """Делает запрос в БД STAR по выгрузке счетов клиента на основе ИНН и возврает выписку в DataFrame"""
    connection, cursor = create_connection()
    sql_get_account_based_on_INN = \
        f'''EXEC	[get.2.8].[InstitutionAccounts]
                @SearchBankName = N\'{bank}\',
                @SearchParameter = N'111',
                @SearchCondition = N\'{INN}\''''
    Print_sub_functions.print_get_accounts_based_on_INN_query(sql_get_account_based_on_INN, debug_lvl)
    try:
        output_table = pd.read_sql_query(sql_get_account_based_on_INN, connection)
    except TypeError:
        Print_sub_functions.print_connection_for_INN_doesnt_work(INN, debug_lvl)
        output_table = pd.DataFrame(columns=['Счёт'])
    cursor.close()
    connection.close()
    return output_table


def convert_sql_table_to_acc_statement(input_table):
    """Конвертирует английские названия столбцов, получаемых из БД, в русские на основе мэппинга в dict"""
    start_col_map = {eng: rus['Описание поля'] for eng, rus in starts_col_dict.items()}
    input_table = input_table.rename(start_col_map, axis=1)
    return input_table[account_statement_columns]


starts_col_dict = {"BankID": {"Описание поля": "Идентификатор банка", "№": "1"},
                   "BankName": {"Описание поля": "Наименование банка", "№": "2"},
                   "BankInn": {"Описание поля": "ИНН банка", "№": "3"},
                   "BankBic": {"Описание поля": "БИК банка", "№": "4"},
                   "BankAccountCorrespondent": {"Описание поля": "Корреспондентский счет банка", "№": "5"},
                   "InstitutionID": {"Описание поля": "Идентификатор исследуемого клиента", "№": "6"},
                   "InstitutionType": {"Описание поля": "Тип исследуемого клиента", "№": "7"},
                   "InstitutionName": {"Описание поля": "Наименование исследуемого клиента", "№": "8"},
                   "InstitutionInn": {"Описание поля": "ИНН исследуемого клиента", "№": "9"},
                   "InstitutionAccountID": {"Описание поля": "Идентификатор счёта исследуемого клиента", "№": "10"},
                   "InstitutionAccountType": {"Описание поля": "Тип счёта исследуемого клиента", "№": "11"},
                   "InstitutionAccountName": {"Описание поля": "Наименование счёта исследуемого клиента", "№": "12"},
                   "InstitutionAccount": {"Описание поля": "Номер исследуемого счёта", "№": "13"},
                   "InnerInstitutionID": {"Описание поля": "Идентификатор внутреннего корреспондирующего клиента",
                                          "№": "14"},
                   "InnerInstitutionType": {"Описание поля": "Тип внутреннего корреспондирующего клиента", "№": "15"},
                   "InnerInstitutionName": {"Описание поля": "Наименование внутреннего корреспондирующего клиента",
                                            "№": "16"},
                   "InnerInstitutionInn": {"Описание поля": "ИНН внутреннего корреспондирующего клиента", "№": "17"},
                   "InnerInstitutionAccountID": {
                       "Описание поля": "Идентификатор счёта внутреннего корреспондирующего клиента", "№": "18"},
                   "InnerInstitutionAccountType": {"Описание поля": "Тип счёта внутреннего корреспондирующего клиента",
                                                   "№": "19"},
                   "InnerInstitutionAccountName": {"Описание поля": "Наименование внутреннего корреспондирующего счёта",
                                                   "№": "20"},
                   "InnerInstitutionAccount": {"Описание поля": "Номер внутреннего корреспондирующего счёта",
                                               "№": "21"},
                   "PartnerName": {"Описание поля": "Наименование контрагента", "№": "22"},
                   "PartnerInn": {"Описание поля": "ИНН контрагента", "№": "23"},
                   "PartnerAccountType": {"Описание поля": "Тип счёта контрагента", "№": "24"},
                   "PartnerAccount": {"Описание поля": "Номер счёта контрагента", "№": "25"},
                   "BankPartnerID": {"Описание поля": "Идентификатор банка контрагента", "№": "26"},
                   "BankPartnerName": {"Описание поля": "Наименование банка контрагента", "№": "27"},
                   "BankPartnerInn": {"Описание поля": "ИНН банка контрагента", "№": "28"},
                   "BankPartnerBic": {"Описание поля": "БИК банка контрагента", "№": "29"},
                   "BankPartnerAccountCorrespondent": {"Описание поля": "Корреспондентский счёт банка контрагента",
                                                       "№": "30"},
                   "OperationID": {"Описание поля": "Идентификатор операции", "№": "31"},
                   "OperationType": {"Описание поля": "Тип операции", "№": "32"},
                   "OperationInstrumentID": {"Описание поля": "Идентификатор инструмента операции", "№": "33"},
                   "OperationInstrumentName": {"Описание поля": "Наименование инструмента операции", "№": "34"},
                   "OperationDocumentNumber": {"Описание поля": "Номер документа операции", "№": "35"},
                   "OperationDate": {"Описание поля": "Дата операции", "№": "36"},
                   "OperationYear": {"Описание поля": "Год операции", "№": "37"},
                   "OperationMonth": {"Описание поля": "Месяц операции", "№": "38"},
                   "OperationDay": {"Описание поля": "День операции", "№": "39"},
                   "OperationTime": {"Описание поля": "Время операции", "№": "40"},
                   "OperationActualDate": {"Описание поля": "Фактическая дата операции", "№": "41"},
                   "OperationActualYear": {"Описание поля": "Фактический год операции", "№": "42"},
                   "OperationActualMonth": {"Описание поля": "Фактический месяц операции", "№": "43"},
                   "OperationActualDay": {"Описание поля": "Фактический день операции", "№": "44"},
                   "OperationActualTime": {"Описание поля": "Фактическое время операции", "№": "45"},
                   "OperationDescription": {"Описание поля": "Назначение платежа", "№": "46"},
                   "AmountReal": {"Описание поля": "Сумма в валюте счёта", "№": "47"},
                   "AmountRealDebit": {"Описание поля": "Сумма в валюте счёта по дебету", "№": "48"},
                   "AmountRealCredit": {"Описание поля": "Сумма в валюте счёта по кредиту", "№": "49"},
                   "AmountEquivalent": {"Описание поля": "Эквивалент суммы", "№": "50"},
                   "RestIn": {"Описание поля": "Входящий остаток", "№": "51"},
                   "AmountEquivalentDebit": {"Описание поля": "Эквивалент суммы по дебету", "№": "52"},
                   "AmountEquivalentCredit": {"Описание поля": "Эквивалент суммы по кредиту", "№": "53"},
                   "RestOut": {"Описание поля": "Исходящий остаток", "№": "54"},
                   "CurrencyInstitutionID": {"Описание поля": "Идентификатор валюты исследуемого счёта", "№": "55"},
                   "CurrencyInstitutionName": {"Описание поля": "Наименование валюты исследуемого счёта", "№": "56"},
                   "CurrencyCorrespondentID": {"Описание поля": "Идентификатор валюты счёта контрагента", "№": "57"},
                   "CurrencyCorrespondentName": {"Описание поля": "Наименование валюты счёта контрагента", "№": "58"},
                   "CurrencyExchangeCourse": {"Описание поля": "Курс обмена валюты", "№": "59"}}

account_statement_columns = ['Номер исследуемого счёта', 'Дата операции', 'Время операции',
                              'Наименование исследуемого клиента', 'ИНН исследуемого клиента',
                              'Наименование внутреннего корреспондирующего клиента',
                              'ИНН внутреннего корреспондирующего клиента',
                              'Наименование внутреннего корреспондирующего счёта',
                              'Номер внутреннего корреспондирующего счёта',
                              'Наименование контрагента', 'ИНН контрагента', 'Тип счёта контрагента',
                              'Номер счёта контрагента', 'Наименование банка контрагента',
                              'ИНН банка контрагента', 'БИК банка контрагента',
                              'Корреспондентский счёт банка контрагента', 'Номер документа операции',
                              'Год операции', 'Месяц операции', 'День операции',
                              'Сумма в валюте счёта по дебету', 'Сумма в валюте счёта по кредиту',
                              'Входящий остаток',
                              'Эквивалент суммы по дебету', 'Эквивалент суммы по кредиту',
                              'Исходящий остаток',
                              'Курс обмена валюты', 'Назначение платежа', 'Идентификатор операции']
