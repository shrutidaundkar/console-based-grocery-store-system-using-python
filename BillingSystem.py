import pymysql


def displayMainMenu():
    print('''

    *****************************Grocery Store(Admin)*****************************
            1. Generate Bill
            2. Manage Inventory
            3. Print receipt
            4. Exit.
    ******************************************************************************
    ''')
    print("Please choose an option numbered 1-4: ")


def displayBillMenu():
    print('''

    *****************************Grocery Store(Bill)******************************
                1. Add item
                2. Update item quantity
                3. Delete item
                4. View all items
                5. Print Bill and go back to main menu
                6. Exit (without saving)
    ******************************************************************************
    ''')
    print("Please choose an option numbered 1-6: ")


def displayInventoryMenu():
    print('''

    *************************Grocery Store(Inventory)******************************
                1. Add item in inventory
                2. Update item quantity in inventory
                3. Delete item in inventory
                4. View all items in inventory
                5. Goto Main menu(exit).
     ******************************************************************************
    ''')
    print("Please choose an option numbered 1-5: ")


def addItemInventory():
    viewAllItemsInventory()
    print("Please enter Item Id")
    itemId = int(input())
    print("Please enter Item Name")
    itemName = input()
    print("Please enter Item Quantity")
    itemQuantity = int(input())
    print("Please enter Item Price")
    itemPrice = float(input())
    sql = "insert into items values(%s,%s,%s,%s)"
    if cursor.execute(sql, (itemId, itemName, itemQuantity, itemPrice)):
        print(itemName, " Item added.")
        connection.commit()
    else:
        print('Item not added!')


def updateItemInventory():
    viewAllItemsInventory()
    print("Enter update item Id")
    itemId = int(input())
    sql = " select * from items where itemId = %s"
    result = cursor.execute(sql, itemId)
    if result > 0:
        print("Enter new quantity of item: ")
        newQuantity = int(input())
        sql = "update items set quantity = %s where itemId = %s"
        if cursor.execute(sql, (newQuantity, itemId)):
            print("Quantity Updated")
            connection.commit()
            viewAllItemsInventory()
        else:
            print("No action performed! ")
    else:
        print("Id NOT present to be updated.")


def getItemAvailableQuantity(itemId):
    sql = " select quantity from items where itemId = %s"
    if cursor.execute(sql, itemId):
        result = cursor.fetchall()
        return result[0][0]
    else:
        return 0


def updateItemQuantity(itemId, itemCount):
    sql = "update items set quantity = %s where itemId = %s"
    if cursor.execute(sql, (itemCount, itemId)):
        print("Quantity updated in inventory")
    else:
        print("Quantity not updated in inventory ")


def deleteItemInventory():
    viewAllItemsInventory()
    print("Enter Id of item to be deleted : ")
    itemId = int(input())
    sql = " select * from items where itemId = %s"
    result = cursor.execute(sql, itemId)
    if result > 0:
        sql = "delete from items where itemId = %s"
        if cursor.execute(sql, itemId):
            print("Item Updated")
            connection.commit()
            viewAllItemsInventory()

        else:
            print("No action performed! ")
    else:
        print("Id NOT present to be deleted.")


def viewAllItemsInventory():
    sql = "select * from items"
    cursor.execute(sql)
    result = cursor.fetchall()
    print("----------------INVENTORY-------------------")
    print("Id      Name           Quantity        Price")
    print("--------------------------------------------")
    for record in result:
        print(record[0], "     ", "{:<10}".format(record[1]), "      ", record[2], "         ", record[3])
    print("--------------------------------------------")


def addItem(billId):
    print("New item to be added")
    viewAllItemsInventory()
    print("Please enter Item Id to be added in cart: ")
    itemId = int(input())
    sql = " select * from items where itemId = %s"
    if cursor.execute(sql, itemId):

        sql = " select quantity from transaction where billId =%s and  itemId = %s"
        if cursor.execute(sql, (billId, itemId)):
            print("Item already present Please update quantity.")
        else:
            print("Please enter Item Quantity: ")
            itemQuantity = int(input())
            if getItemAvailableQuantity(itemId) >= itemQuantity:
                sql = "insert into transaction values(%s,%s,%s)"
                if cursor.execute(sql, (billId, itemId, itemQuantity)):
                    updateItemQuantity(itemId, itemQuantity)
                    print(" Item added in cart....")
                else:
                    print('Item not added!')
            else:
                print('Not sufficient inventory present!')
    else:
        print('Incorrect Item Id!')


def updateItem(billId):
    viewAllItems(billId)
    print("Item id to be updated in the cart: ")
    itemId = int(input())
    sql = " select quantity from transaction where billId =%s and  itemId = %s"
    if cursor.execute(sql, (billId, itemId)):
        result = cursor.fetchall()
        initialCount = result[0][0]
        print("Please enter new quantity for the item: ")
        itemQuantity = int(input())
        if getItemAvailableQuantity(itemId)+initialCount >= itemQuantity:
            updateItemQuantity(itemId, getItemAvailableQuantity(itemId)+initialCount)
            sql = "update transaction set quantity = %s where billId = %s and itemId = %s"

            if cursor.execute(sql, (itemQuantity, billId, itemId)):
                updateItemQuantity(itemId, getItemAvailableQuantity(itemId)-itemQuantity)
                print(" Item quantity updated in cart....")
            else:
                print('Item not updated!')
        else:
            print('Insufficient inventory!')
    else:
        print("Item Id not present!")


def deleteItem(billId):
    viewAllItems(billId)
    print("Item id to be deleted in the cart: ")
    itemId = int(input())

    sql = "delete from transaction where billId = %s and itemId = %s"
    if cursor.execute(sql, (billId, itemId)):
        print(" Item deleted in cart....")
    else:
        print('Item not deleted!')


def viewAllItems(billId):
    sql = "select * from transaction where billId = %s"
    cursor.execute(sql, billId)
    result = cursor.fetchall()
    print("--------------------CART ITEMS: ", billId, "------------------")
    print("Id     Item Name      Quantity      Price    Total")
    print("-------------------------------------------------------")
    for record in result:
        name = getItemName(record[1])
        price = getItemPrice(record[1])
        total = price * record[2]
        print(record[1], "     ", "{:<10}".format(name), "      ", record[2], "       ", price, "    ",
              total, "Rs ")
    print("-------------------------------------------------------")
    print("            Total:", viewTotalAmount(billId), " Rs             ")
    print("-------------------------------------------------------")


def getItemPrice(itemId):
    sql = "select price from items where itemId = %s"
    cursor.execute(sql, itemId)
    result = cursor.fetchall()
    if result:
        return result[0][0]
    else:
        return ""


def getItemName(itemId):
    sql = "select itemName from items where itemId = %s"
    cursor.execute(sql, itemId)
    result = cursor.fetchall()
    if result:
        # print(result[0])
        return result[0][0]
    else:
        return -1


def viewTotalAmount(billId):
    sql = "select * from transaction where billId = %s"
    cursor.execute(sql, billId)
    result = cursor.fetchall()
    totalSum = 0
    for record in result:
        quantity = record[2]
        price = getItemPrice(record[1])
        totalSum = totalSum + (price * quantity)

    return totalSum


def printBill(billId):
    sql = "update bill set totalAmount = %s where billId = %s"
    if cursor.execute(sql, (viewTotalAmount(billId), billId)):
        print(" Transaction Complete.")
        printReceipt(billId)
        connection.commit()
    else:
        print('Bill Amount not updated!')


def printReceipt(billId):
    sql = "select * from bill where billId = %s"
    if cursor.execute(sql, billId):
        result = cursor.fetchall()
        customerName = result[0][1]
        totalBill = result[0][2]
        sql = "select * from transaction where billId = %s"
        if cursor.execute(sql, billId):
            result = cursor.fetchall()
            file = open(str(billId) + 'Bill.txt', 'w')
            file.write("-----------------------------------------------------------\n\n")
            file.write("Bill Id : "+str(billId)+"\t\t\tCustomer Name : "+str(customerName)+"\n\n")
            file.write("------------------------CART-------------------------------\n")
            file.write("Id      Item Name       Quantity       Price     Total \n")
            file.write("-----------------------------------------------------------\n")
            for record in result:
                name = getItemName(record[1])
                price = str(getItemPrice(record[1]))
                total = str(getItemPrice(record[1]) * record[2])
                file.write(str(record[1])+"\t\t"+"{:<10}".format(name)+"\t\t"+str(record[2])+"\t\t\t\t"+price+"\t\t"+total+"Rs \n")
            file.write("------------------------------------------------------------\n")
            file.write("            Total:"+str(viewTotalAmount(billId))+" Rs            \n")
            file.write("------------------------------------------------------------\n")
            file.close()
            print("Receipt Downloaded successfully!")
        else:
            print("No items in cart!")
    else:
        print("Error Occurred!")


def manageInventory():
    inventoryChoice = 1

    while inventoryChoice != 5:
        displayInventoryMenu()
        inventoryChoice = int(input())
        if inventoryChoice == 1:
            addItemInventory()
        elif inventoryChoice == 2:
            updateItemInventory()
        elif inventoryChoice == 3:
            deleteItemInventory()
        elif inventoryChoice == 4:
            viewAllItemsInventory()
        elif inventoryChoice == 5:
            print("Back to main menu")
        else:
            print("Invalid choice")


def revertBill():
    print("Revert")
    connection.rollback()


def generateBill():
    sql = "select billId from bill"
    printAllBillIds()

    print("Please enter Bill Id: ")
    billId = int(input())
    print("Please Customer Name")
    customerName = input()

    billChoice = 1
    sql = "insert into bill values(%s,%s,-1)"

    if cursor.execute(sql, (billId, customerName)):

        while billChoice != 6:
            displayBillMenu()
            billChoice = int(input())
            if billChoice == 1:
                addItem(billId)
            elif billChoice == 2:
                updateItem(billId)
            elif billChoice == 3:
                deleteItem(billId)
            elif billChoice == 4:
                viewAllItems(billId)
            elif billChoice == 5:
                printBill(billId)
                break
            elif billChoice == 6:
                revertBill()
                print("Back to main menu without saving")
            else:
                print("Invalid choice")
        connection.commit()
    else:
        print('Bill not added!')


def printAllBillIds():
    sql = "select * from bill where totalAmount != -1"
    if cursor.execute(sql):
        result = cursor.fetchall()
        print("--------------------Bill History---------------------------")
        print("BillId      Customer Name               Bill Amount        ")
        for record in result:
            print(str(record[0])+"\t\t\t"+str(record[1])+"\t\t\t\t"+str(record[2]))
        print("----------------------------------------------------------")


if __name__ == "__main__":
    connection = pymysql.connect(host="localhost", user="system", password="system", database="training")
    cursor = connection.cursor()
    choice = 0
    while choice != 4:
        displayMainMenu()
        choice = int(input())
        if choice == 1:
            generateBill()
        elif choice == 2:
            manageInventory()
        elif choice == 3:
            bill = int(input("Enter bill Id : "))
            printReceipt(bill)
        elif choice == 4:
            print("Thank you! ")
        else:
            print("Invalid choice!")
    connection.close()
