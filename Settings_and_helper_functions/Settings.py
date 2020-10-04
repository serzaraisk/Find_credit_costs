import pandas as pd


def init_result_tables():
    """Создает шаблоны output таблиц"""
    init_output_table_stage_1 = {'Наименование заемщика': [1],
                                 'ИНН заемщика': [2],
                                 'Номер кредитного договора': [3],
                                 'Дата кредитного договора': [4],
                                 'Валюта кредита': [5],
                                 'Сумма выданных в исследуемом периоде траншей': [6],
                                 'Дата выдачи транша': [7],
                                 'Сумма транша': [8],
                                 'Номер внутреннего корреспондирующего счёта': [9],
                                 'Направление расходования ссудной задолженности': [10],
                                 'Направление (Дата перечисления)': [11],
                                 'Направление (Сумма перечисления)': [12],
                                 'Направление(Название)': [13],
                                 'Направление(ИНН)': [14],
                                 'Направление(Банк)': [15],
                                 'Направление(Номер корреспондирующего счёта)': [16],
                                 'Направление(Назначение платежа)': [17],
                                 'Направление (Целевое назначение)': [18],
                                 'Конечный получатель (Название)': [19],
                                 'Конечный получатель (ИНН)': [20],
                                 'Конечный получатель (Дата перечисления контрагенту)': [21],
                                 'Конечный получатель (Банк)': [22],
                                 'Конечный получатель (Сумма перечисления)': [23],
                                 'Конечный получатель (Назначение платежа)': [24],
                                 'Конечный получатель (Номер счета контрагента)': [25],
                                 'Конечный получатель (Целевое назначение)': [25],
                                 'Комментарий': [26],
                                 }
    init_output_table_stage_2 = {'Контрагент (Наименование)': [1],
                                 'Контрагент (ИНН)': [2],
                                 'Заемщики': [3]
                                 }
    return pd.DataFrame(init_output_table_stage_1), pd.DataFrame(init_output_table_stage_2)


def reorder_columns(ouput_table):
    """Меняет местами колонки в итоговой таблице"""
    order_columns_in_output_table = ['Порядковый № исследуемого ИНН',
                                     'Порядковый номер исследуемого ссудного счета',
                                     'Порядковый № кредитного транжа',
                                     'Порядковый номер первого (после заемщика) получателя средств',
                                     'Порядковый номер конечного получателя средств',
                                     'Наименование заемщика', 'ИНН заемщика', 'Номер кредитного договора',
                                     'Дата кредитного договора', 'Валюта кредита',
                                     'Сумма выданных в исследуемом периоде траншей', 'Дата выдачи транша',
                                     'Сумма транша', 'Номер внутреннего корреспондирующего счёта',
                                     'Направление расходования ссудной задолженности',
                                     'Направление (Дата перечисления)', 'Направление (Сумма перечисления)',
                                     'Направление(Название)', 'Направление(ИНН)', 'Направление(Банк)',
                                     'Направление(Номер корреспондирующего счёта)',
                                     'Направление(Назначение платежа)', 'Направление (Целевое назначение)',
                                     'Конечный получатель (Название)', 'Конечный получатель (ИНН)',
                                     'Конечный получатель (Дата перечисления контрагенту)',
                                     'Конечный получатель (Банк)',
                                     'Конечный получатель (Сумма перечисления)',
                                     'Конечный получатель (Назначение платежа)',
                                     'Конечный получатель (Номер счета контрагента)',
                                     'Конечный получатель (Целевое назначение)', 'Комментарий',
                                     ]
    return ouput_table[order_columns_in_output_table]


# Таблица из Общероссийского классификатора валют
currency_dict = {"008": {"code": "ALL", "name": "Лек"},
                 "012": {"code": "DZD", "name": "Алжирский динар"},
                 "032": {"code": "ARS", "name": "Аргентинское песо"},
                 "036": {"code": "AUD", "name": "Австралийский доллар"},
                 "044": {"code": "BSD", "name": "Багамский доллар"},
                 "048": {"code": "BHD", "name": "Бахрейнский динар"},
                 "050": {"code": "BDT", "name": "Така"},
                 "051": {"code": "AMD", "name": "Армянский драм"},
                 "052": {"code": "BBD", "name": "Барбадосский доллар"},
                 "060": {"code": "BMD", "name": "Бермудский доллар"},
                 "064": {"code": "BTN", "name": "Нгултрум"},
                 "068": {"code": "BOB", "name": "Боливиано"},
                 "072": {"code": "BWP", "name": "Пула"},
                 "084": {"code": "BZD", "name": "Белизский доллар"},
                 "090": {"code": "SBD", "name": "Доллар Соломоновых Островов"},
                 "096": {"code": "BND", "name": "Брунейский доллар"},
                 "104": {"code": "MMK", "name": "Кьят"},
                 "108": {"code": "BIF", "name": "Бурундийский франк"},
                 "116": {"code": "KHR", "name": "Риель"},
                 "124": {"code": "CAD", "name": "Канадский доллар"},
                 "132": {"code": "CVE", "name": "Эскудо Кабо-Верде"},
                 "136": {"code": "KYD", "name": "Доллар Островов Кайман"},
                 "144": {"code": "LKR", "name": "Шри-ланкийская рупия"},
                 "152": {"code": "CLP", "name": "Чилийское песо"},
                 "156": {"code": "CNY", "name": "Юань"},
                 "170": {"code": "COP", "name": "Колумбийское песо"},
                 "174": {"code": "KMF", "name": "Коморский франк"},
                 "188": {"code": "CRC", "name": "Коста-риканский колон"},
                 "191": {"code": "HRK", "name": "Куна"},
                 "192": {"code": "CUP", "name": "Кубинское песо"},
                 "203": {"code": "CZK", "name": "Чешская крона"},
                 "208": {"code": "DKK", "name": "Датская крона"},
                 "214": {"code": "DOP", "name": "Доминиканское песо"},
                 "222": {"code": "SVC", "name": "Сальвадорский колон"},
                 "230": {"code": "ETB", "name": "Эфиопский быр"},
                 "232": {"code": "ERN", "name": "Накфа"},
                 "238": {"code": "FKP", "name": "Фунт Фолклендских островов"},
                 "242": {"code": "FJD", "name": "Доллар Фиджи"},
                 "262": {"code": "DJF", "name": "Франк Джибути"},
                 "270": {"code": "GMD", "name": "Даласи"},
                 "292": {"code": "GIP", "name": "Гибралтарский фунт"},
                 "320": {"code": "GTQ", "name": "Кетсаль"},
                 "324": {"code": "GNF", "name": "Гвинейский франк"},
                 "328": {"code": "GYD", "name": "Гайанский доллар"},
                 "332": {"code": "HTG", "name": "Гурд"},
                 "340": {"code": "HNL", "name": "Лемпира"},
                 "344": {"code": "HKD", "name": "Гонконгский доллар"},
                 "348": {"code": "HUF", "name": "Форинт"},
                 "352": {"code": "ISK", "name": "Исландская крона"},
                 "356": {"code": "INR", "name": "Индийская рупия"},
                 "360": {"code": "IDR", "name": "Рупия"},
                 "364": {"code": "IRR", "name": "Иранский риал"},
                 "368": {"code": "IQD", "name": "Иракский динар"},
                 "376": {"code": "ILS", "name": "Новый израильский шекель"},
                 "388": {"code": "JMD", "name": "Ямайский доллар"},
                 "392": {"code": "JPY", "name": "Иена"},
                 "398": {"code": "KZT", "name": "Тенге"},
                 "400": {"code": "JOD", "name": "Иорданский динар"},
                 "404": {"code": "KES", "name": "Кенийский шиллинг"},
                 "408": {"code": "KPW", "name": "Северокорейская вона"},
                 "410": {"code": "KRW", "name": "Вона"},
                 "414": {"code": "KWD", "name": "Кувейтский динар"},
                 "417": {"code": "KGS", "name": "Сом"},
                 "418": {"code": "LAK", "name": "Лаосский кип"},
                 "422": {"code": "LBP", "name": "Ливанский фунт"},
                 "426": {"code": "LSL", "name": "Лоти"},
                 "430": {"code": "LRD", "name": "Либерийский доллар"},
                 "434": {"code": "LYD", "name": "Ливийский динар"},
                 "446": {"code": "MOP", "name": "Патака"},
                 "454": {"code": "MWK", "name": "Квача"},
                 "458": {"code": "MYR", "name": "Малайзийский ринггит"},
                 "462": {"code": "MVR", "name": "Руфия"},
                 "480": {"code": "MUR", "name": "Маврикийская рупия"},
                 "484": {"code": "MXN", "name": "Мексиканское песо"},
                 "496": {"code": "MNT", "name": "Тугрик"},
                 "498": {"code": "MDL", "name": "Молдавский лей"},
                 "504": {"code": "MAD", "name": "Марокканский дирхам"},
                 "512": {"code": "OMR", "name": "Оманский риал"},
                 "516": {"code": "NAD", "name": "Доллар Намибии"},
                 "524": {"code": "NPR", "name": "Непальская рупия"},
                 "532": {"code": "ANG", "name": "Нидерландский антильский гульден"},
                 "533": {"code": "AWG", "name": "Арубанский флорин"},
                 "548": {"code": "VUV", "name": "Вату"},
                 "554": {"code": "NZD", "name": "Новозеландский доллар"},
                 "558": {"code": "NIO", "name": "Золотая кордоба"},
                 "566": {"code": "NGN", "name": "Найра"},
                 "578": {"code": "NOK", "name": "Норвежская крона"},
                 "586": {"code": "PKR", "name": "Пакистанская рупия"},
                 "590": {"code": "PAB", "name": "Бальбоа"},
                 "598": {"code": "PGK", "name": "Кина"},
                 "600": {"code": "PYG", "name": "Гуарани"},
                 "604": {"code": "PEN", "name": "Соль"},
                 "608": {"code": "PHP", "name": "Филиппинское песо"},
                 "634": {"code": "QAR", "name": "Катарский риал"},
                 "643": {"code": "RUB", "name": "Российский рубль"},
                 "646": {"code": "RWF", "name": "Франк Руанды"},
                 "654": {"code": "SHP", "name": "Фунт Святой Елены"},
                 "682": {"code": "SAR", "name": "Саудовский риял"},
                 "690": {"code": "SCR", "name": "Сейшельская рупия"},
                 "694": {"code": "SLL", "name": "Леоне"},
                 "702": {"code": "SGD", "name": "Сингапурский доллар"},
                 "704": {"code": "VND", "name": "Донг"},
                 "706": {"code": "SOS", "name": "Сомалийский шиллинг"},
                 "710": {"code": "ZAR", "name": "Рэнд"},
                 "728": {"code": "SSP", "name": "Южносуданский фунт"},
                 "748": {"code": "SZL", "name": "Лилангени"},
                 "752": {"code": "SEK", "name": "Шведская крона"},
                 "756": {"code": "CHF", "name": "Швейцарский франк"},
                 "760": {"code": "SYP", "name": "Сирийский фунт"},
                 "764": {"code": "THB", "name": "Бат"},
                 "776": {"code": "TOP", "name": "Паанга"},
                 "780": {"code": "TTD", "name": "Доллар Тринидада и Тобаго"},
                 "784": {"code": "AED", "name": "Дирхам (ОАЭ)"},
                 "788": {"code": "TND", "name": "Тунисский динар"},
                 "800": {"code": "UGX", "name": "Угандийский шиллинг"},
                 "807": {"code": "MKD", "name": "Денар"},
                 "810": {"code": "RUB", "name": "Российский рубль"},
                 "818": {"code": "EGP", "name": "Египетский фунт"},
                 "826": {"code": "GBP", "name": "Фунт стерлингов"},
                 "834": {"code": "TZS", "name": "Танзанийский шиллинг"},
                 "840": {"code": "USD", "name": "Доллар США"},
                 "858": {"code": "UYU", "name": "Уругвайское песо"},
                 "860": {"code": "UZS", "name": "Узбекский сум"},
                 "882": {"code": "WST", "name": "Тала"},
                 "886": {"code": "YER", "name": "Йеменский риал"},
                 "901": {"code": "TWD", "name": "Новый тайваньский доллар"},
                 "928": {"code": "VES", "name": "Боливар Соберано"},
                 "929": {"code": "MRU", "name": "Угия"},
                 "930": {"code": "STN", "name": "Добра"},
                 "931": {"code": "CUC", "name": "Конвертируемое песо"},
                 "932": {"code": "ZWL", "name": "Доллар Зимбабве"},
                 "933": {"code": "BYN", "name": "Белорусский рубль"},
                 "934": {"code": "TMT", "name": "Новый туркменский манат"},
                 "936": {"code": "GHS", "name": "Ганский седи"},
                 "937": {"code": "VEF", "name": "Боливар"},
                 "938": {"code": "SDG", "name": "Суданский фунт"},
                 "940": {"code": "UYI", "name": "Уругвайское песо в индексированных единицах"},
                 "941": {"code": "RSD", "name": "Сербский динар"},
                 "943": {"code": "MZN", "name": "Мозамбикский метикал"},
                 "944": {"code": "AZN", "name": "Азербайджанский манат"},
                 "946": {"code": "RON", "name": "Румынский лей"},
                 "949": {"code": "TRY", "name": "Турецкая лира"},
                 "950": {"code": "XAF", "name": "Франк КФА ВЕАС"},
                 "951": {"code": "XCD", "name": "Восточно-карибский доллар"},
                 "952": {"code": "XOF", "name": "Франк КФА ВСЕАО"},
                 "953": {"code": "XPF", "name": "Франк КФП"},
                 "960": {"code": "XDR", "name": "СДР (специальные права заимствования)"},
                 "967": {"code": "ZMW", "name": "Замбийская квача"},
                 "968": {"code": "SRD", "name": "Суринамский доллар"},
                 "969": {"code": "MGA", "name": "Малагасийский ариари"},
                 "970": {"code": "COU", "name": "Единица реальной стоимости"},
                 "971": {"code": "AFN", "name": "Афгани"},
                 "972": {"code": "TJS", "name": "Сомони"},
                 "973": {"code": "AOA", "name": "Кванза"},
                 "974": {"code": "BYR", "name": "Белорусский рубль"},
                 "975": {"code": "BGN", "name": "Болгарский лев"},
                 "976": {"code": "CDF", "name": "Конголезский франк"},
                 "977": {"code": "ВАМ", "name": "Конвертируемая марка"},
                 "978": {"code": "EUR", "name": "Евро"},
                 "980": {"code": "UAH", "name": "Гривна"},
                 "981": {"code": "GEL", "name": "Лари"},
                 "985": {"code": "PLN", "name": "Злотый"},
                 "986": {"code": "BRL", "name": "Бразильский реал"}}
