# Модуль включает в себя настройку формата ячеек для финальной выгрузки данных в excel
def cell_format_for_header_blue(workbook):
    cell_format_header = workbook.add_format()
    cell_format_header.set_text_wrap()
    cell_format_header.set_font_color('#FFFFFF')
    cell_format_header.set_bg_color('#00338D')
    cell_format_header.set_bottom()
    cell_format_header.set_top()
    cell_format_header.set_left()
    cell_format_header.set_right()
    cell_format_header.set_align('center')
    cell_format_header.set_align('vcenter')
    cell_format_header.set_bold()
    return cell_format_header


def cell_format_for_header_medium_blue(workbook):
    cell_format_header = workbook.add_format()
    cell_format_header.set_text_wrap()
    cell_format_header.set_font_color('#FFFFFF')
    cell_format_header.set_bg_color('#005EB8')
    cell_format_header.set_bottom()
    cell_format_header.set_top()
    cell_format_header.set_left()
    cell_format_header.set_right()
    cell_format_header.set_align('center')
    cell_format_header.set_align('vcenter')
    cell_format_header.set_bold()
    return cell_format_header


def cell_format_for_header_purple(workbook):
    cell_format_header = workbook.add_format()
    cell_format_header.set_text_wrap()
    cell_format_header.set_font_color('#FFFFFF')
    cell_format_header.set_bg_color('#6D2077')
    cell_format_header.set_bottom()
    cell_format_header.set_top()
    cell_format_header.set_left()
    cell_format_header.set_right()
    cell_format_header.set_align('center')
    cell_format_header.set_align('vcenter')
    cell_format_header.set_bold()
    return cell_format_header


def cell_format_for_header_green(workbook):
    cell_format_header = workbook.add_format()
    cell_format_header.set_text_wrap()
    cell_format_header.set_font_color('#FFFFFF')
    cell_format_header.set_bg_color('#00A3A1')
    cell_format_header.set_bottom()
    cell_format_header.set_top()
    cell_format_header.set_left()
    cell_format_header.set_right()
    cell_format_header.set_align('center')
    cell_format_header.set_align('vcenter')
    cell_format_header.set_bold()
    return cell_format_header


def cell_format_for_second_row(workbook):
    cell_format_second_row = workbook.add_format()
    cell_format_second_row.set_font_color('#000000')
    cell_format_second_row.set_bg_color('#DCDCDC')
    cell_format_second_row.set_italic()
    cell_format_second_row.set_align('center')
    return cell_format_second_row


def cell_format_main(workbook):
    cell_format = workbook.add_format()
    cell_format.set_font_color('#051141')
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    return cell_format


def cell_format_for_numeric(workbook):
    cell_format_numeric = workbook.add_format()
    cell_format_numeric.set_font_color('#051141')
    cell_format_numeric.set_num_format('#,##0')
    cell_format_numeric.set_align('center')
    cell_format_numeric.set_align('vcenter')
    return cell_format_numeric


def cell_format_for_date(workbook):
    cell_format = workbook.add_format()
    cell_format.set_font_color('#051141')
    cell_format.set_num_format('m/d/yyyy')
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    return cell_format
