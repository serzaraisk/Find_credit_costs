import pandas as pd
import warnings

from Settings_and_helper_functions import Settings, helper_functions, Print_sub_functions
from Stages_and_scenarios import First_stage, Second_stage
from Stars import Stars_settings

# отключил предупреждения pandas, связанные с найденными regex группами(в алгоритме важен только сам факт их нахождения)
warnings.filterwarnings("ignore", 'This pattern has match groups')

if __name__ == "__main__":
    INN_list = ['7726722697','7716677131','7728848663','7708762376','7707808660','7723820706','7708758299',
                '7811509546','7811509546','7726722697','7717731173','7840037714','7721679938']
    bank = 'ТГБ (Бисквит)'
    output_tables = []  # Хранит в себе в себе финальные таблицы, разбитые по ИНН
    accounts_dict = {}  # хранит в себе список всех банковских выписок, которые были выгружены из БД (нужен для того, чтобы  не выгружать выписки по 2 и более раз)
    debug_lvl = 3
    # 1 Функции print не выдают информацию
    # 2 Функции print выдают информацию о ходе загрузки запрашиваемых БД счетов
    # 3 Функции print  также выдают детальную информацию по каждому этапу (также делает выгрузку в excel всех анализируемых в алгоритме банковских счетов)
    # 4 Функции print также выдают запрашиваемые sql query серверу (также делает выгрузку в excel всех анализируемых в алгоритме банковских счетов)
    Print_sub_functions.print_inn_list(INN_list, debug_lvl)

    # Первый этап: поиск всех ссудных счетов клиента
    for order_INN, INN in enumerate(INN_list, 1):
        Print_sub_functions.print_inn_for_analysis(INN, debug_lvl)
        credit_accounts_list = list(helper_functions.get_credit_accounts_list(bank, INN, debug_lvl))
        Print_sub_functions.print_accounts_list(credit_accounts_list, debug_lvl)

        empty_df = 0  # показывает количество пустых ссудных счетов (нужно для нумерации строк)

        for order, credit_account in enumerate(credit_accounts_list):
            # Второй этап: выгрузка ссудного счета в df
            Print_sub_functions.print_account_search_start(order, credit_account, credit_accounts_list, debug_lvl)
            credit_account_statement = Stars_settings.sql_get_account_statement_info(bank, credit_account, debug_lvl)
            Print_sub_functions.print_account_search_end(order, credit_account, credit_accounts_list, debug_lvl)
            if credit_account_statement.shape[0] == 0:
                empty_df += 1
                continue
            # Мэпим англ и русские колонки
            credit_account_statement = Stars_settings.convert_sql_table_to_acc_statement(credit_account_statement)
            credit_account_statement['Порядковый номер кредитного договора'] = credit_account
            accounts_dict[credit_account] = credit_account_statement
            # второе добавление банковской выписки в dict (с приставкой clear) связано с тем, что:
            # в алгоритме реализован процесс откидывания строк, которые уже ранее были использованы в других транжах
            # (то есть их невозможно затянуть во второй раз следующим проходом алгоритма)
            # Clear версии выписок нужны для их дальнейшей выгрузки в Excel
            accounts_dict[credit_account+'clear'] = credit_account_statement

            # Третий этап: формирование шаблонов output таблиц
            output_table_1, output_table_2 = Settings.init_result_tables()

            # Четвертый этап: фильтрация DataFrame по корсчетам, которые не попадают ни в один из описанных в ТЗ сценариев:
            filtered_file = First_stage.filter_unsuitable_rows(credit_account_statement)
            if filtered_file.shape[0] == 0:
                empty_df += 1
                continue

            # Пятый этап: заполнение первой части output таблицы на основе выписки по ссудному счету
            output_table_1 = First_stage.fill_rows_based_on_credit_account(output_table_1, filtered_file)

            # Шестой этап: создание dict, который включает в себя информацию о движениях полученных средств
            # исходя из описанных сценариев
            output_table_1['dict_column'] = output_table_1.apply(Second_stage.fill_rows_based_on_payment_account,
                                                                 args=(bank, accounts_dict, debug_lvl), axis=1)

            # Седьмой этап: заполнение второй части output таблицы на основе заполненного dict
            order_without_empty_df = order - empty_df + 1
            output_table_1 = Second_stage.fill_rows_from_dict(output_table_1, order_without_empty_df, order_INN,
                                                              bank, accounts_dict, debug_lvl)

            # Восьмой этап: удаление ненужной первой строчки в последующих таблицах
            if len(output_tables) == 0:
                output_tables.append(output_table_1)
            else:
                output_tables.append(output_table_1.iloc[1:])

    # Девятый этап: обьединение всех таблиц по ИНН в одну
    try:
        df = pd.concat(output_tables)
        df = df[df['Направление (Сумма перечисления)'] != 0]
    except ValueError:
        # Если таблиц нет, создаем пустые таблицы, чтобы выдавала пустой результат
        output_table_1, output_table_2 = Settings.init_result_tables()
        df = output_table_1

    # Десятый этап: выгрузка файла в Excel

    helper_functions.load_to_excel(df, accounts_dict, debug_lvl)
