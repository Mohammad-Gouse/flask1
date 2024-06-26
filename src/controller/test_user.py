# def create_user(data):
#     phone_number = data['phone_number']
#     phone_number_verified = data['phone_number_verified']
#     mfa_enabled = data['cognito:mfa_enabled']
#     cognito_username = data['cognito:username']


#     'coginto:username'
#     # nickname = data['nickname']
#     email = data['email']
#     email_verified = data['email_verified']
#     user_attributes = []
#     username = data['cognito:username']
#     # if phone_number_verified == 'true':
#     #     username = phone_number
#     #     print("verified phone")
#     # elif email_verified == 'true':
#     #     username = email
#     #     print("verified email")
#     # else:
#     #     username = email

#     for attribute_name, attribute_value in data.items():
#         print("attribute name", attribute_name)
#         print("attribute value", attribute_value)
#         if attribute_name != cognito:username and attribute_name != cognito:mfa_enabled and attribute_name != custom:groups:
#             user_attributes.append({
#                 'Name': attribute_name,
#                 'Value': attribute_value
#             })

#     print("user_attributes: ", user_attributes)

#     try:
#         # create_user_response = cognito_client.admin_create_user(
#         #     UserPoolId=user_pool_id,
#         #     Username=username,
#         #     UserAttributes=user_attributes
#         # )

#         print(f'user created successfully {username}')
#         # assign_group(data, username)
#     except Exception as e:
#         # assign_group(data, username)
#         pass


# # data = {

# #     'user1': {
# #         'phone_number': '12346',
# #         'email': 'gouse@email.com',
# #         'phone_number_verified': 'false',
# #         'email_verified': 'true',
# #         'cognito:username': 'gouse username'
# #     },
# #     'user2': {
# #         'phone_number': '12346',
# #         'email': 'gouse@email.com',
# #         'phone_number_verified': 'false',
# #         'email_verified': 'true',
# #         'cognito:username': 'gouse username'
# #     }

# # }

# data = {
#     'phone_number': '12346',
#     'email': 'gouse@email.com',
#     'phone_number_verified': 'false',
#     'email_verified': 'true',
#     'cognito:username': 'gouse username'
# }

# create_user(data)
