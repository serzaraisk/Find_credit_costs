from Settings_and_helper_functions import Settings, helper_functions
import pandas as pd


def filter_unsuitable_rows(input_file):
    """Фильтрует строки первоначальной таблицы, так чтобы они подходили по одному из описанных сценариев"""

    # Сценарий 1: перевод с ссудного счета на расчетный счет (.str.contains(r'^40[1-8]\d*')))
    # Сценарий 2: перевод с ссудного счета на кассу (.str.contains(r'^202\d*')))
    # Сценарий 3: перевод с ссудного счета на счет в другом банке (.isna()))
    # pd.notna(input_file['Дата операции'] нужна для фильтрации входящих и исходящих остатков

    return input_file[(input_file['Номер внутреннего корреспондирующего счёта'].str.contains(r'^40[1-8]\d*') |
                       input_file['Номер внутреннего корреспондирующего счёта'].str.contains(r'^202\d*') |
                       input_file['Номер внутреннего корреспондирующего счёта'].str.contains(r'^303\d*') | # добавил по 303 счетам
                       input_file['Номер внутреннего корреспондирующего счёта'].isna()) &
                      (input_file['Номер счёта контрагента'].str.contains(r'^40[1-8]\d*') |
                       input_file['Номер счёта контрагента'].str.contains(r'^202\d*') |
                       input_file['Номер счёта контрагента'].isna()) &
                      (input_file['Эквивалент суммы по кредиту'] == 0) &
                      (pd.notna(input_file['Дата операции']))]


def fill_rows_based_on_credit_account(output_file, filtered_file):
    """Заполняет часть первоначальной таблицы на основе данных кредитного счета

    :param output_file: Шаблон конечной таблицы
    :param filtered_file: Отфильтрованная по сценариям выписка по кредитному счету
    :return: Конечную таблицу, частично заполненную данными  из выписки по кредитному счету
    """

    # Определяется код валюты исходя из части счета
    currency = Settings.currency_dict[filtered_file['Номер исследуемого счёта'].iloc[0][5:8]]['code']
    credits_sum = filtered_file['Эквивалент суммы по дебету'].sum()
    for row in filtered_file.iterrows():
        # Дата и № договора парсятся из назначения платежа
        act, date = helper_functions.parse_act_date_contract(row[1]['Назначение платежа'])
        # Проверка: если номер счета 303, то межфилиал и нужно брать счет контрагента
        if str(row[1]['Номер внутреннего корреспондирующего счёта']).startswith('303'):
            account_number = row[1]['Номер счёта контрагента']
        else:
            account_number = row[1]['Номер внутреннего корреспондирующего счёта']

        output_file = output_file.append({'Наименование заемщика': row[1]['Наименование исследуемого клиента'],
                                          'ИНН заемщика': row[1]['ИНН исследуемого клиента'],
                                          'Номер кредитного договора': act,
                                          'Дата кредитного договора': date,
                                          'Валюта кредита': currency,
                                          'Сумма выданных в исследуемом периоде траншей': credits_sum,
                                          'Дата выдачи транша': row[1]['Дата операции'],
                                          'Сумма транша': row[1]['Эквивалент суммы по дебету'],
                                          'Номер внутреннего корреспондирующего счёта':
                                              account_number,
                                          'Направление (Дата перечисления)': row[1]['Дата операции'],
                                          'Направление (Сумма перечисления)': row[1]['Эквивалент суммы по дебету'],
                                          'Направление(Название)': row[1]['Наименование контрагента'],
                                          'Направление(ИНН)': row[1]['ИНН банка контрагента'],
                                          'Направление(Банк)': row[1]['Наименование банка контрагента'],
                                          'Направление(Номер корреспондирующего счёта)': 'Не применимо',
                                          'Направление(Назначение платежа)': row[1]['Назначение платежа'],
                                          'Направление (Целевое назначение)': 'Не применимо',
                                          'Конечный получатель (Название)': 'Не применимо',
                                          'Конечный получатель (ИНН)': 'Не применимо',
                                          'Конечный получатель (Дата перечисления контрагенту)': 'Не применимо',
                                          'Конечный получатель (Банк)': 'Не применимо',
                                          'Конечный получатель (Сумма перечисления)': 'Не применимо',
                                          'Конечный получатель (Назначение платежа)': 'Не применимо',
                                          'Конечный получатель (Номер счета контрагента)': 'Не применимо',
                                          'Конечный получатель (Целевое назначение)': 'Не применимо',
                                          'Комментарий': 'Не применимо',
                                          'Порядковый номер кредитного договора': row[1]['Порядковый номер кредитного договора']},
                                         ignore_index=True)

    # Группировка по дням
    if output_file.shape[0] > 1:
        output_file = output_file.head(1).append(group_by_credit_rows_based_on_date(output_file.iloc[1:]), sort=False)
    return output_file


def group_by_credit_rows_based_on_date(input_table):
    """Группирует df по дням выдачи транжа, для каждой группы берет первую строчку и заменяет сумму транжа в этой строчке на сумму всех транжей за день"""

    output_table = input_table.groupby('Дата выдачи транша').first()
    output_table = output_table.reset_index()
    for row in output_table.iterrows():
        output_table.loc[row[0], 'Сумма транша'] = input_table[
            input_table['Дата выдачи транша'] == row[1]['Дата выдачи транша']]['Сумма транша'].sum()

    return output_table


