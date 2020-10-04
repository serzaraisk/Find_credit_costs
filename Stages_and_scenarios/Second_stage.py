from Stages_and_scenarios import First_scenario
from Settings_and_helper_functions import helper_functions
import pandas as pd
from Stages_and_scenarios.Third_stage import inner_search_func

pd.options.mode.chained_assignment = None


def fill_rows_based_on_payment_account(cash_flow, bank, accounts_dict, debug_lvl):
    """Создает dict c информацией о расходовании кредитных средств

    :param cash_flow: анализируемая строчка(транж), которая была сформирована из выписки по ссудному счету
    :param bank: анализируемый банк (необходим для выгрузок из БД)
    :param accounts_dict: dict всех счетов, которые были ранее выгружены из БД
    :param debug_lvl: нужен для Print_sub_function, onределяет работу print

    :return: dict c информацией о расходовании кредитных средств
    """
    #  фильтр от первой строчки таблицы (нумерация)
    row_to_add = {} if cash_flow['Комментарий'] != 22 else ''

    if cash_flow['Номер внутреннего корреспондирующего счёта'] != 9:

        # Кредитные средства выданы с ссудного счета счета Заемщика на расчетный счет
        if str(cash_flow['Номер внутреннего корреспондирующего счёта']).startswith('4'):
            row_to_add = {
                'Направление расходования ссудной задолженности': ['Перечисление на расчетный / текущий счет Заемщика']}
            costs_list, accounts_dict = First_scenario.analyse_first_scenario(cash_flow, bank, accounts_dict, debug_lvl)
            if costs_list.shape[0] == 0:
                helper_functions.create_zero_row(row_to_add)
            # создаем dict для дальнейшего DataFrame
            for cost in costs_list.iterrows():
                try:
                    helper_functions.add_row(cost, row_to_add)
                except KeyError:
                    helper_functions.create_row(cost, row_to_add)

        # Кредитные средства выданы с ссудного счета счета Заемщика через кассу
        elif str(cash_flow['Номер внутреннего корреспондирующего счёта']).startswith('2'):
            row_to_add = {'Направление расходования ссудной задолженности': ['Через кассу Банка']}
            helper_functions.create_zero_row(row_to_add)

        # Кредитные средства перечислены на расчетный / текущий счет заемщика или контрагента в другую К
        else:
            row_to_add = {'Направление расходования ссудной задолженности':
                [
                    'кредитные средства перечислены на расчетный / текущий счет заемщика или контрагента в другую КО']}
            helper_functions.create_zero_row(row_to_add)
    return row_to_add


def fill_rows_from_dict(output_table_1, order_num, order_INN, bank, accounts_dict, debug_lvl):
    """Заполняет output таблицу на основе сформированного dict c информацией о расходовании кредитных средств

    :param bank: анализируемый банк (необходим для выгрузок из БД)
    :param accounts_dict: dict всех счетов, которые были ранее выгружены из БД
    :param debug_lvl: нужен для Print_sub_function, onределяет работу print
    :param order_INN: порядок ИНН
    :param order_num: порядок ссудных счетов
    :param output_table_1: output таблица с уже заполненным dict c информацией о расходовании кредитных средств
    :return: заполненную по колонкам output таблицу
    """
    costs_df = pd.DataFrame()
    for row in output_table_1.iterrows():
        if isinstance(row[1]['dict_column'], dict):
            dict_to_df = pd.DataFrame(row[1]['dict_column'])
            if dict_to_df.shape[0] != 0:
                initial_receiver = row[1]
                dict_to_df = inner_search_func(dict_to_df, bank, initial_receiver, accounts_dict, debug_lvl)
                dict_to_df['original_index'] = row[0]
                costs_df = costs_df.append(dict_to_df, sort=False)
    output_table_1.drop('dict_column', axis=1, inplace=True)
    output_table_1['original_index'] = output_table_1.index
    output_table_1.reset_index(inplace=True)
    costs_df.reset_index(inplace=True)
    output_table_1 = output_table_1.merge(costs_df, 'outer', on='original_index', suffixes=('', '_cost_df'), sort=False)
    output_table_1.reset_index(inplace=True)
    output_table_1 = replace_values_from_merge_columns(output_table_1, order_num, order_INN)
    return output_table_1


def replace_values_from_merge_columns(output_table_1, order_num, order_INN):
    """Мэтчит старые и cost_df колонки, забирая информацию из cost_df колонки если она не None(также подготавливает нумерацию)"""
    map_dict = {'Направление (Дата перечисления)': 'Направление (Дата перечисления)_cost_df',
                'Направление (Сумма перечисления)': 'Направление (Сумма перечисления)_cost_df',
                'Направление (Целевое назначение)': 'Направление (Целевое назначение)_cost_df',
                'Направление расходования ссудной задолженности': 'Направление расходования ссудной задолженности_cost_df',
                'Направление(Банк)': 'Направление(Банк)_cost_df',
                'Направление(ИНН)': 'Направление(ИНН)_cost_df',
                'Направление(Название)': 'Направление(Название)_cost_df',
                'Направление(Назначение платежа)': 'Направление(Назначение платежа)_cost_df',
                'Направление(Номер корреспондирующего счёта)': 'Направление(Номер корреспондирующего счёта)_cost_df',
                'Конечный получатель (Название)': 'Конечный получатель (Название)_cost_df',
                'Конечный получатель (ИНН)': 'Конечный получатель (ИНН)_cost_df',
                'Конечный получатель (Дата перечисления контрагенту)': 'Конечный получатель (Дата перечисления контрагенту)_cost_df',
                'Конечный получатель (Банк)': 'Конечный получатель (Банк)_cost_df',
                'Конечный получатель (Сумма перечисления)': 'Конечный получатель (Сумма перечисления)_cost_df',
                'Конечный получатель (Назначение платежа)': 'Конечный получатель (Назначение платежа)_cost_df',
                'Конечный получатель (Номер счета контрагента)': 'Конечный получатель (Номер счета контрагента)_cost_df',
                'Конечный получатель (Целевое назначение)': 'Конечный получатель (Целевое назначение)_cost_df',
                'Комментарий': 'Комментарий_cost_df'
                }
    for key, value in map_dict.items():
        for row in range(1, output_table_1.shape[0]):
            if output_table_1.loc[row, value] is not None:
                output_table_1.loc[row, key] = output_table_1.loc[row, value]
            else:
                continue
        output_table_1.drop([value], axis=1, inplace=True)

    output_table_1['level_0'] = str(order_INN) + ' (' + output_table_1['ИНН заемщика'].astype('str') + ')'
    output_table_1['Порядковый номер исследуемого ссудного счета'] = str(order_INN) + '.' + str(order_num) + ' (' \
                                                                     + output_table_1[
                                                                         'Порядковый номер кредитного договора'] \
                                                                         .astype('str') + ')'

    output_table_1['index'] = (str(order_INN) + '.' + str(order_num) \
                               + '.' + output_table_1['original_index'].astype('str'))  #
    output_table_1['Порядковый номер первого (после заемщика) получателя средств'] = output_table_1['index'] + '.' + \
                                                                                    output_table_1[
                                                                                        'Порядковый номер первого получателя средств'] \
                                                                                        .astype('str').str.replace('.0',
                                                                                                                   '')
    output_table_1['Порядковый номер конечного получателя средств'] = \
        output_table_1['Порядковый номер первого (после заемщика) получателя средств'] + '.' + output_table_1[
            'Порядковый номер конечного получателя средств'] \
            .astype('str').str.replace('.0', '')

    output_table_1.drop(['Порядковый номер кредитного договора'], axis=1, inplace=True)
    output_table_1.drop(['original_index'], axis=1, inplace=True)
    output_table_1.drop(['index_cost_df'], axis=1, inplace=True)
    output_table_1['Направление (Сумма перечисления)'] = output_table_1['Направление (Сумма перечисления)'].astype(
        'float', errors='ignore')
    output_table_1.rename(columns={'level_0': 'Порядковый № исследуемого ИНН',
                                   'index': 'Порядковый № кредитного транжа'}, inplace=True)
    return output_table_1
