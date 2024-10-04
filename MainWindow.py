from tkinter import *
from DatabaseConnection.databaseConnection import Connect

sql = Connect()
root = Tk()
root.title("SQL Select Statement Creation")

buttonWidth = 10

def tablesDisplay(listbox, scrollbar):
    databaseTables.grid_forget()
    databaseScrollbar.grid_forget()
    tableColumns.grid_forget()
    tableColumnScroll.grid_forget()
    filterResults.grid_forget()
    filterScroll.grid_forget()
    filterQuery.grid_forget()
    listbox.grid(column=0, row=0, sticky='ewns')
    scrollbar.grid(column=1, row=0, stick='ns')
    tableNames = databaseTables.get(databaseTables.curselection())
    columns = []
    for i in tableColumns.curselection():
        columns.append(tableColumns.get(i))
    statement = ('SELECT {columnNames} FROM {tableNames} WHERE '.
                 format(
                     tableNames = tableNames,
                     columnNames = ', '.join(columns),
                    )
                 )
    sqlStatementBuilder.set(statement)

def columnData():
    tableColumns.delete(0, END)
    addColumnData = sql.runQuery("SELECT owner, column_name FROM all_tab_columns WHERE table_name = '{table}'".format(table = databaseTables.get(databaseTables.curselection())))
    for columnName in addColumnData:
        tableColumns.insert(END, columnName[1]) 

def filterData():
    filterResults.delete(0, END)
    filterQuery.insert(END, "Delete this text and enter your search criteria here")
    filterQuery.grid(row=1, sticky='ew')
    for i in tableColumns.curselection():
        filterResults.insert(END, tableColumns.get(i))

def runQuery():
    tableNames = databaseTables.get(databaseTables.curselection())
    columns = []
    for i in tableColumns.curselection():
        columns.append(tableColumns.get(i))
    statement = ('SELECT {columnNames} FROM {tableNames} WHERE {filter} = \'{searchValue}\''.
                 format(
                     tableNames = tableNames,
                     columnNames = ', '.join(columns),
                     filter = filterResults.get(filterResults.curselection()),
                     searchValue = filterQuery.get()
                    )
                 )
    sqlStatementBuilder.set(statement)
    tupleColumns = tuple(columns)
    results = sql.runQuery(sqlStatement.get())
    results.insert(0, tupleColumns)
    for row in results:
        resultText.insert(END, str(row) + "\n")

buttonFrame = Frame(root, highlightbackground="black", highlightthickness=2)
tablesButton = Button(buttonFrame, text="Tables", width=buttonWidth, command=lambda: tablesDisplay(databaseTables, databaseScrollbar)).grid(column=0, row=0)
columnsButton = Button(buttonFrame, text="Columns", width=buttonWidth, command=lambda: [tablesDisplay(tableColumns, tableColumnScroll), columnData()]).grid(column=0, row=1)
filterButton = Button(buttonFrame, text="Filter Results", width=buttonWidth, command=lambda: [tablesDisplay(filterResults, filterScroll), filterData()]).grid(column=0, row=2)
runQueryButton = Button(buttonFrame, text="Run Query", width=buttonWidth, command=lambda: runQuery()).grid(column=0, row=3)
buttonFrame.grid(column=0, row=0, sticky='ns')

dataFrame = Frame(root, highlightbackground="black", highlightthickness=2)

databaseTables = Listbox(dataFrame, selectmode="single", exportselection=0)
databaseScrollbar = Scrollbar(dataFrame, orient=VERTICAL)
tablesAvailable = sql.runQuery("SELECT owner, table_name FROM all_tables WHERE owner != 'SYS' UNION SELECT owner, view_name FROM all_views WHERE owner != 'SYS' ORDER BY table_name")
for each_item in tablesAvailable: databaseTables.insert(END, each_item[1])
databaseTables.config(yscrollcommand=databaseScrollbar.set)
databaseScrollbar.config(command=databaseTables.yview)
databaseTables.grid(column=0, row=0, sticky='ewns')
databaseScrollbar.grid(column=1, row=0, sticky='ns')
dataFrame.rowconfigure(0, weight=1)
dataFrame.columnconfigure(0, weight=1)


tableColumns = Listbox(dataFrame, selectmode="multiple", exportselection=0)
tableColumnScroll = Scrollbar(dataFrame, orient=VERTICAL)
tableColumns.config(yscrollcommand=tableColumnScroll.set)
tableColumnScroll.config(command=tableColumns.yview)


filterResults = Listbox(dataFrame, selectmode="single", exportselection=0)
filterScroll = Scrollbar(dataFrame, orient=VERTICAL)
filterResults.config(yscrollcommand=filterScroll.set)
filterScroll.config(command=filterResults.yview)

filterQuery = Entry(dataFrame, text="Hello World!")

dataFrame.grid(column=1, row=0, sticky='nsew')

sqlFrame = Frame(root, highlightbackground="black", highlightthickness=2)
sqlStatementBuilder = StringVar(sqlFrame, value='Select a Table you want to query and click the Columns button to move to the next step.')
sqlStatement = Entry(sqlFrame, textvariable=sqlStatementBuilder)
sqlStatement.grid(row=0, column=0, sticky='nsew')

sqlTableFrame = Frame(sqlFrame)

resultText = Text(sqlTableFrame, height=8) 
resultScroll = Scrollbar(sqlTableFrame) 
resultText.configure(yscrollcommand=resultScroll.set) 
resultText.grid(row=0, column=0, sticky='nsew') 
resultScroll.config(command=resultText.yview) 
resultScroll.grid(row=0, column=1, sticky='ns')

sqlTableFrame.columnconfigure(0, weight=1)
sqlTableFrame.rowconfigure(0, weight=1)

sqlTableFrame.grid(row=1, column=0, sticky='nsew')

sqlFrame.rowconfigure(0, weight=1)
sqlFrame.columnconfigure(0, weight=1)
sqlFrame.grid(columnspan=2, row=1, sticky='nsew')

root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()