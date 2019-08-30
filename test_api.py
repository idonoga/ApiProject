import requests


def check_home_page(_url):
    response_home_page = requests.get(_url)
    if response_home_page.status_code == 200:
        print("Homepage is Fine!")
        return 200
    else:
        print("Homepage is Down!!!")
        return 300


def check_add_users(_url):
    response_add_user = requests.post(_url, json={'user-id':'9999','user-name':'testuser','user-email':'testuser@test.com','user-password':'testpass'})
    if response_add_user.status_code == 200:
        print("Adding user didn't fail , now checking if the user exists")
        return_value = check_if_user_added('http://localhost:5000/ListUsers/9999')
        if return_value == 200:
            return 200
        else:
            return 300
    else:
        print("Adding user FAILED with status code = " + str(response_add_user.status_code))
        return 300


def check_if_user_added(_url):
    response_check_created_user = requests.get(_url)
    if str(response_check_created_user.json()) == "[[9999, 'testuser', 'testuser@test.com', 'testpass']]":
        print("User Created Successfully!")
        return 200
    else:
        print("User is not created successfully!!!")
        return 300


def check_modify_user(_url):
    response_modify_user = requests.put(_url, json={'user-id':'9999', 'user-name':'changed', 'user-email':'changed', 'user-password':'changed'})
    if response_modify_user.status_code == 200:
        print ("Modifying user didn't fail, checking if actually changed")
        if str(requests.get('http://localhost:5000/ListUsers/9999').json()) == "[[9999, 'changed', 'changed', 'changed']]":
            print ("User Successfully changed!!")
            return 200
        else:
            return 300
    else:
        return 300


def check_delete_users(_url):
    response_delete_user = requests.delete(_url)
    if str(response_delete_user.json()) == 'User Deleted Successfully':
        print ("User Deleted Successfully")
        return 200
    else:
        return 300


def test_api():
    _url = 'http://localhost:5000'
    homepage_status = check_home_page(_url)
    adduser_status = check_add_users(_url + '/' + 'AddUser')
    modifyuser_status = check_modify_user(_url + '/' + 'ModifyUser')
    deleteuser_status = check_delete_users(_url + '/' + 'DeleteUser/9999')
    if homepage_status == 300 or adduser_status == 300 or modifyuser_status == 300 or deleteuser_status == 300:
        return 300
    else:
        return 200
