from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox

class LoginPage:
    """登录界面"""

    def __init__(self, master):
        self.root = master
        self.root.geometry('400x200+600+300')
        self.root.title('学生管理系统')
        self.conn = sqlite3.connect('mydb.db')
        self.username = StringVar()
        self.password = StringVar()
        self.page = Frame(self.root)
        self.creatapage()

    def creatapage(self):
        """界面布局"""
        Label(self.page).grid(row=0)
        Label(self.page, text='用户名:').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码:').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, stick=E, column=1)
        Button(self.page, text='登录', command=self.login).grid(row=3, stick=W, pady=10)
        Button(self.page, text='注册账号', command=self.register).grid(row=3, stick=E, column=1)
        self.page.pack()

    def login(self):
        """登录功能"""
        curs = self.conn.cursor()
        query = "select username, password, loginerror from loginuser where username='%s'" % self.username.get()
        curs.execute(query)  # 返回一个迭代器
        c = curs.fetchall()  # 接收全部信息
        if len(c) == 0:
            messagebox.showerror('登录失败', '账户不存在')
        else:
            us, pw, lerror = c[0]
            if lerror >= 3:
                messagebox.showwarning('登录失败', '账户已被锁定')
            elif us == self.username.get() and pw == self.password.get():
                self.conn.close()
                messagebox.showinfo('登录成功', '欢迎：%s' % us)
                self.page.destroy()
                MainUI(self.root)
            else:
                messagebox.showwarning('登录失败', '密码错误')

    def register(self):
        """注册功能跳转"""
        self.conn.close()
        self.page.destroy()
        RegisterPage(self.root)


class RegisterPage:
    """注册界面"""

    def __init__(self, master=None):
        self.root = master
        self.root.title('账号注册')
        self.root.geometry('400x250')
        self.conn = sqlite3.connect('mydb.db')
        self.username = StringVar()
        self.password0 = StringVar()  # 第一次输入密码
        self.password1 = StringVar()  # 第二次输入密码
        self.email = StringVar()
        self.page = Frame(self.root)
        self.createpage()

    def createpage(self):
        """界面布局"""
        Label(self.page).grid(row=0)
        Label(self.page, text="账号:").grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text="密码:").grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password0, show='*').grid(row=2, column=1, stick=E)
        Label(self.page, text="再次输入:").grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.password1, show='*').grid(row=3, column=1, stick=E)
        Label(self.page, text="Email:").grid(row=4, stick=W, pady=10)
        Entry(self.page, textvariable=self.email).grid(row=4, column=1, stick=E)
        Button(self.page, text="返回", command=self.repage).grid(row=5, stick=W, pady=10)
        Button(self.page, text="注册", command=self.register).grid(row=5, column=1, stick=E)
        self.page.pack()

    def repage(self):
        """返回登录界面"""
        self.page.destroy()
        self.conn.close()
        LoginPage(self.root)

    def register(self):
        """注册"""
        if self.password0.get() != self.password1.get():
            messagebox.showwarning('错误', '密码核对错误')
        elif len(self.username.get()) == 0 or len(self.password0.get()) == 0 or len(self.email.get()) == 0:
            messagebox.showerror("错误", "不能为空")
        else:
            curs = self.conn.cursor()
            query = 'insert into loginuser values (?,?,?,?)'
            val = [self.username.get(), self.password0.get(), self.email.get(), 0]
            try:
                curs.execute(query, val)
                self.conn.commit()
                self.conn.close()
                messagebox.showinfo("成功", "注册成功，按确定返回登录界面")
                self.page.destroy()
                LoginPage(self.root)
            except sqlite3.IntegrityError:
                messagebox.showerror("注册失败", "该账户已存在")


class MainUI:
    """主界面"""

    def __init__(self, master=None):
        self.root = master
        self.dbstr = "mydb.db"
        self.root.geometry('700x700+300+50')
        self.root.title('学生管理系统')
        self.sid = StringVar()      # 学号
        self.name = StringVar()     # 姓名
        self.sex = StringVar()  # 性别
        self.score = StringVar()    # 成绩
        self.hobby = StringVar()  # 兴趣
        self.minzu = StringVar()  # 民族
        self.clickedStudentNumber = "未选中"   # 单击所选中的学生
        self.dataTreeview = ttk.Treeview(self.root, show='headings', column=('sid', 'name', 'sex','chengji','hobby','minzu'))
        self.createPage()

    def showAllInfo(self):
        """显示所有学生记录"""
        x = self.dataTreeview.get_children()
        for item in x:
            self.dataTreeview.delete(item)
        con = sqlite3.connect(self.dbstr)
        cur = con.cursor()
        cur.execute("select * from studentUser")
        lst = cur.fetchall()
        for item in lst:
            self.dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()
        con.close()


    def appendInfo(self):
        """添加学生记录"""
        if self.sid.get() == "":
            showerror(title='提示', message='输入不能为空')
        elif self.name.get() == "":
            showerror(title='提示', message='输入不能为空')
        elif self.sex.get()== 0:
            showerror(title='提示', message='输入不能为空')
        elif self.score.get() == "":
            showerror(title='提示', message='输入不能为空')
        elif self.hobby.get() == "":
            showerror(title='提示', message='输入不能为空')
        elif self.minzu.get() == "":
           showerror(title='提示', message='输入不能为空')
        else:
            x = self.dataTreeview.get_children()
            for item in x:
                self.dataTreeview.delete(item)
            list1 = []
            list1.append(self.sid.get())
            list1.append(self.name.get())
            list1.append(self.sex.get())
            list1.append(self.score.get())
            list1.append(self.hobby.get())
            list1.append(self.minzu.get())
            con = sqlite3.connect(self.dbstr)
            cur = con.cursor()
            cur.execute("insert into studentUser values(?,?,?,?,?,?)", tuple(list1))
            con.commit()
            cur.execute("select * from studentUser")
            lst = cur.fetchall()
            for item in lst:
                self.dataTreeview.insert("", 1, text="line1", values=item)
            cur.close()
            con.close()

    def deleteInfo(self):
        """删除学生记录"""
        con = sqlite3.connect(self.dbstr)
        cur = con.cursor()
        cur.execute("select * from studentUser")
        studentList = cur.fetchall()
        cur.close()
        con.close()
        print(self)
        print(studentList)
        num = self.clickedStudentNumber
        flag = 0
        if not num.isnumeric():
            showerror(title='提示', message='删除失败,未选中任何学生！')
            return
        for i in range(len(studentList)):
            for item in studentList[i]:
                if int(num) == item:
                    flag = 1
                    con = sqlite3.connect(self.dbstr)
                    cur = con.cursor()
                    cur.execute("delete from studentUser where id = ?", (int(num),))
                    con.commit()
                    cur.close()
                    con.close()
                    break
        if flag == 1:
            showinfo(title='提示', message='删除成功！')
        else:
            showerror(title='提示', message='删除失败')
        x = self.dataTreeview.get_children()
        for item in x:
            self.dataTreeview.delete(item)
        con = sqlite3.connect(self.dbstr)
        cur = con.cursor()
        cur.execute("select * from studentUser")
        lst = cur.fetchall()
        for item in lst:
            self.dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()
        con.close()

    # def print_radiobutton(self):
    #     print(self.sex.get())

    def getClickedStudentNumber(self,event):       # 获取显示列表中被单击选中的学生的学号
        self.clickedStudentNumber=self.dataTreeview.item(self.dataTreeview.selection()[0],"values")[0]
        print("您选中了一名学生，学号为：",str(self.clickedStudentNumber))

    def createPage(self):
        """界面布局"""
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute('create table if not exists studentUser(id int(10) primary key,name varchar(20),chengji int(10),sex char(2))')
        self.sex = StringVar()
        self.sex.set("男")

        Label(self.root, text="学号：").place(relx=0, rely=0.05, relwidth=0.1)
        Label(self.root, text="姓名：").place(relx=0.5, rely=0.05, relwidth=0.1)
        Label(self.root, text="成绩：").place(relx=0, rely=0.1, relwidth=0.1)
        Radiobutton(self.root, text='男', variable=self.sex, value="男").place(relx=0.5, rely=0.1, relwidth=0.1)
        Radiobutton(self.root, text='女', variable=self.sex, value="女").place(relx=0.6, rely=0.1, relwidth=0.1)
        # for lang, num in LANGS:
        #     Radiobutton(self.root, text=lang, variable=v, value=num).place(relx=0.75, rely=0.1, relwidth=0.1)
        Entry(self.root, textvariable=self.sid).place(relx=0.1, rely=0.05, relwidth=0.37, height=25)
        Entry(self.root, textvariable=self.name).place(relx=0.6, rely=0.05, relwidth=0.37, height=25)
        Entry(self.root, textvariable=self.score).place(relx=0.1, rely=0.1, relwidth=0.37, height=25)
        # Entry(self.root, textvariable=self.sex).place(relx=0.6, rely=0.1, relwidth=0.37, height=25)
        self.hobby = StringVar()
        self.hobby.set("爱好")  # 默认显示one
        OptionMenu(self.root, self.hobby, '睡觉', '吃饭', '学习python语言').place(relx=0.75, rely=0.1, relwidth=0.1)
        self.minzu = StringVar()
        self.minzu.set("民族")  # 默认显示one
        OptionMenu(self.root, self.minzu, '汉族', '苗族', '其他').place(relx=0.85, rely=0.1, relwidth=0.1)
        Label(self.root, text='学生信息管理', bg='white', fg='red', font=('宋体', 15)).pack(side=TOP, fill='x')
        Button(self.root, text="显示所有信息", command=self.showAllInfo).place(relx=0.2, rely=0.2, width=100)
        Button(self.root, text="添加信息", command=self.appendInfo).place(relx=0.4, rely=0.2, width=100)
        Button(self.root, text="删除信息", command=self.deleteInfo).place(relx=0.6, rely=0.2, width=100)
        self.dataTreeview.column('sid', width=100, anchor="center")
        self.dataTreeview.column('name', width=100, anchor="center")
        self.dataTreeview.column('sex', width=100, anchor="center")
        self.dataTreeview.column('chengji', width=100, anchor="center")
        self.dataTreeview.column('hobby', width=100, anchor="center")
        self.dataTreeview.column('minzu', width=100, anchor="center")
        self.dataTreeview.heading('sid', text='学号')
        self.dataTreeview.heading('name', text='名字')
        self.dataTreeview.heading('sex', text='性别')
        self.dataTreeview.heading('chengji', text='成绩')
        self.dataTreeview.heading('hobby', text='兴趣爱好')
        self.dataTreeview.heading('minzu', text='民族')
        self.dataTreeview.place(rely=0.3, relwidth=0.97)
        self.dataTreeview.bind('<ButtonRelease-1>',self.getClickedStudentNumber)
        self.showAllInfo()

if __name__ == '__main__':
    root = Tk()
    LoginPage(root)
    root.mainloop()