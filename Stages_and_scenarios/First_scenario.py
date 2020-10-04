import pandas as pd
from Stars import Stars_settings
from Settings_and_helper_functions import Print_sub_functions, helper_functions


def analyse_first_scenario(cash_flow, bank, accounts_dict, debug_lvl):

    """Отфильтровывает выписку по расчетному счету для нахождения наиболее соответствующих расходов по дебету счета

    :param cash_flow: анализируемая строчка(транж), которая была сформирована из выписки по ссудному счету
    :param bank: анализируемый банк (необходим для выгрузок из БД)
    :param accounts_dict: dict всех счетов, которые были ранее выгружены из БД
    :param debug_lvl: нужен для Print_sub_function, onределяет работу print
    :return: отфильтрованная выписка по расчетному счету, которая отражает соответствующие траншу расходования
    """

    # Загрузка выписки по необходимому расчетному счету(если его нет в accounts_dict)
    account = cash_flow['Номер внутреннего корреспондирующего счёта']
    if cash_flow['Номер внутреннего корреспондирующего счёта'] not in accounts_dict.keys():
        Print_sub_functions.print_payment_account_search_start(account, debug_lvl)
        accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = \
            Stars_settings.sql_get_account_statement_info(bank,
                                                          cash_flow['Номер внутреннего корреспондирующего счёта'], debug_lvl)
        Print_sub_functions.print_payment_account_search_end(account, debug_lvl)
        accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = \
            Stars_settings.convert_sql_table_to_acc_statement(
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']])
        accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта'] + 'clear'] = \
            Stars_settings.convert_sql_table_to_acc_statement(
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']])

    pandas_file = accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']]

    # Сортировка выписки по дате(на данный момент для всех операций время было = 00:00:00)
    pandas_file.sort_values(by=['Дата операции'], inplace=True)

    # Фильтруем выписку только по тем операциям, которые были в момент или после получения денег(транжа)
    filter_file = pandas_file[pandas_file['Дата операции'] >= cash_flow['Дата выдачи транша']]
    # Пробный фильтр
    #filter_file = pandas_file[pandas_file['Идентификатор операции'] >= cash_flow['Идентификатор операции']]

    # Старые фильтры

    #filter_for_df = \
    #    (0.1 * cash_flow['Сумма транша'] <= filter_file['Эквивалент суммы по дебету']) & \
    #    (filter_file['Эквивалент суммы по дебету'] <= 1.3 * cash_flow['Сумма транша'])

    #filter_for_df = filter_file['Эквивалент суммы по дебету'] <= 1.3 * cash_flow['Сумма транша']

    #filter_file_for_identical_sums = filter_file[filter_for_df]
    filter_file_for_identical_sums = filter_file

    if filter_file_for_identical_sums.shape[0] == 0:
        zero_table = pd.DataFrame(columns=filter_file_for_identical_sums.columns)
        zero_table.loc[0, 'Направление (Целевое назначение)'] = \
            'Определить направление расходования не представляется возможным. Необходимо посмотреть вручную'
        return zero_table, accounts_dict

    # Описание общего алгоритма:
        # Датафрейм фильтруется по дню операции
        # Делается проверка, если общая сумма всех платежей за день превышает 90% от суммы транжа, то используется только один день
        # Если 90% не набираются, то добавляется еще следующий день после дня(итого два дня, потом три и т.д.) операции для фильтрации
        #

    min_day_for_filter_table = filter_file_for_identical_sums['Дата операции'].min()
    output_table = filter_file_for_identical_sums[
        (filter_file_for_identical_sums['Дата операции'] == min_day_for_filter_table)]
    min_day_for_filter_table_plus_one = min_day_for_filter_table

    while True:
        if output_table['Эквивалент суммы по дебету'].sum() >= 0.99 * cash_flow['Сумма транша']:
            if (output_table['Эквивалент суммы по дебету'] == cash_flow['Сумма транша']).any():
                output_table = output_table[output_table['Эквивалент суммы по дебету'] == cash_flow['Сумма транша']]
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = helper_functions. \
                    filter_used_accounts_based_on_id(
                    accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']],
                    output_table)
                return output_table[output_table['Эквивалент суммы по дебету'] == cash_flow['Сумма транша']], accounts_dict

            output_table = helper_functions.knapsack_filter_sum_function(output_table, cash_flow)
            if output_table['Эквивалент суммы по дебету'].sum() > 0.75 * float(cash_flow['Сумма транша']):
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = helper_functions.\
                                            filter_used_accounts_based_on_id(
                                            accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']],
                                            output_table)
                return output_table, accounts_dict

            else:
                output_table = helper_functions.remove_min_element_function(output_table, cash_flow)
                accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']] = helper_functions. \
                    filter_used_accounts_based_on_id(
                    accounts_dict[cash_flow['Номер внутреннего корреспондирующего счёта']],
                    output_table)
                return output_table, accounts_dict


        else:
            min_day_for_filter_table_plus_one = min_day_for_filter_table_plus_one + pd.Timedelta('1 days')
            output_table = filter_file_for_identical_sums[
                (filter_file_for_identical_sums['Дата операции'] <= min_day_for_filter_table_plus_one)]
        if min_day_for_filter_table_plus_one > min_day_for_filter_table + 30 * pd.Timedelta('1 days'):
            zero_table = pd.DataFrame(columns=output_table.columns)
            zero_table.loc[0, 'Направление (Целевое назначение)'] = \
                'Определить направление расходования не представляется возможным. Необходимо посмотреть вручную'
            return zero_table, accounts_dict

