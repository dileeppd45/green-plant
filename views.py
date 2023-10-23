

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from . import views
from textblob import TextBlob


def logout(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id= '" + userid+ "' AND password = '" + password+ "'")
        admin = cursor.fetchone()
        if admin== None:
            cursor.execute("select * from user_register where user_id= '" + userid+ "' AND password = '" + password+ "'")
            user= cursor.fetchone()
            if user == None:
                messages.error(request, 'Error: Invalid UserId Or Password!!')
                return render(request, "login.html")
            else:
                request.session["userId"] = userid
                cursor.execute("select * from category")
                cdata = cursor.fetchall()
                return render(request, "user_home.html", {'cdata': cdata})
            
        else:
            return redirect("admin_home")

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        user_id = request.POST['name']

        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        pin = request.POST['pincode']

        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id= '" + user_id + "' ")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute(
                "select * from user_register where user_id= '" + user_id + "'")
            user = cursor.fetchone()
            if user == None:
                cursor.execute("insert into user_register values('" + user_id + "','" + str(name) + "','" + str(address) + "','" + str(email) + "','" + str(phone) + "','" + str(pin) + "','" + str(password) + "')")
                return redirect("login")
            else:
                messages.info(request, "User Name already exists")
                return render(request, "invalidsign_up.html")
        else:
            messages.info(request, "User Name already exists")
            return render(request, "invalidsign_up.html")
    else:
        return render(request,"sign_up.html")


def admin_home(request):
    cursor = connection.cursor()
    cursor.execute("select * from order_master where payment_status='yes' and delivery_status='pending' ")
    cdata = cursor.fetchall()
    return render(request, "admin_home.html",  {'cdata': cdata})

def approved_carts(request):
    cursor=connection.cursor()
    cursor.execute("select * from order_master where payment_status='yes' and delivery_status='approved' ")
    cdata = cursor.fetchall()
    return render(request, "approved_orders.html", {'cdata': cdata})

def view_all_plant(request):#admin view
    cursor = connection.cursor()
    cursor.execute("select * from category")
    cdata = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("select * from plants")
    pdata=cursor.fetchall()
    return render(request, "view_all_plant.html", {'cdata': cdata, 'data': pdata})

def edit_plant_link(request, id):#admin view
    request.session['cid'] = id
    cursor = connection.cursor()
    cursor.execute("select * from plants where idplants='" + str(id) + "' ")
    data = cursor.fetchone()
    return render(request, "edit_plant.html", {'data': data})

def register_category_link(request):#admin view
    return render(request, "register_category.html")

def register_category(request):#admin view
    if request.method == "POST":
        name = request.POST['txtName']
        cursor = connection.cursor()
        messages.info(request, "green_plant")
        cursor.execute("insert into category values(null,'" + name + "')")
        return redirect("view_all_category")
    else:
        messages.info(request, "Error Adding")

def view_all_category(request):#admin view
    cursor = connection.cursor()
    cursor.execute("select * from category")
    cdata = cursor.fetchall()
    l = list(cdata)
    length = len(l)
    if length == 0:
        val = "categories"
        return render(request, "ano_carts.html", {'val': val})

    return render(request, "view_all_category.html", {'cdata': cdata})

def edit_category_link(request, id):#admin view
    request.session['cid'] = id
    cursor = connection.cursor()
    cursor.execute("select * from category where idcategory='" + str(id) + "' ")
    data = cursor.fetchone()
    return render(request, "edit_category.html", {'data': data})



def update_category(request):#admin view
    cursor = connection.cursor()
    name = request.POST['txtName']
    bid=request.session['cid']
    cursor.execute("update category set name='"+name+"' where idcategory= '" + str(bid) + "' ")
    return redirect('view_all_category')

def register_item(request, id):
    return render(request, "register_item.html",{"id":id})

def plant_add(request):#admin view
    if request.method == "POST":
        cid = request.POST['cid']
        name = request.POST['txtname']
        description = request.POST['txtdes']
        price = request.POST['txtprice']
        image_url=request.POST['imgurl']
        status= request.POST['txtstatus']
        cursor = connection.cursor()
        cursor.execute("insert into plants values(null,'" + cid + "', '" + name + "','" + description + "','" + price + "','" + image_url + "','" + status + "')")
        cursor = connection.cursor()
        cursor.execute("select * from plants where idcategory ='"+ cid +"' ")
        data = cursor.fetchall()
        return render(request, "view_all_plant.html", {'data': data})
    else:
        messages.info(request, "Error Adding")

def admin_pending_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback where reply = 'pending' ")
    table = cursor.fetchall()
    table0 = list(table)
    length = len(table0)
    if length == 0:
        val = "feedback"
        return render(request, "ano_carts.html", {"val": val})
    else:
        return render(request, "admin_pending_fb.html", {"table": table})

def admin_replied_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback where reply != 'pending' ")
    table = cursor.fetchall()
    table0 = list(table)
    length = len(table0)
    if length == 0:
        val = "replys"
        return render(request, "ano_carts.html", {"val": val})
    else:
        return render(request, "admin_replied_fb.html", {"table": table})


def view_orders(request, id):
    cursor = connection.cursor()
    cursor.execute("select  plants.idplants, plants.name, plants.image_url, plants.price, order_items.idorder_items, order_items.idplants, order_items.quantity, order_items.total, order_items.idorder_items, order_master.total_amount,order_master.idorder_master from order_items join plants join order_master ON order_items.idplants = plants.idplants and order_master.idorder_master = order_items.idorder_master where order_master.idorder_master='" + str(id) + "' AND payment_status= 'yes' ")
    table = cursor.fetchall()
    table0 = list(table)
    table0 = list(table0[0])
    total_amount = table0[9]
    idmaster = table0[10]
    print(idmaster)
    return render(request, "admin_cart.html", {"cart": table, "ta": total_amount, "idmaster": idmaster})

def view_approved_orders(request, id):
    cursor = connection.cursor()
    cursor.execute("select  plants.idplants, plants.name, plants.image_url, plants.price, order_items.idorder_items, order_items.idplants, order_items.quantity, order_items.total, order_items.idorder_items, order_master.total_amount,order_master.idorder_master from order_items join plants join order_master ON order_items.idplants = plants.idplants and order_master.idorder_master = order_items.idorder_master where order_master.idorder_master='" + str(id) + "' AND payment_status= 'yes' and delivery_status='approved' ")
    table = cursor.fetchall()
    table0 = list(table)
    table0 = list(table0[0])
    total_amount = table0[9]
    idmaster = table0[10]

    return render(request, "admin_approved_cart.html", {"cart": table, "ta": total_amount, "idmaster": idmaster})

def approve_order(request,id):
    cursor=connection.cursor()
    cursor.execute("update order_master set delivery_status='approved' where idorder_master='" + str(id) + "'")
    messages.info(request, "Delevered Succesfully")
    return redirect('admin_home')

def user_home(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    cdata = cursor.fetchall()
    return render(request, "user_home.html", {'cdata': cdata})

def view_cat(request):
    cursor = connection.cursor() 
    cursor.execute("select * from category")
    cdata = cursor.fetchall()
    return render(request, "user_home.html", {'cdata': cdata})







def view_cart(request):
    user= str(request.session["userId"])
    cursor=connection.cursor()
    cursor.execute("select  plants.idplants, plants.name, plants.image_url, plants.price, order_items.idorder_items, order_items.idplants, order_items.quantity, order_items.total, order_items.idorder_items, order_master.total_amount,order_master.idorder_master,plants.description from order_items join plants join order_master ON order_items.idplants = plants.idplants and order_master.idorder_master = order_items.idorder_master where order_master.user_id='"+user+"' AND payment_status= 'no' ")
    table=cursor.fetchall()
    table0 = list(table)
    length = len(table0)
    if length==0:
        val="cart"
        messages.info(request, "No Items Added Yet")
        # Error Message will be showed as Toast
        return render(request,"no_carts.html",{"val":val})

    else:
        table0=list(table0[0])
        print(table0)
        total_amount=table0[9]
        idmaster=table0[10]
        request.session["idmaster"]=idmaster
        print(idmaster)
        return render(request, "cart.html", {"cart":table,"ta":total_amount,"idmaster":idmaster})

def feedback(request):
    ser = str(request.session["userId"])
    return render(request, "feedback.html", {"user":ser})
def sendfb(request):
    cursor = connection.cursor()
    if request.method == "POST":
        fbdetails = request.POST['fbdetails']
        user=str(request.session["userId"])
        cursor.execute("insert into feedback values( null,'" + str(user) + "',curdate(), '" + str(fbdetails) + "', 'pending' )")
        messages.info(request, "done")
        feedback = fbdetails
        # print text
        print(feedback)
        obj = TextBlob(feedback)
        # returns the sentiment of text
        # by returning a value between -1.0 and 1.0
        sentiment = obj.sentiment.polarity
        print(sentiment)
        if sentiment == 0:
            print('The text is neutral')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk ")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,0,0,1)")
            else:
                cursor = connection.cursor()
                cursor.execute(
                    "update feedback_nltk set neutral_count=neutral_count+1 ")
        elif sentiment > 0:
            print('The text is positive')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,1,0,0)")
            else:
                cursor = connection.cursor()
                cursor.execute("update feedback_nltk set positive_count=positive_count+1 ")
        else:
            print('The text is negative')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk  ")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,0,1,0)")
            else:
                cursor = connection.cursor()
                cursor.execute("update review_nltk set negative_count=negative_count+1  ")

        return redirect("view_fb")

def view_fb(request):
    ser = str(request.session["userId"])
    cursor=connection.cursor()
    cursor.execute("select * from feedback where user_id='"+ser+"' ")
    table=cursor.fetchall()
    table0 = list(table)
    length = len(table0)
    if length == 0:
        val="feedback"
        return render(request,"no_carts.html",{"val":val})
    else:
        return render(request,"view_fb.html",{"table":table})

def reply_fb(request, id):
    request.session["fbId"]=id
    cursor=connection.cursor()
    cursor.execute("select * from feedback where idfeedback ='"+ str(id)+"'")
    row=cursor.fetchone()
    return render(request, "reply_form.html", {"data": row})
def edit_reply_fb(request, id):
    request.session["efbId"]=id
    cursor=connection.cursor()
    cursor.execute("select * from feedback where idfeedback ='"+str(id)+"' ")
    row=cursor.fetchone()
    return render(request, "edit_reply_form.html", {"data": row})
def reply_submit(request):
    ser = request.session["fbId"]
    if request.method == "POST":
        reply = request.POST['reply']
        cursor =connection.cursor()
        cursor.execute(" update feedback set reply='"+str(reply)+"' where idfeedback='"+str(ser)+"' ")
        return redirect(admin_pending_feedback)


def edit_reply_submit(request):
    ser = request.session["fbId"]
    if request.method == "POST":
        reply = request.POST['reply']
        cursor =connection.cursor()
        cursor.execute(" update feedback set reply='"+str(reply)+"' where idfeedback='"+str(ser)+"' ")
        return redirect(admin_replied_feedback)

def all_carts(request):#optional
    
    cursor=connection.cursor()
    cursor.execute("select  plants.idplants, plants.name, plants.image_url, plants.price, order_items.idorder_items, order_items.idplants, order_items.quantity, order_items.total, order_items.idorder_items, order_master.total_amount,order_master.idorder_master,order_master.user_id from order_items join plants join order_master ON order_items.idplants = plants.idplants and order_master.idorder_master = order_items.idorder_master where payment_status= 'yes' ")
    table=cursor.fetchall()
    table0=list(table)
    # table0=list(table0[0])
    ta=0
    for i in table0:
        print(i[7])
        ta=int(i[7])+ta
    total_amount=ta
    return render(request, "all_cart.html", {"cart":table,"ta":total_amount} )


def delete_cart_item(request, id):

        idmaster=request.session["idmaster"]
        cursor=connection.cursor()
        cursor.execute("delete from order_items where idorder_items='"+str(id)+"' ")
        cursor.execute("select total from order_items where idorder_master= '" + str(idmaster) + "'")
        totalrow=cursor.fetchall()
        totallist=list(totalrow)
        print(totallist)
        v=int(0)
        for i in totallist:
            print(i[0])
            v=v+int(i[0])
        cursor.execute("update order_master set total_amount ='"+ str(v) +"' where idorder_master = '" + str(idmaster) + "' ")
        return redirect('view_cart')

def edit_cart_item(request, id):
    idmaster = request.session["idmaster"]
    cursor=connection.cursor()
    cursor.execute("select idplants, quantity from order_items where idorder_items= '" + str(id) + "'")
    pid=cursor.fetchone()
    pid=list(pid)
    quantity=pid[1]
    pid=pid[0]

    cursor.execute("select * from plants where idplants= '"+pid+"'")
    data=cursor.fetchone()
    return render(request, "edit_cart_item.html", {'pid': pid,'quantity': quantity, 'data':data})

def update_cart_item(request):
    cursor=connection.cursor()
    pid=request.POST['pid']
    price=int(request.POST['price']) # prise of item
    quantity=int(request.POST['quantity']) #quantity of item
    total=int(quantity*price) #total amount of item
    user= str(request.session["userId"])
    cursor.execute(" select idorder_master from order_master where user_id ='" + str(user) +"'  AND payment_status = 'no' ")

    idmastercolumn=cursor.fetchone() #get idorder_master from ordermaster which inserted above
    idmaster=list(idmastercolumn)

    cursor.execute(" select * from order_items where idorder_master ='" + str(idmaster[0]) + "' AND idplants= '" + str(pid) +"' " )
    odata=cursor.fetchone()
    
    cursor.execute("update order_items set quantity ='"+ str(quantity) +"' where idplants = '" + str(pid) + "' ")
                
    cursor.execute("update order_items set total ='"+ str(total) +"' where idplants = '" + str(pid) + "' ")

                
    cursor.execute("select total from order_items where idorder_master= '" + str(idmaster[0]) + "'")
    totalrow=cursor.fetchall()
    totallist=list(totalrow)
    print(totallist)
    v=int(0)
    for i in totallist:                
        v=v+int(i[0])        
    cursor.execute("update order_master set total_amount ='"+ str(v) +"' where idorder_master = '" + str(idmaster[0]) + "' ")
    return redirect('view_cart')

def pay_card_gateway(request,id):
    request.session["gateidmaster"]=id
    return render(request, "card_gateway.html")

def card_verify(request):
    id=request.session["gateidmaster"]
    if request.method == "POST":
        card_name = request.POST['card_name']
        card_num = request.POST['card_num']
        cvv = request.POST['cvv']
        exp = "11/11/2025"
        cursor = connection.cursor()
        cursor.execute("select * from account where card_no = '" + str(card_num) + "' and cvv = '" + str(cvv) + "' and expiry_date = '" + str(exp) + "' and name = '" + str(card_name) + "'")
        admin = cursor.fetchone()
        if admin == None:
            messages.info(request, "entered values are incorrect. please try again..")
            return redirect('view_cart')
        else:
            cursor=connection.cursor()
            cursor.execute("update order_master set payment_status='yes' where idorder_master='"+str(id)+"'")
            messages.info(request, "payed succesfully")
            return redirect('user_home')

def database(request):#admin view
    cursor=connection.cursor()
    cursor.execute(" select * from order_master ")
    ordermaster=cursor.fetchall() 
    
    
    cursor.execute(" select * from order_items ")
    orderitems=cursor.fetchall() 

    
    cursor.execute(" select * from category ")
    cat=cursor.fetchall()

    
    cursor.execute(" select * from plants ")
    plant=cursor.fetchall()

    
    cursor.execute(" select * from user_register ")
    user=cursor.fetchall()

    
    cursor.execute(" select * from login ")
    admin=cursor.fetchall()

    return render(request, "database.html ",{"order_master":ordermaster,"order_items":orderitems,"category":cat, "plants":plant, "user":user,"admin":admin})



def user_register_link(request):
    return render(request, "signup")

def user_register(request):
    return render(request, "signup")






def delete_category(request, id):#admin view
    cursor = connection.cursor()
    cursor.execute("delete from category where idcategory= '" + str(id) + "' ")
    return redirect('view_all_category')

def delete_plant(request, id):#admin view
    cursor = connection.cursor()
    cursor.execute("delete from plants where idplants= '" + str(id) + "' ")
    return redirect('view_all_plant')



def update_plant(request):#admin view
    cursor = connection.cursor()
    name = request.POST['pname']
    bid=request.session['cid']
    description = request.POST['discription']
    price = request.POST['prise']
    image = request.POST['image']
    status = request.POST['status']
    cursor.execute("update plants set name='"+name+"' where idplants= '" + str(bid) + "' ")
    cursor.execute("update plants set description='"+description+"' where idplants= '" + str(bid) + "' ")
    cursor.execute("update plants set price='"+price+"' where idplants= '" + str(bid) + "' ")
    cursor.execute("update plants set image_url='"+image+"' where idplants= '" + str(bid) + "' ")
    cursor.execute("update plants set status='"+status+"' where idplants= '" + str(bid) + "' ")
    return redirect('view_all_plant')



def my_orders(request):
    user=str(request.session["userId"])
    cursor=connection.cursor()
    cursor.execute("select * from order_master where user_id='"+user+"' and payment_status ='yes' and delivery_status='approved' ")
    data=cursor.fetchall()
    cursor.execute("select * from order_master where user_id='" + user + "' and payment_status ='yes' and delivery_status='pending' ")
    mata = cursor.fetchall()
    return render(request, "user_orders.html",{'cdata':data,'mata':mata})

def user_approved_orders(request, id):
    cursor = connection.cursor()
    cursor.execute("select  plants.idplants, plants.name, plants.image_url, plants.price, order_items.idorder_items, order_items.idplants, order_items.quantity, order_items.total, order_items.idorder_items, order_master.total_amount,order_master.idorder_master from order_items join plants join order_master ON order_items.idplants = plants.idplants and order_master.idorder_master = order_items.idorder_master where order_master.idorder_master='" + str(id) + "' AND payment_status= 'yes' and delivery_status='approved' ")
    table = cursor.fetchall()
    table0 = list(table)
    table0 = list(table0[0])
    total_amount = table0[9]
    idmaster = table0[10]
    print(idmaster)
    return render(request, "user_approved_cart.html", {"cart": table, "ta": total_amount, "idmaster": idmaster})


#.......


def view_items(request, id):  # admin view

    cursor = connection.cursor()
    cursor.execute("select * from plants where idcategory='" + str(id) + "' ")
    data = cursor.fetchall()
    l = list(data)
    length = len(l)
    if length == 0:
        val = "plants"
        return render(request, "no_carts.html", {'val': val})
    else:
        return render(request, "view_items.html ", {"data": data})


def addcart(request, itemid):
    user = str(request.session["userId"])

    if request.method == "POST":
        catid = request.POST['catid']
        pid = request.POST['pid']  # id of item

        prise = int(request.POST['prise'])  # prise of item
        quantity = int(request.POST['quantity'])  # quantity of item
        total = int(quantity * prise)  # total amount of item
        del_status = "pending"
        pay_status_no = "no"

        cursor = connection.cursor()
        cursor.execute("select * from order_master where user_id='" + str(user) + "' ")
        data = cursor.fetchone()  # get all rows of userid =id

        cursor.execute("select * from order_master where user_id='" + str(user) + "' AND payment_status = '" + pay_status_no + "'  ")
        datanotpayed = cursor.fetchone()  # get a row of userid=id and paystatus =no

        if data == None:  # if there is no row of userid =id
            total_amount = int(0)
            cursor.execute("insert into order_master values(null,'" + str(user) + "', curdate(), '" + str(total_amount) + "', '" + del_status + "', '" + pay_status_no + "' ) ")  # inserting added items datas to order_master

            cursor.execute(" select idorder_master from order_master where user_id='" + str(user) + "' ")
            idmastercolumn = cursor.fetchone()  # get idorder_master from ordermaster which inserted above
            idmaster = list(idmastercolumn)

            cursor.execute("insert into order_items values( null,  '" + str(idmaster[0]) + "' ,'" + pid + "', '" + str(quantity) + "', '" + str(total) + "') ")

            ta = total_amount + total
            cursor.execute("update order_master set total_amount ='" + str(ta) + "' where idorder_master = '" + str(idmaster[0]) + "' ")

            cursor.execute("select * from plants where idcategory='" + str(catid) + "' ")
            vdata = cursor.fetchall()
            return render(request, "view_items.html ", {"data": vdata, "itemid": itemid})

        elif datanotpayed == None:

            total_amount = int(0)
            del_status = "pending"
            pay_status_no = "no"

            cursor.execute(" insert into order_master values( null,'" + str(user) + "', curdate(), '" + str(
                total_amount) + "', '" + del_status + "', '" + pay_status_no + "' ) ")

            cursor.execute(" select idorder_master from order_master where user_id ='" + str(
                user) + "'  AND payment_status = '" + pay_status_no + "' ")
            idmastercolumn = cursor.fetchone()  # get idorder_master from ordermaster which inserted above
            idmaster = list(idmastercolumn)

            cursor.execute("insert into order_items values( null,'" + str(idmaster[0]) + "','" + pid + "', '" + str(
                quantity) + "', '" + str(total) + "') ")

            ta = total_amount + total

            cursor.execute("update order_master set total_amount ='" + str(ta) + "' where idorder_master = '" + str(
                idmaster[0]) + "' ")

            cursor.execute("select * from plants where idcategory='" + str(catid) + "' ")
            vdata = cursor.fetchall()
            return render(request, "view_items.html ", {"data": vdata, "id": catid, "itemid": itemid})
        else:
            cursor.execute(" select idorder_master from order_master where user_id ='" + str(
                user) + "'  AND payment_status = '" + pay_status_no + "' ")
            idmastercolumn = cursor.fetchone()  # get idorder_master from ordermaster which inserted above
            idmaster = list(idmastercolumn)

            cursor.execute(
                " select * from order_items where idorder_master ='" + str(idmaster[0]) + "' AND idplants= '" + str(
                    pid) + "' ")
            odata = cursor.fetchone()

            if odata == None:

                cursor.execute("insert into order_items values( null,'" + str(idmaster[0]) + "','" + pid + "', '" + str(
                    quantity) + "', '" + str(total) + "') ")

                cursor.execute(
                    " select total_amount from order_master where  idorder_master = '" + str(idmaster[0]) + "' ")
                total_amountrow = cursor.fetchone()
                total_amount = list(total_amountrow)
                ta = int(total_amount[0]) + total

                cursor.execute("update order_master set total_amount ='" + str(ta) + "' where idorder_master = '" + str(
                    idmaster[0]) + "' ")

                cursor.execute("select * from plants where idcategory='" + str(catid) + "' ")
                vdata = cursor.fetchall()
                return render(request, "view_items.html ", {"data": vdata, "itemid": itemid})
            else:

                cursor.execute(
                    "update order_items set quantity ='" + str(quantity) + "' where idplants = '" + str(pid) + "' ")

                cursor.execute(
                    "update order_items set total ='" + str(total) + "' where idplants = '" + str(pid) + "' ")

                cursor.execute("select total from order_items where idorder_master= '" + str(idmaster[0]) + "'")
                totalrow = cursor.fetchall()
                totallist = list(totalrow)
                print(totallist)
                v = int(0)
                for i in totallist:
                    v = v + int(i[0])

                cursor.execute("update order_master set total_amount ='" + str(v) + "' where idorder_master = '" + str(
                    idmaster[0]) + "' ")

                cursor.execute("select * from plants where idcategory='" + str(catid) + "' ")
                vdata = cursor.fetchall()
                return render(request, "view_items.html ", {"data": vdata, "itemid": itemid})
    else:
        messages.info(request, "Error Adding")


def admin_nltk_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback_nltk")
    data = cursor.fetchone()
    return render(request,'admin_feedback_nltk.html',{'data':data})