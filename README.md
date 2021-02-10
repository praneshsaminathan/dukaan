# dukaan  
  
URL : **http://127.0.0.1:8000/api/v1/generate-otp/** 
Type: POST
Input: **Phonenumber with country code**.
Output: **OTP** 

URL : **http://127.0.0.1:8000/api/v1/login/** 
Input: phonenumber, otp, role [Buyer, Seller}
Output: **JWT Token**
Exp: Role is required for signup, for login not required


URL : **http://127.0.0.1:8000/api/v1/stores/** 
Type: POST
Input: 
 

       {
            "name": "Tempp Fry Kitchen",
            "address" : "test test",
            "postal_code": "638405"
        
        }

Output:

    {
     "id": "8b5d2fb6-9252-46df-a667-67bc09edc82d",
    "name": "Tempp Fry Kitchen",
    "slug": "tempp-3",
    "address": "test test",
    "postal_code": "638405",
    "created_by": "43899731-aaa1-470f-bf8c-3a46c9594b9f"
    }
Exp: **Slug will create automatically**

URL : **http://127.0.0.1:8000/api/v1/stores/--storeid--/** 
Type: GET, PUT, PATCH, DELETE
Output:

 {
     "id": "8b5d2fb6-9252-46df-a667-67bc09edc82d",
    "name": "Tempp Fry Kitchen",
    "slug": "tempp-3",
    "address": "test test",
    "postal_code": "638405",
    "created_by": "43899731-aaa1-470f-bf8c-3a46c9594b9f"
    }

Exp:
	Buyer create a store and  only created user can perform all actions.

URL : **http://127.0.0.1:8000/api/v1/categories/** 
Type: List
Output: 

    [{    
    "id": "f6c05243-3b17-400c-b159-da7824cf888d",
    "name": "sweets"
    }]

URL : **http://127.0.0.1:8000/api/v1/products/** 
Type: POST, DELETE, UPDATE, GET- ALLOWANY
Input:

     {
         "store": "8b5d2fb6-9252-46df-a667-67bc09edc82d",
        "name": "cookie",
        "sale_price": "5.00",
        "mrp": "4.50",
        "category": "sweet",
        "image": file field
        }
Output:

    {
    "id": "32016df1-5bc8-48f7-907c-355b2c5af0bb",
    "name": "Test",
    "description": "",
    "mrp": 5.0,
    "sale_price": 4.5,
    "image": "http://127.0.0.1:8000/product_image/header_QwX69Ew.png",
    "store": "8b5d2fb6-9252-46df-a667-67bc09edc82d"
    }
Exp:
	GET Method any one can use and  only the created user can perform all other actions.
	category string. if not in db create a category.

URL : **http://127.0.0.1:8000/api/v1/cart/** 
TYPE: CREATE, UPDATE, DELETE, RETREIVE- allowany

Input:

    {
    "line_items": "[{'product': '0c52ca4c-d4ea-4b1d-bffe-f2a4a0eb0c07', 'count': 5}]"
    }
Output:

    {
    "id": "48884c7b-f3c8-4194-953c-323711168c31",
    "line_items": "[{'product': '0c52ca4c-d4ea-4b1d-bffe-f2a4a0eb0c07', 'count': 5}]"
    }
Exp:
**I kept line_items as string field since SQLite didnt support ARRAYField.**

URL: **http://127.0.0.1:8000/api/v1/orders/**
Type: POST - Any Auth User
Input: 

    {
     "cart": "5d221a60-f763-4b0e-a871-2806e6c8363b"
    }
output:

    {
        "id": "48884c7b-f3c8-4194-953c-323711168c31",
        "line_items": "[{'product': '0c52ca4c-d4ea-4b1d-bffe-f2a4a0eb0c07', 'count': 5}]"
     }
URL: **http://127.0.0.1:8000/api/v1/orders/--orderid--**
Type: UPDATE, RETREIVE - Only object owner can modify

URL: **http://127.0.0.1:8000/api/v1/store/--store_slug--**
Type: GET - AllowAny
Exp: Slug name matched store info will return.

