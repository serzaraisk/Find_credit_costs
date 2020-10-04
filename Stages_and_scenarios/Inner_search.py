import pandas as pd
import numpy as np
from Settings_and_helper_functions import helper_functions
from Settings_and_helper_functions import Print_sub_functions
from Stars import Stars_settings


def inner_search_end_receiver(cash_flow, bank, initial_cash_flow, previous_receiver, all_operations_id, accounts_dict,
                              debug_lvl):
    """Рекурсия: должна проваливаться в банковские выписки контрагентов пока не найдет конечный счет

    :param cash_flow: анализируемая строчка(транж), которая была сформирована из выписки по ссудному счету
    :param bank: анализируемый банк (необходим для выгрузок из БД)
    :param initial_cash_flow: данные о первом получателе ссудных средств от заемщика
    :param previous_receiver: данные о заемщике
    :param all_operations_id: список всех id операций по контрагентам, которые участвовали в рекурсии
    :param accounts_dict: dict всех счетов, которые были ранее выгружены из БД
    :param debug_lvl: нужен для Print_sub_function, onределяет работу print
    :return: таблицу конечных получателей денежных средств + комментарии
    """

    inner_row_to_add = {}
    # на первом этапе рекурсии функция получает данные из уже готовой таблицы, отличную от банковской выписки,
    # поэтому на первом шаге идет переименование части данных
    if initial_cash_flow == '':
        initial_cash_flow = cash_flow[
            'initial_cash_flow_and_date']  # сохранил отдельно данные о первом получателе ссудных средств
        all_operations_id = {}
        cash_flow = cash_flow.copy()
        cash_flow['Номер счёта контрагента'] = ''
        cash_flow['Наименование исследуемого клиента'] = previous_receiver[
            'Наименование заемщика']  # наименование заемщика средств
        cash_flow['Идентификатор операции'] = 'Операция первого получателя заемных средств'
        cash_flow = cash_flow.rename(
            {'Направление(Название)': 'Наименование контрагента',
             'Направление(ИНН)': 'ИНН контрагента',
             'Направление(Банк)': 'Наименование банка контрагента',
             'Направление(Назначение платежа)': 'Назначение платежа',
             'Направление(Номер корреспондирующего счёта)': 'Номер внутреннего корреспондирующего счёта',
             'Направление (Дата перечисления)': 'Дата операции',
             'Направление (Сумма перечисления)': 'Эквивалент суммы по дебету'})

    if pd.isna(cash_flow['Наименование контрагента']):
        cash_flow['Наименование контрагента'] = ''  # иногда наименование контрагента в БД пустое

    # Под условие попадают как расчетные счета, так и ссудные
    if str(cash_flow['Номер внутреннего корреспондирующего счёта']).startswith('407'):
        Print_sub_functions.print_recursion_account(cash_flow, initial_cash_flow, debug_lvl)
        costs_list, all_operations_id = inner_analyze_first_scenario(cash_flow, bank, initial_cash_flow,
                                                                     previous_receiver, all_operations_id,
                                                                     accounts_dict, debug_lvl)

        Print_sub_functions.print_all_operations_id(all_operations_id, debug_lvl)
        iter_list = []
        # Использовать функцию Apply(axis=1) нельзя
        # https://stackoverflow.com/questions/31877909/pandas-function-dataframe-apply-runs-top-row-twice
        for row in costs_list.iterrows():
            iter_list.append(inner_search_end_receiver(row[1], bank, initial_cash_flow, previous_receiver,
                                                       all_operations_id, accounts_dict, debug_lvl))
        costs_list['dict_column'] = iter_list
        costs_list['Знаменатель для %'] = cash_flow['Эквивалент суммы по дебету']
        costs_list = upper_concat(costs_list[['Наименование контрагента', 'Знаменатель для %', 'dict_column']])
        return costs_list
    else:
        # print(cash_flow)
        if (pd.isna(cash_flow['Номер внутреннего корреспондирующего счёта'])
                and pd.isna(cash_flow['Номер счёта контрагента'])
                or
                (cash_flow['Номер внутреннего корреспондирующего счёта'].startswith('301'))):
            return helper_functions.create_inner_end_zero_row()
        Print_sub_functions.print_last_receiver(cash_flow, debug_lvl)
        helper_functions.create_inner_end_row(cash_flow, inner_row_to_add)
        return pd.DataFrame(inner_row_to_add)


def upper_concat(input_table):
    """Соединяет DataFrame состоящий из названия и dict конечного dict"""
    costs_df = pd.DataFrame()
    for row in input_table.iterrows():
        dict_to_df = pd.DataFrame(row[1]['dict_column'])
        dict_to_df['original_index'] = row[0]
        costs_df = costs_df.append(dict_to_df, sort=False)
    input_table.drop('dict_column', axis=1, inplace=True)
    input_table['original_index'] = input_table.index
    input_table.reset_index(inplace=True, drop=True)
    costs_df.reset_index(inplace=True, drop=True)
    input_table = input_table.merge(costs_df, 'outer', on='original_index', sort=False)
    input_table.reset_index(inplace=True, drop=True)
    input_table['percentage'] = input_table.apply(calculate_percentages, axis=1)
    input_table['percentage'] = input_table.apply(helper_functions.format_percentages, axis=1)
    input_table['Наименование контрагента'] = input_table['Наименование контрагента'].fillna('')
    input_table.loc[
        ((input_table['Конечный получатель (Целевое назначение)'] == 'Рефинансирование ссудной задолженности') &
         (input_table['Наименование контрагента'] == '')), 'Наименование контрагента'] = 'Банк'

    # print('Наименование контрагента')
    # print(input_table['Наименование контрагента'])
    input_table['Комментарий'] = '=>' + input_table['Наименование контрагента'] + ' (' + \
                                 input_table['percentage'] + ')' + input_table['Комментарий']
    #
    input_table['Числитель для %'] = input_table['Знаменатель для %']
    input_table.drop(['Наименование контрагента', 'Знаменатель для %', 'percentage'], axis=1, inplace=True)
    return input_table


def inner_analyze_first_scenario(cash_flow, bank, initial_cash_flow, previous_receiver, all_operations_id,
                                 accounts_dict, debug_lvl):
    """Отфильтровывает выписку по расчетному счету для нахождения наиболее соответствующих расходов по дебету счета

    :param cash_flow: анализируемая строчка(транж), которая была сформирована из выписки по ссудному счету
    :param bank: анализируемый банк (необходим для выгрузок из БД)
    :param initial_cash_flow: данные о первом получателе ссудных средств от заемщика
    :param previous_receiver: данные о заемщике
    :param all_operations_id: список всех id операций по контрагентам, которые участвовали в рекурсии
    :param accounts_dict: dict всех счетов, которые были ранее выгружены из БД
    :param debug_lvl: нужен для Print_sub_function, onределяет работу print
    :return: отфильтрованная выписка по расчетному счету, которая отражает соответствующие траншу расходования
    """

    # Загрузка выписки по необходимому расчетному счету
    account = cash_flow['Номер внутреннего корреспондирующего счёта']
    if cash_flow['Номер внутреннего корреспондирующего счёта'] not in accounts_dict.keys():
        Print_sub_functions.print_inner_account_search_start(account, debug_lvl)
        accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = \
            Stars_settings.sql_get_account_statement_info(bank,
                                                          cash_flow['Номер внутреннего корреспондирующего счёта'],
                                                          debug_lvl)
        Print_sub_functions.print_inner_account_search_end(account, debug_lvl)
        accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = \
            Stars_settings.convert_sql_table_to_acc_statement(
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']])
        accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта'] + 'clear'] = \
            Stars_settings.convert_sql_table_to_acc_statement(
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']])

    pandas_file = accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']]

    if pandas_file.shape[0] == 0:
        # print('первое условие inner_analyze_first_scenario')
        zero_table = pd.DataFrame(columns=pandas_file.columns)
        zero_table.loc[0, 'Направление (Целевое назначение)'] = \
            'Определить направление расходования не представляется возможным. Необходимо посмотреть вручную'
        return zero_table, all_operations_id

    # Сортировка выписки по дате и идентификатору (на данный момент для всех операций время было = 00:00:00)
    # print(pandas_file)
    # print('первый фильтр')
    pandas_file.sort_values(by=['Дата операции'], inplace=True)

    # Фильтруем выписку только по тем операциям, которые были в момент или после получения денег(транжа)
    searched_agent = pandas_file['Наименование исследуемого клиента'].iloc[0]
    date_object = cash_flow['Дата операции']
    if isinstance(date_object, str) and date_object != 'Не применимо':
        import datetime
        date_object = datetime.datetime.strptime(date_object, '%Y-%m-%d').date()

    try:
        # print('второй фильтр')
        # print(pandas_file[['Дата операции','Эквивалент суммы по дебету','Назначение платежа']])
        # print(cash_flow['Назначение платежа'])
        # print(~pandas_file['Идентификатор операции'].isin(list(all_operations_id[searched_agent])))
        filter_file = pandas_file[(pandas_file['Дата операции'] >= date_object)
                                  & (~pandas_file['Идентификатор операции'].isin(
            list(all_operations_id[searched_agent])))]
    except (KeyError):
        # print(pandas_file[['Дата операции','Эквивалент суммы по дебету','Назначение платежа']])
        # print(cash_flow['Номер внутреннего корреспондирующего счёта'])
        # print(cash_flow['Назначение платежа'])
        # print(cash_flow['Наименование исследуемого клиента'])
        filter_file = pandas_file[(pandas_file['Дата операции'] >= date_object)]

    #  старые фильтры

    # filter_for_df = \
    #    (0.1 * initial_cash_flow['Сумма транша'] <= filter_file['Эквивалент суммы по дебету']) & \
    #   (filter_file['Эквивалент суммы по дебету'] <= 1.3 * initial_cash_flow['Сумма транша'])

    # filter_for_df = (filter_file['Эквивалент суммы по дебету'] <= 1.3 * float(cash_flow['Эквивалент суммы по дебету']))

    # Использование первого фильтра(если первый фильтр не находит строк, то используется второй фильтр)
    # print(filter_file[['Дата операции','Эквивалент суммы по дебету']])
    # print('третий фильтр')
    # filter_file_for_identical_sums = filter_file[filter_for_df]

    filter_file_for_identical_sums = filter_file

    if filter_file_for_identical_sums.shape[0] == 0:
        # print('второе условие inner_analyze_first_scenario')
        zero_table = pd.DataFrame(columns=filter_file_for_identical_sums.columns)
        zero_table.loc[0, 'Направление (Целевое назначение)'] = \
            'Определить направление расходования не представляется возможным. Необходимо посмотреть вручную'
        return zero_table, all_operations_id

    min_day_for_filter_table = filter_file_for_identical_sums['Дата операции'].min()
    output_table = filter_file_for_identical_sums[
        (filter_file_for_identical_sums['Дата операции'] == min_day_for_filter_table)]
    min_day_for_filter_table_plus_one = min_day_for_filter_table
    # print(output_table[['Дата операции', 'Эквивалент суммы по дебету']])

    while True:
        # print(output_table[['Дата операции','Эквивалент суммы по дебету']])
        if output_table['Эквивалент суммы по дебету'].sum() >= 0.99 * float(cash_flow['Эквивалент суммы по дебету']):
            if (output_table['Эквивалент суммы по дебету'] == float(cash_flow['Эквивалент суммы по дебету'])).any():
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = helper_functions. \
                    filter_used_accounts_based_on_id(
                    accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']],
                    output_table)
                return output_table[
                           output_table['Эквивалент суммы по дебету'] == float(cash_flow['Эквивалент суммы по дебету'])
                           ], all_operations_id
            output_table = helper_functions.knapsack_filter_sum_function(output_table, cash_flow)
            if output_table['Эквивалент суммы по дебету'].sum() > 0.75 * float(cash_flow['Эквивалент суммы по дебету']):
                # print(output_table)
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = helper_functions. \
                    filter_used_accounts_based_on_id(
                    accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']],
                    output_table)
                return output_table, all_operations_id
            else:
                output_table = helper_functions.remove_min_element_function(output_table, cash_flow)
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = helper_functions. \
                    filter_used_accounts_based_on_id(
                    accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']],
                    output_table)
                return output_table, all_operations_id
        else:
            min_day_for_filter_table_plus_one = min_day_for_filter_table_plus_one + pd.Timedelta('1 days')
            output_table = filter_file_for_identical_sums[
                (filter_file_for_identical_sums['Дата операции'] <= min_day_for_filter_table_plus_one)]
        if min_day_for_filter_table_plus_one > min_day_for_filter_table + 10 * pd.Timedelta('1 days'):
            # print('третье условие inner_analyze_first_scenario')
            zero_table = pd.DataFrame(columns=output_table.columns)
            zero_table.loc[0, 'Направление (Целевое назначение)'] = \
                'Определить направление расходования не представляется возможным. Необходимо посмотреть вручную'
            return zero_table, all_operations_id


def add_operations_to_all_operations_id(output_table, all_operations_id):
    """Добавляет исследуемого контрагента и все операции, которые участвовали в рекурсии"""
    agent = output_table['Наименование исследуемого клиента'].iloc[0]
    operations_id = output_table['Идентификатор операции'].to_numpy()
    try:
        all_operations_id[agent] = np.unique(np.append(all_operations_id[agent], operations_id))
    except KeyError:
        all_operations_id[agent] = operations_id

    return all_operations_id


def calculate_percentages(cash_flow):
    """Рассчитывает проценты анализируемого расходования от предыдущего расходования (предыдущего получателя заемных средств)"""
    try:
        if cash_flow['Конечный получатель (Сумма перечисления)'] != 'Не применимо':
            if not pd.isna(cash_flow['Числитель для %']):
                # c = float(cash_flow['Числитель для %'])
                # d = float(cash_flow['Знаменатель для %'])
                # print(f'Числитель: {c}')
                # print(f'Знаменатель: {d}')
                return float(cash_flow['Числитель для %']) / float(cash_flow['Знаменатель для %'])
            else:
                # c = float(cash_flow['Конечный получатель (Сумма перечисления)'])
                # d = float(cash_flow['Знаменатель для %'])
                # print(f'Конечный получатель: {c}')
                # print(f'Знаменатель: {d}')
                return float(cash_flow['Конечный получатель (Сумма перечисления)']) / float(
                    cash_flow['Знаменатель для %'])
        else:
            return ''
    except KeyError:
        if cash_flow['Конечный получатель (Сумма перечисления)'] != 'Не применимо':
            # c = float(cash_flow['Конечный получатель (Сумма перечисления)'])
            # d = float(cash_flow['Знаменатель для %'])
            # print(f'Конечный получатель: {c}')
            # print(f'Знаменатель: {d}')
            return float(cash_flow['Конечный получатель (Сумма перечисления)']) / float(cash_flow['Знаменатель для %'])
        else:
            return ''
