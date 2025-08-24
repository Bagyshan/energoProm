from django.test import TestCase

# Create your tests here.


import bcrypt

password = b'1234'  # твой новый пароль
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())



{
  "average_consumption": 98.765,
  "diff_amount": 10.5,
  "diff_percent": 9.279,
  "graphic_evaluate": [
    {
        "created_at": "2025-08-23T12:34:56Z",
        "consumption": 123.45,
        "current_check_date": "2025-08-23",
        "month_name": "Август"
    },
    {
        "created_at": "2025-08-23T12:34:56Z",
        "consumption": 123.45,
        "current_check_date": "2025-08-23",
        "month_name": "Август"
    },
    {
        "created_at": "2025-08-23T12:34:56Z",
        "consumption": 123.45,
        "current_check_date": "2025-08-23",
        "month_name": "Август"
    }
  ]
}