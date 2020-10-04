import datetime
import pandas as pd
import numpy as np

from Stages_and_scenarios import Inner_search
from Settings_and_helper_functions import helper_functions


def inner_search_func(output_table, bank, initial_receiver, accounts_dict, debug_lvl):
    """Ищет и добавляет строки с конечными получателями средств и цепочками получателей денежных средств"""

    def return_initial_cash_flow_and_date(x):
        """Записывает в dict данные по первоначальному получателю денежных средств от заемщика"""
        date_object = x['Направление (Дата перечисления)']
        sum_object = x['Направление (Сумма перечисления)']
        if isinstance(date_object, str) and date_object != 'Не применимо':
            date_object = datetime.datetime.strptime(date_object, '%Y-%m-%d').date()
            sum_object = float(sum_object)
        return {'Сумма транша': sum_object,
                'Дата выдачи транша': date_object}

    output_table['initial_cash_flow_and_date'] = output_table.apply(return_initial_cash_flow_and_date, axis=1)
    initial_cash_flow = ''
    all_operations_id = ''
    # Использовать функцию Apply(axis=1) нельзя
    # https://stackoverflow.com/questions/31877909/pandas-function-dataframe-apply-runs-top-row-twice
    iter_list = []
    for row in output_table.iterrows():
        iter_list.append(Inner_search.inner_search_end_receiver(row[1], bank, initial_cash_flow, initial_receiver,
                                                                all_operations_id, accounts_dict, debug_lvl))
    output_table['dict_column'] = iter_list
    # Соединяем полученную таблицу первоначальных получателей заемных средств с конечными
    costs_df = pd.DataFrame()
    for row in output_table.iterrows():
        dict_to_df = row[1]['dict_column']
        try:
            dict_to_df.drop('Числитель для %', axis=1, inplace=True)
        except KeyError:
            pass
        dict_to_df['original_index'] = row[0]
        dict_to_df['Порядковый номер конечного получателя средств'] = np.arange(1, dict_to_df.shape[0] + 1)
        costs_df = costs_df.append(dict_to_df, sort=False)
    output_table.drop('dict_column', axis=1, inplace=True)
    output_table['original_index'] = output_table.index
    output_table.fillna('', inplace=True)
    output_table.reset_index(inplace=True)
    costs_df.reset_index(inplace=True)
    output_table = output_table.merge(costs_df, 'outer', on='original_index', sort=False)
    output_table.reset_index(inplace=True)

    # Дополняем строку комментарии
    output_table['initial_receiver'] = initial_receiver['Наименование заемщика']
    try:
        output_table['percentage'] = pd.to_numeric(output_table['Направление (Сумма перечисления)']) \
                                     / float(initial_receiver['Сумма транша'])
    except ValueError:
        output_table['percentage'] = 1
    output_table['percentage'] = output_table.apply(helper_functions.format_percentages, axis=1)
    for row in output_table.iterrows():
        if row[1]['Конечный получатель (Название)'] != 'Не применимо':
            output_table.loc[row[0], 'Комментарий'] = str(row[1]['initial_receiver'])+ '(100%)=>' \
                                                      + str(row[1]['Направление(Название)']) + \
                                                      '(' + str(row[1]['percentage']) + ')' \
                                                        + str(row[1]['Комментарий'])

            #
        else:
            output_table.loc[row[0], 'Комментарий'] = str(row[1]['initial_receiver']) + '(100%)=>' + str(row[1][
                'Направление(Название)']) + '(' + str(row[1]['percentage'] + ')')

    output_table['Порядковый номер первого получателя средств'] = output_table['original_index'] + 1
    # Выбираем только необходимые столбцы
    output_table = output_table[['Направление расходования ссудной задолженности',
                                 'Направление (Дата перечисления)',
                                 'Направление (Сумма перечисления)',
                                 'Направление(Название)',
                                 'Направление(ИНН)',
                                 'Направление(Банк)',
                                 'Направление(Номер корреспондирующего счёта)',
                                 'Направление(Назначение платежа)',
                                 'Направление (Целевое назначение)',
                                 'Конечный получатель (Название)',
                                 'Конечный получатель (ИНН)',
                                 'Конечный получатель (Дата перечисления контрагенту)',
                                 'Конечный получатель (Банк)',
                                 'Конечный получатель (Сумма перечисления)',
                                 'Конечный получатель (Назначение платежа)',
                                 'Конечный получатель (Номер счета контрагента)',
                                 'Конечный получатель (Целевое назначение)',
                                 'Комментарий',
                                 'Порядковый номер первого получателя средств',
                                 'Порядковый номер конечного получателя средств']]
    return output_table
