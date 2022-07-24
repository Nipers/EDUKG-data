import xlrd

def cell_background_is_yellow ( workbook, cell ):
    # Returns TRUE if the given cell from the given workbook has a yellow RGB (255,255,0) background.
    # Note that the workbook must be opened with formatting_info = True, i.e.
    #     xlrd.open_workbook(xls_filename, formatting_info=True)
    assert type (cell) is xlrd.sheet.Cell
    assert type (workbook) is xlrd.book.Book

    xf_index = cell.xf_index
    print(xf_index)
    # test.append(xf_index)
    if xf_index != None:
        xf_style = workbook.xf_list[xf_index]
        xf_background = xf_style.background

        fill_pattern = xf_background.fill_pattern
        pattern_colour_index = xf_background.pattern_colour_index
        background_colour_index = xf_background.background_colour_index

        pattern_colour = workbook.colour_map[pattern_colour_index]
        background_colour = workbook.colour_map[background_colour_index]
        print(pattern_colour)
        print(background_colour)
        # If the cell has a solid cyan background, then:
        #  - fill_pattern will be 0x01
        #  - pattern_colour will be cyan (0,255,255)
        #  - background_colour is not used with fill pattern 0x01. (undefined value)
        #    So despite the name, for a solid fill, the background colour is not actually the background colour.
        # Refer https://www.openoffice.org/sc/excelfileformat.pdf S. 2.5.12 'Patterns for Cell and Chart Background Area'
    #     if fill_pattern == 0x01 and pattern_colour == (255,255,0):
    #         return True
    # return False

filename="./population/6/A0101a.xls"#读取excel
book = xlrd.open_workbook(filename, formatting_info=True)
name = book.sheet_names()[0]
sheet = book.sheet_by_name(name)
rows = sheet.nrows
# print(sheet.cell_value(0, 0))
for i in range(rows):
    xfx = sheet.cell_xf_index(i, 0)
    xf = book.xf_list[xfx]
    print(xf.background.pattern_colour_index)
    # cell_background_is_yellow(book, sheet.cell(i,1))
