from database import Database

'''
CONSTANTS
'''
FULL_NAME = 0
USERNAME = 1
HOUSE = 2
TELEGRAM_ID = 3
CODE = 4
IS_HUMAN = 5
POINTS = 6

print("============ Start Of Test ==============")
testDatabase = Database()
testDatabase.create_tables()

# Ensuring user table queries work
## Insert users
print("Expected: 3 users printed")
testDatabase.insert_user("Bryan Leong Yong Shengg", "troller1234", "Leo", "1157634501", "submit_code1", "1", 5, "smallboi")
testDatabase.insert_user("Bryan Wong Hong Liang", "troller123", "Aquila", "1157634502", "submit_code2", "1", 10, "bryanwhl")
testDatabase.insert_user("Bryan Leong Hong Liang", "troller12", "Ursa", "1157634503", "submit_code3", "0", 15, "bryanlhl")
print(testDatabase.query_all_users())
print("==========================")

# ## Delete users
# print("Expected: 2 users printed")
# testDatabase.delete_user("Bryan Leong Hong Liang")
# print(testDatabase.query_all_users())
# print("==========================")

## Query exist fullname/username
print("Expected: False")
print(testDatabase.full_name_exist("Hello"))
print("Expected: True")
print(testDatabase.full_name_exist("Bryan Leong Yong Sheng"))
print("==========================")

print("Expected: True")
print(testDatabase.username_exist("troller1234"))
print("==========================")

## Query user
print("Expected: 1 user printed")
print(testDatabase.query_user("1157634501")[FULL_NAME])
print("==========================")

## Query number of humans and zombies
print("Expected: 2")
print(testDatabase.query_number_humans())
print("==========================")

print("Expected: 1")
print(testDatabase.query_number_zombies())
print("==========================")

## Query top usernames
print("Expected: Top 2")
print(testDatabase.query_top_usernames(2))
print("==========================")

# # Test admins table
# print("Expected: 1 user")
# testDatabase.insert_admin("1157634500")
# testDatabase.insert_admin("1157634501")
# testDatabase.insert_admin("1157634502")
# print(testDatabase.query_all_admins())

# ## Submit code
# print("Human submit human code")
# print(testDatabase.submit_code("1157634501", "submit_code1"))
# print("Expected: 5 points")
# print(testDatabase.query_user("1157634502"))
# print("==========================")

# # Ensuring code_submissions table work
# print("Expected: 1 pair of codes")
# print(testDatabase.query_code_submissions_table())
# print("==========================")



