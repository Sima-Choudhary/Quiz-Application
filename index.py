#creating A quiz application using python
#https://shorturl.at/aBKX5
#index.html/home/default ->
import mysql.connector 
import random

my = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="", 
    database="quiz"
)


# Create a cursor object
cursor = my.cursor()

#cursor.execute("create table candidates(ID int AUTO_INCREMENT primary key ,Name varchar(100),Gender varchar(10),DOB date,Contact Varchar(10),Password varchar(20),Enrollment varchar(12))")



print("************************Welcome to quiz Application***********************************")
print(" 1.Registration   \n 2.Login Page     \n 3.Help   \n 4.Contact Us     \n 5.Exit")
print("**************************************************************************************")



def first():
    
    choice = (int)(input("Enter your choice :"))

    if choice ==1:
        register()
    elif choice ==2:
        login()
    elif choice ==3:
        help()
    elif choice ==4:
        contact()
    elif choice ==5:
        exitt()
    else:
        print("Please choose correct option :")


def register():
    print("\nEnter your Details\n")
    name = input("Enter your Name :")
    gender = input("Enter your Gender :")
    DOB = input("Enter your DOB :")
    contact = input("Enter your Contact No :")
    enrollment = input("Enter your Enrollment No :")   
    password = input("Enter your Password :")

    #user must enter the password till that is valid
    res =validate_password(password)
    while not res:
        password = input("Enter your Password :")
        res =validate_password(password)
    
    cursor.execute("INSERT INTO candidates(Name,Gender,DOB,Contact,Enrollment,Password) VALUES(%s,%s,%s,%s,%s,%s)",(name,gender,DOB,contact,enrollment,password))
    my.commit()
    print("Registered Successfully !! Now you can login \n\n*****************************************************************************")
    login()    


#validate password : upercase,lowercase,digit,special characters,length(8-20)

def validate_password(pwd):
    l=u=d=s=0
    if len(pwd) >8 and len(pwd) < 20:
      
        for i in pwd:
            if i.isupper():
                u +=1
            elif i.islower():
                l +=1
            elif i.isdigit():
                d +=1
            else:
                s +=1

    
    if l>=0 and u>=0 and d>=0 and s>=0 :
       return True
    else :
       return False


               


################################################################
def login():
    global username
    global logged_in
    global u_enrollment
    u_enrollment =input("Enter your Enrollment No :")
    
    cursor.execute("SELECT password,name FROM candidates WHERE enrollment=%s", (u_enrollment,))

    data = cursor.fetchone()
    #print(data)      tuple of strings

    
    if data is not None:
        pwd =input("Enter your password :")
        while  data[0] != pwd:
            print("you password is incorrect!! try Again ")            
            pwd = input("Enter your Password :")      
        
        print(f"welcome {data[1]}")
        username = data[1]
        logged_in = True
        
    else:
        print("wrong userName  or you have not registered\n************************************************************************************************")
    
        print("Do you want to continue ? \n1.Login\n2.Register\n************************************************************************")
        ch = input("Do you want to register!!! y/n")
        if ch=='y' or ch == 'Y':
            register()
        else:
            login()

            
    print("""
        Choose 1 : Attempt quiz
        Choose 2 : View result
        Choose 3 : Show profile
        Choose 4 : Update Profile
        """)
    ch = input("Enter your choice: ")
    if ch == '1':
        attemptQuiz()
    elif ch == '2':
        result()
    elif ch == '3':
        showProfile()
    elif ch == '4':
        updateProfile()



def updateProfile():
    print ("******************************UPDATE PROFILE ******************************")
    print(""" What Do you want to update
          1. Username
          2.Gender
          3.Date of birth
          4.Contact Number
          5.Enrollment Number
          6.Nothing needed to be updated
          """)    
    ch=input("Enter your choice: ")
    sql = "select * from candidates where Enrollment =%s"
    cursor.execute(sql, (u_enrollment,))
    user = cursor.fetchone()

    if ch == '1':
        user = input("Enter new username: ")
        cursor.execute("UPDATE candidates SET Name = %s WHERE Enrollment = %s", (user, u_enrollment))
        my.commit()
        print(f"Username updated to {user}")
    elif ch == '2':
        user = input("Enter new gender: ")
        cursor.execute("UPDATE candidates SET Gender = %s WHERE Enrollment = %s", (user, u_enrollment))
        my.commit()
        print(f"Gender updated to {user}")
    elif ch == '3':
        user = input("Enter new date of birth: ")
        cursor.execute("UPDATE candidates SET DOB = %s WHERE Enrollment = %s", (user, u_enrollment))
        my.commit()
        print(f"Date of birth updated to {user}")
    elif ch == '4':
        user = input("Enter new contact number: ")
        cursor.execute("UPDATE candidates SET Contact = %s WHERE Enrollment = %s", (user, u_enrollment))
        my.commit()
        print(f"Contact number updated to {user}")
    elif ch == '5':
        user = input("Enter new enrollment number: ")
        cursor.execute("UPDATE candidates SET Enrollment = %s WHERE Enrollment = %s", (user, u_enrollment))
        my.commit()
        print(f"Enrollment number updated to {user}")
    elif ch == '6':
        exitt()
    else:
        updateProfile()


def showProfile():
    sql = "select * from candidates where Enrollment =%s"
    cursor.execute(sql, (u_enrollment,))
    user = cursor.fetchone()
    if logged_in:
        print(f"\n\nUsername {user[1]}\nGender: {user[2]}\nDate of bith: {user[3]} \ncontact number : {user[4]}\nEnrollemnt No : {user[6]}")
        ch = input("Do you want to update your profile: y/n ")
        if ch == 'y' or ch == 'Y':
            updateProfile()
        else:
            exitt()
    else:
        print("You are not logged in!!\n")
        login()



def attemptQuiz():
    print("\n 1. Python\n 2. java \n \n")
    ch = input("Choose an option : ")
    if ch == '1':
        sql = "select * from questions where category = 'Python'"
        cursor.execute(sql)
        ques = cursor.fetchall() #fetchone()
        #print(ques) #[(),(),(),()]
        qu = [] #100
        for i in ques:
            qu.append(i) #[, , , , ,]
        qs = random.sample(qu,5) #14, 25, 89, 99
        n = 1
        Result = 0
        print(f"HEllo {username} you are attempting quiz of Python !!\n")
        for i in qs:
            op = [f"{i[3]}",f"{i[4]}",f"{i[5]},"f"{i[6]}"]
            random.shuffle(op)
            print(f"Q.{n}. {i[1]}\n A. {i[4]}\n B. {i[5]}\n C. {i[6]}\n D. {i[7]}\n")
            ans = input("Your Answer A/B/C/D: ").lower()
            if ans == i[2]:
                Result += 1

            n = n+1
        print(f"\nYour Result is {Result} out of 5")
        cursor.execute("UPDATE candidates SET Python_Result = %s WHERE Name = %s", (Result, username))
        my.commit()
    elif ch == '2':
        sql = "select * from questions where category = 'Java'"
        cursor.execute(sql)
        ques = cursor.fetchall() #fetchone()
        #print(ques) #[(),(),(),()]
        qu = [] #100
        for i in ques:
            qu.append(i) #[, , , , ,]
        qs = random.sample(qu,5) #14, 25, 89, 99
        n = 1
        Result = 0
        print(f"HEllo {username} you are attempting quiz of Java")
        for i in qs:
            op = [f"{i[3]}",f"{i[4]}",f"{i[5]},"f"{i[6]}"]
            random.shuffle(op)
            print(f"Q.{n}. {i[1]}\n A. {i[4]}\n B. {i[5]}\n C. {i[6]}\n D. {i[7]}\n")
            ans = input("Your Answer A/B/C/D: ").lower()
            if ans == i[2]:
                Result += 1

            n = n+1
        print(f"Your Result is {Result}")
        cursor.execute("UPDATE candidates SET Java_Result = %s WHERE Name = %s", (Result, username))
        my.commit()
        result()
   

########################################################################

def result():
    
    sql="""select * from candidates where enrollment= %s"""
    cursor.execute(sql, (u_enrollment,))
    ques = cursor.fetchone() 
    print("\n\n************Welcome to result page **************************")
    print("""Wich marks you want to check
          1.Python
          2.Java """)
    ch = input("Enter your choice: ")
    if ch == '1':
        if ques[8] != None:
            print(f"Your Python marks are {ques[8]}/5")
        else:
            print("You have not attempted Python quiz!!!")
    if ch == '2':
        if ques[7] != None:
            print(f"Your Java marks are {ques[7]}/5")
        else:
            print("You have not attempted Java quiz!!!")
    print("\nDo you want to Attempt Quiz? y/n ")
    ch= input("\nEnter any choise: ")
    if ch == "y" or ch == "Y":
        attemptQuiz()
    elif ch == "n" or ch =="N":
        exitt()
    else:
        print("Invalid option")
              

################################
def help():
    pass


################################
def contact():
    pass

################################
def exitt():
    print("Thanks for visiting!!!")
    exit()


# Declaring functions
if __name__=="__main__":
    first()


