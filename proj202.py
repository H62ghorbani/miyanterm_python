import tkinter
import sqlite3
import productAction

def is_admin():
    sql='''SELECT username FROM USERS WHERE id=?'''
    result=cnt.execute(sql,(session,))
    row=result.fetchone()
    if row[0] == "admin":
        return True
    else:
        return False

def login():
    global session
    user=txt_user.get()
    pas=txt_pass.get()
    sql='''SELECT * FROM USERS WHERE username=? AND pass=?'''
    result=cnt.execute(sql,(user,pas))
    rows=result.fetchall()
    if len(rows)<1:
        lbl_msg.configure(text="wrong username or password!",fg="red")
    else:
        session=rows[0][0]
        lbl_msg.configure(text="welcome to your account",fg="green")
        btn_login.configure(state="disabled")
        btn_logout.configure(state="active")
        btn_shop.configure(state="active")
        btn_cart.configure(state="active")
        if is_admin():
            btn_admin_panel.configure(state="active")
        txt_user.delete(0,"end")
        txt_pass.delete(0,"end")

def logout():
    global session
    lbl_msg.configure(text="you have logged out!", fg='red')
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    btn_shop.configure(state="disabled")
    btn_cart.configure(state="disabled")
    btn_admin_panel.configure(state="disabled")


def show_cart():
    win_cart=tkinter.Toplevel(win)
    win_cart.title("cart panel")
    win_cart.geometry("550x350")
    
    lstbx=tkinter.Listbox(win_cart,width=90)
    lstbx.pack()
    
    rows = productAction.getCart(session)

    for row in rows:
        pid = row[2]
        qnt = row[3]
        product = productAction.getProduct(pid)
        name = product[1]
        price = product[2]
        totol_price = qnt * price
        text=f"id:{pid}, Name:{name}, price:{price}, quantity:{qnt}, total price:{totol_price}"
        lstbx.insert("end",text)

    win_cart.mainloop()


def validation(user,pas,addr):
    if user=="" or pas=="" or addr=="":
        return False,"fill the inputs"
    
    if len(pas)<8:
        return False,"password length error!"
    
    sql='''SELECT * FROM USERS WHERE username=?'''
    result=cnt.execute(sql,(user,))
    rows=result.fetchall()
    if len(rows)>0:
        return False,"Username already exist!"
    
    return True,""
    
    
    
    
    
def submit():
    def register():
        user=txt_user.get()
        pas=txt_pass.get()
        addr=txt_addr.get()
        result,errorMSG=validation(user,pas,addr)
        if result: #if result==True 
            sql='''INSERT INTO users (username,pass,addr,grade)
                VALUES(?,?,?,?)'''
            cnt.execute(sql,(user,pas,addr,5))
            cnt.commit()
            lbl_msg.configure(text="submit done",fg="green")
        else:
            lbl_msg.configure(text=errorMSG,fg="red")
        
          
        
        
    win_submit=tkinter.Toplevel()  
    win_submit.title("Submit panel")
    win_submit.geometry("300x400")
    
    lbl_user=tkinter.Label(win_submit,text="Username: ")
    lbl_user.pack()
    txt_user=tkinter.Entry(win_submit)
    txt_user.pack()

    lbl_pass=tkinter.Label(win_submit,text="Password: ")
    lbl_pass.pack()
    txt_pass=tkinter.Entry(win_submit)
    txt_pass.pack()
    
    lbl_addr=tkinter.Label(win_submit,text="Address: ")
    lbl_addr.pack()
    txt_addr=tkinter.Entry(win_submit)
    txt_addr.pack()
    
    lbl_msg=tkinter.Label(win_submit,text="")
    lbl_msg.pack()
    
    btn_submit=tkinter.Button(win_submit,text="Submit",command=register)
    btn_submit.pack()
    
    win_submit.mainloop()

def shop():
    def buy():
        global session
        pid=txt_id.get()
        qnt=txt_qnt.get()
        result,msg=productAction.buyValidate(pid, qnt)
        if not result: #if result==False
              lbl_msg.configure(text=msg,fg="red")  
              return
        productAction.savetocart(session,pid,qnt)
        lbl_msg.configure(text="saved to cart",fg="green") 
        txt_id.delete(0,"end")
        txt_qnt.delete(0,"end")
        
        productAction.updateqnt(pid,qnt)
        
        lstbx.delete(0,"end")
        products=productAction.getAllProducts()
        for product in products:
            text=f"id:{product[0]},   Name:{product[1]},   price:{product[2]},   quantity:{product[3]}"
            lstbx.insert("end",text)
        
        
        
        
        
    win_shop=tkinter.Toplevel(win)
    win_shop.title("shop panel")
    win_shop.geometry("400x350")
    
    lstbx=tkinter.Listbox(win_shop,width=65)
    lstbx.pack()
    
    products=productAction.getAllProducts()
    for product in products:
        text=f"id:{product[0]},   Name:{product[1]},   price:{product[2]},   quantity:{product[3]}"
        lstbx.insert("end",text)
    
    lbl_id=tkinter.Label(win_shop,text="product id:")
    lbl_id.pack()
    txt_id=tkinter.Entry(win_shop)
    txt_id.pack()
    
    lbl_qnt=tkinter.Label(win_shop,text="quantity:")
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry(win_shop)
    txt_qnt.pack()
    
    lbl_msg=tkinter.Label(win_shop,text="")
    lbl_msg.pack()
    
    btn_buy=tkinter.Button(win_shop,text="buy",command=buy)
    btn_buy.pack()
    
    win_shop.mainloop()

def admin_panel():
    def add():
        global session
        pname=txt_name.get()
        price=txt_price.get()
        qnt=txt_qnt.get()
        
        productAction.addProduct(pname,price,qnt)
        lbl_msg.configure(text="new product added",fg="green") 
        txt_name.delete(0,"end")
        txt_price.delete(0,"end")
        txt_qnt.delete(0,"end")


    win_admin_panel=tkinter.Toplevel(win)
    win_admin_panel.title("shop panel")
    win_admin_panel.geometry("400x350")

    lbl_name=tkinter.Label(win_admin_panel,text="product name:")
    lbl_name.pack()
    txt_name=tkinter.Entry(win_admin_panel)
    txt_name.pack()
    
    lbl_price=tkinter.Label(win_admin_panel,text="price:")
    lbl_price.pack()
    txt_price=tkinter.Entry(win_admin_panel)
    txt_price.pack()
    
    lbl_qnt=tkinter.Label(win_admin_panel,text="quantity:")
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry(win_admin_panel)
    txt_qnt.pack()
    
    lbl_msg=tkinter.Label(win_admin_panel,text="")
    lbl_msg.pack()
    
    btn_add=tkinter.Button(win_admin_panel,text="add",command=add)
    btn_add.pack()
    
    win_admin_panel.mainloop()



 #----------------- main ------------------------------ 
session=False    
cnt=sqlite3.connect("store.db")

win=tkinter.Tk()
win.title("SHOP PROJECT")
win.geometry("300x300")

lbl_user=tkinter.Label(win,text="Username: ")
lbl_user.pack()
txt_user=tkinter.Entry(win)
txt_user.pack()

lbl_pass=tkinter.Label(win,text="Password: ")
lbl_pass.pack()
txt_pass=tkinter.Entry(win)
txt_pass.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

btn_login=tkinter.Button(win,text="Login",command=login)
btn_login.pack()

btn_logout=tkinter.Button(win,text="Logout",command=logout)
btn_logout.pack()

btn_submit=tkinter.Button(win,text="Submit",command=submit)
btn_submit.pack()

btn_shop=tkinter.Button(win,text="Shop",state="disabled",command=shop)
btn_shop.pack()

btn_cart=tkinter.Button(win,text="Cart",state="disabled",command=show_cart)
btn_cart.pack()

btn_admin_panel=tkinter.Button(win,text="Admin Panel",state="disabled",command=admin_panel)
btn_admin_panel.pack()


win.mainloop()