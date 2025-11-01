from django.test import TestCase

# Create your tests here.
a = {
  "info": {
    "_postman_id": "0b5ff830-8847-4949-9a77-861d6b348817",
    "name": "ENERGOPROM",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "_exporter_id": "26701836",
    "_collection_link": "https://mydom-kg.postman.co/workspace/MyDom-Workspace~da62a64d-4062-48ad-9562-53cf4a1a5301/collection/26701836-0b5ff830-8847-4949-9a77-861d6b348817?action=share&source=collection_link&creator=26701836"
  },
  "item": [
    {
      "name": "платежные ссылки",
      "item": [
        {
          "name": "предварительный просмотр оплаты",
          "request": {
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{token}}",
                  "type": "string"
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "api-key",
                "value": "{{apiKey}}",
                "type": "text"
              },
              {
                "key": "Accept",
                "value": "application/json",
                "type": "text"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "account",
                  "value": "{{account}}",
                  "type": "text"
                },
                {
                  "key": "total",
                  "value": "400.8",
                  "type": "text"
                }
              ]
            },
            "url": {
              "raw": "{{baseUrl}}/invoice/preview",
              "host": [
                "{{baseUrl}}"
              ],
              "path": [
                "invoice",
                "preview"
              ]
            }
          },
          "response": []
        },
        {
          "name": "получить платежные ссылки",
          "request": {
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{token}}",
                  "type": "string"
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "api-key",
                "value": "{{apiKey}}",
                "type": "text"
              },
              {
                "key": "Accept",
                "value": "application/json",
                "type": "text"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "account",
                  "value": "{{account}}",
                  "type": "text"
                },
                {
                  "key": "total",
                  "value": "2.5",
                  "type": "text"
                }
              ]
            },
            "url": {
              "raw": "{{baseUrl}}/invoice/create",
              "host": [
                "{{baseUrl}}"
              ],
              "path": [
                "invoice",
                "create"
              ]
            }
          },
          "response": []
        },
        {
          "name": "история платежей",
          "request": {
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{token}}",
                  "type": "string"
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "api-key",
                "value": "{{apiKey}}",
                "type": "text"
              },
              {
                "key": "Accept",
                "value": "application/json",
                "type": "text"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "account",
                  "value": "{{account}}",
                  "type": "text"
                }
              ]
            },
            "url": {
              "raw": "{{baseUrl}}/payment/history",
              "host": [
                "{{baseUrl}}"
              ],
              "path": [
                "payment",
                "history"
              ]
            }
          },
          "response": []
        },
        {
          "name": "пдф чек об оплате",
          "request": {
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{token}}",
                  "type": "string"
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "api-key",
                "value": "{{apiKey}}",
                "type": "text"
              },
              {
                "key": "Accept",
                "value": "application/json",
                "type": "text",
                "disabled": true
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": []
            },
            "url": {
              "raw": "{{baseUrl}}/pdf/{{requisite}}",
              "host": [
                "{{baseUrl}}"
              ],
              "path": [
                "pdf",
                "{{requisite}}"
              ]
            }
          },
          "response": []
        },
        {
          "name": "logout",
          "request": {
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{token}}",
                  "type": "string"
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "api-key",
                "value": "{{apiKey}}",
                "type": "text"
              },
              {
                "key": "Accept",
                "value": "application/json",
                "type": "text"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": []
            },
            "url": {
              "raw": "{{baseUrl}}/user/logout",
              "host": [
                "{{baseUrl}}"
              ],
              "path": [
                "user",
                "logout"
              ]
            }
          },
          "response": []
        }
      ]
    }
  ],
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "type": "text/javascript",
        "packages": {

        },
        "requests": {

        },
        "exec": [
          ""
        ]
      }
    },
    {
      "listen": "test",
      "script": {
        "type": "text/javascript",
        "packages": {

        },
        "requests": {

        },
        "exec": [
          ""
        ]
      }
    }
  ],
  "variable": [
    {
      "key": "apiKey",
      "value": "123456"
    },
    {
      "key": "baseUrl",
      "value": "http://localhost:8080"
    },
    {
      "key": "token",
      "value": "ac19f0fa-13d2-4b23-99dd-b09cf2edabb7-skmimw6sl1gzqzbqtfibs0h3rwq4m7f90e7q7tiooixlpfegkwkgybafftkpkxqjp7peiuniltewzazjw4jj7uwpze295ww5ks5o"
    },
    {
      "key": "requisite",
      "value": ""
    },
    {
      "key": "account",
      "value": ""
    },
    {
      "key": "email",
      "value": ""
    },
    {
      "key": "password",
      "value": ""
    },
    {
      "key": "localBaseUrl",
      "value": ""
    }
  ]
}