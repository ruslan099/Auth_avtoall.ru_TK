from os import remove
from tkinter import *
import requests
from bs4 import BeautifulSoup
from requests.sessions import session
import fake_useragent

root = Tk()
root.title("Авторизация")
root.geometry("250x140")
root.resizable(False, False)

frame1 = Frame(root, bg = 'black', relief=SUNKEN)
frame1.grid(row = 0, column =0, sticky = W)

def auth():
    ent_stat = Entry(frame1, width=25, fg="white", bg="black")
    ent_stat.grid(row=3, column=0, columnspan=2)
    but_log.grid(row=4, column=0, columnspan=2, pady=10)
    ent_stat.delete(0,END)
    
    global session
    session = requests.Session()
    link = 'https://www.avtoall.ru/login/?type=email&back_url=https://www.avtoall.ru/'
    user = fake_useragent.UserAgent().random

    login = ent_login.get()
    pwd = ent_pwd.get()
    
    global header
    header = {
        "user-agent": user
    }
    data = {
        "LoginForm[type]":	"login",
        "LoginForm[username]": login,
        "LoginForm[password]": pwd,
        "yt0": "Войти"
    }

    responce = session.post(link, data=data, headers=header).text
    soup = BeautifulSoup(responce, 'lxml')

    try:
        if soup.find("a", class_="a logout").text == "[выйти]":
            ent_stat.insert(0, "Успешно!")
            but_log.grid(row=4, column=0, columnspan=2, pady=10)
            but_log.configure(fg="red")
            but_log['text']='В профиль!'
            but_log.configure(activebackground="black",command=profile)
    except AttributeError:
        None
    try:
        if soup.find("div", class_="errorMessage").text == "Неправильный логин/e-mail или пароль.":
            ent_stat.insert(0, "Ошибка!Неправильный логин/пароль")
            but_log.grid(row=4, column=0, columnspan=2, pady=10)
            ent_pwd.delete(0, END)
    except AttributeError:
        None

def profile():
    root.destroy()
    global root2
    root2 = Tk()
    root2.title("Профиль")
    root2.geometry("340x230")
    frame2 = Frame(root2, bg = 'white', relief=SUNKEN)
    frame2.grid(row = 0, column =0, sticky = W)

    profile_link = "https://www.avtoall.ru/personal/orders/"
    resp = session.get(profile_link, headers=header)    #Получаем и записываем код страницы
    global soup2
    soup2 = BeautifulSoup(resp.text, 'lxml')

    def my_orders():
        lst = []
        all_orders = soup2.findAll("h2")
        for item in all_orders:
            if item.find("a") is not None:
                lst.append(item.text)
        i=3
        for el in lst:
            el = str(el)
            el = el.replace("\n", " ")
            el = el.replace("                 ", "")
            el = el.replace("    ", " ")
            Label(frame2, text=el, bg="white").grid(row=i, column=0, columnspan=4, pady=5)
            i+=1

    lbl_name = Label(frame2, text="Добро пожаловать, "+soup2.find("a", class_="a").text, fg="red", bg="white")
    lbl_name.grid(row=0, column=0, sticky=SW)

    but_orders = Button(frame2, text="Мои заказы", width=15, command=my_orders)
    but_orders.grid(row=1, column=0)
    but_search = Button(frame2, text="Поиск товара", width=15, command=search)
    but_search.grid(row=1, column=1, sticky=W)
        
    root2.mainloop()


def search():
    root2.destroy()
    root3 = Tk()
    root3.title('{} - Поиск товара в каталоге'.format(soup2.find("a", class_="a").text))
    root3.geometry("750x600")
    frame3 = Frame(root3, bg = 'white', relief=SUNKEN)
    frame3.grid(row = 0, column =0, sticky = W)

    # Заранее объявляем переменную надписи, чтобы потом убирать из области видимости
    lbl_res_numb = Label(frame3)
    def poisk():
        link = 'https://www.avtoall.ru/search/?GlobalFilterForm%5Bnamearticle%5D='
        srch = str(ent_search.get())
        srch.replace(' ','+')
        link = link+srch

        response = session.get(link, headers=header).text

        soup3 = BeautifulSoup(response, 'lxml')

        # Получим количество товаров, найденных по запросу юзера
        try:
            res_numb = soup3.find("div", class_="searchQuery-result").text
        except AttributeError:
            res_numb = "Вы ничего не ввели!"

        # Теперь настраиваем скрываем надпись кол-ва товаров из области видимости(чтобы каждый раз обновлялась)
        lbl_res_numb.configure(text=res_numb, bg="white")
        lbl_res_numb.grid_forget()
        lbl_res_numb.grid(row=2, column=0, sticky=W, pady=10)

        all_tabs = soup3.findAll("strong", class_="item-name")
        ords = []
        for order in all_tabs:
            ords.append(order.find("a").text)

        all_prices = soup3.findAll("div", class_="price")

        prcs = []

        for price in all_prices:
            if price.find("b", class_="price-internet") is not None:
                prcs.append(price.text)

        listbox = Listbox(frame3, width=80, height=40)
        listbox.delete(0, END)
        x=3
        for i, j in zip(ords, prcs):
            listbox.insert(END, i+j)
            x += 1
        listbox.grid(row=3, column=0, sticky=NW, padx=10)

    lbl_search = Label(frame3, text="Что вас интересует?")
    lbl_search.grid(row=0, column=0)
    ent_search = Entry(frame3, width=100, borderwidth=2)
    ent_search.grid(row=1, column=0, padx=10)
    but_search = Button(frame3, text="Поиск", width=15, activebackground="white", command=poisk)
    but_search.grid(row=1, column=1, padx=5)

    root3.mainloop()


lbl_hi = Label(frame1, text="Пройдите авторизацию!", fg="red", bg="black")
lbl_hi.configure(font=("Courier", 10, "bold"))
lbl_hi.grid(row=0, column=0, columnspan=2, pady=10)

lbl_login = Label(frame1, text="Логин:", bg="black", fg="white")
lbl_login.grid(row = 1, column = 0)
ent_login = Entry(frame1, width=30)
ent_login.grid(row=1, column=1, padx=10)

lbl_pwd = Label(frame1, text="Пароль:", bg="black", fg="white")
lbl_pwd.grid(row=2, column=0)
ent_pwd = Entry(frame1, width=30, show="*")
ent_pwd.grid(row=2, column=1)

but_log = Button(frame1, text="Войти", width=15, activebackground="gray", command=auth)
but_log.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()