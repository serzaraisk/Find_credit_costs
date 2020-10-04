import datetime


def print_inn_list(inn_list, debug_lvl):
    if debug_lvl > 1:
        print('Список анализируемых ИНН:')
        print('\n'.join([str(INN) for INN in inn_list]))


def print_inn_for_analysis(inn, debug_lvl):
    if debug_lvl > 1:
        print('=' * 40)
        print(f'Анализируемый ИНН: {inn} ')


def print_accounts_list(credit_accounts_list, debug_lvl):
    if debug_lvl > 1:
        print('*' * 40)
        print('Список анализируемых счетов:')
        credit_accounts_list_print = [(pos, acc) for pos, acc in
                                      zip(range(1, len(credit_accounts_list) + 1), credit_accounts_list)]
        print(';\n'.join([str(acc[0]) + ": " + acc[1] for acc in credit_accounts_list_print]))
        print('*' * 40)


def print_account_list_kicked(accounts_list, filter_credit_accounts, debug_lvl):
    if debug_lvl > 4:
        credit_accounts_list = accounts_list[~filter_credit_accounts].unique()
        print('-' * 40)
        print('Список отброшенных счетов:')
        credit_accounts_list_print = [(pos, acc) for pos, acc in
                                      zip(range(1, len(credit_accounts_list) + 1), credit_accounts_list)]
        print(';\n'.join([str(acc[0]) + ": " + acc[1] for acc in credit_accounts_list_print]))
        print('-' * 40)


def print_get_credit_accounts_list_query(sql_get_account_statement, debug_lvl):
    if debug_lvl > 3:
        print('*' * 40)
        print(sql_get_account_statement)
        print('*' * 40)


def print_get_accounts_based_on_INN_query(sql_get_account_statement, debug_lvl):
    if debug_lvl > 3:
        print('*' * 40)
        print(sql_get_account_statement)
        print('*' * 40)


def print_account_search_start(order, credit_account, credit_accounts_list, debug_lvl):
    if debug_lvl > 1:
        import datetime
        credit_accounts_list_print = [(pos, acc) for pos, acc in
                                      zip(range(1, len(credit_accounts_list) + 1), credit_accounts_list)]
        print(
            f'[{order + 1}/{len(credit_accounts_list_print)}] {datetime.datetime.now()}: выгрузка ссудного счета {credit_account} из БД')


def print_account_search_end(order, credit_account, credit_accounts_list, debug_lvl):
    if debug_lvl > 1:
        import datetime
        credit_accounts_list_print = [(pos, acc) for pos, acc in
                                      zip(range(1, len(credit_accounts_list) + 1), credit_accounts_list)]
        print(
            f'[{order + 1}/{len(credit_accounts_list_print)}] {datetime.datetime.now()}: выгрузка ссудного счета {credit_account} из БД закончена\n')


def print_payment_account_search_start(account, debug_lvl):
    if debug_lvl > 1:
        print(f'{datetime.datetime.now()}: выгрузка счета {account} из БД')


def print_payment_account_search_end(account, debug_lvl):
    if debug_lvl > 1:
        print(f'{datetime.datetime.now()}: выгрузка счета {account} из БД закончена\n')


def print_inner_account_search_start(account, debug_lvl):
    if debug_lvl > 1:
        print(f'{datetime.datetime.now()}: Поиск конечного получателя средств по счету {account} ')


def print_inner_account_search_end(account, debug_lvl):
    if debug_lvl > 1:
        print(f'{datetime.datetime.now()}: Поиск конечного получателя средств по счету {account} из БД закончена\n')


def print_recursion_account(cash_flow, initial_sum_and_date, debug_lvl):
    if debug_lvl > 2:
        receiver = cash_flow['Наименование контрагента']
        acc = cash_flow['Номер внутреннего корреспондирующего счёта']
        date = cash_flow['Дата операции']
        sum_cash = cash_flow['Эквивалент суммы по дебету']
        identificator = cash_flow['Идентификатор операции']
        initial_sum = initial_sum_and_date['Сумма транша']
        initial_date = initial_sum_and_date['Дата выдачи транша']
        print('-' * 60)
        print(f'>>>>Рекурсия по счету: {acc}. Контрагент: {receiver}.\n'
              f'>>>>Дата операции {date}. Сумма операции {sum_cash}. Идентификатор операции {identificator} \n'
              f'>>>>Первоначальная сумма {initial_sum}. Первоначальная дата {initial_date}')
        print('=' * 60)


def print_last_receiver(cash_flow, debug_lvl):
    if debug_lvl > 2:
        receiver = cash_flow['Наименование контрагента']
        acc = cash_flow['Номер внутреннего корреспондирующего счёта']
        date = cash_flow['Дата операции']
        print(f'>>>>Конечный получатель средств {receiver}. Проводка по счету {acc}. Дата операции {date}')


def print_all_operations_id(all_operations_id, debug_lvl):
    if debug_lvl > 3:
        print(f'>>>>Список всех операций по контрагентам(рекурсия):')
        print(all_operations_id)


def print_connection_for_INN_doesnt_work(INN, debug_lvl):
    if debug_lvl > 1:
        print(f'!!!!!!!! Выписка по ИНН {INN} не была получена !!!!!!!!')


def print_connection_for_statement_doesnt_work(account, debug_lvl):
    if debug_lvl > 1:
        print(f'!!!!!!!! Выписка по счету {account} не была получена !!!!!!!!')
