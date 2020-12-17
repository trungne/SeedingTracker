MAX_COLUMN_RANGE = 10
DEFAULT_PAD_Y = 4


def show_widgets_in_consecutive_grids(list_of_widgets, row=0):
    total_rows = len(list_of_widgets) + row

    index = 0
    for each_row in range(row, total_rows):
        if type(list_of_widgets[index]) == list: # if an item is a list
            for i in range(len(list_of_widgets[index])): # display the list in ONE ROW
                list_of_widgets[index][i].grid(row=each_row, sticky="nsew", column=i, pady=DEFAULT_PAD_Y)
        
        elif type(list_of_widgets[index]).__name__ == "Reaction":
            list_of_widgets[index].display_reaction(each_row)
        # sticky="nsew"
        else:
            list_of_widgets[index].grid(row=each_row, sticky="nsew", columnspan=MAX_COLUMN_RANGE, pady=DEFAULT_PAD_Y)
        index += 1
    return total_rows + row


def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True