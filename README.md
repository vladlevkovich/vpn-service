
---

```
    git clone https://github.com/vladlevkovich/vpn-service.git

```


```
    docker build -t vpn:tag .
```

```
    docker run -p 8000:8000 vpn:tag
 ```

---

- ***`/api/v1/register`*** - **User register**
- ***`/api/v1/login`*** - **Login**
- ***`/api/v1/profile/`*** - **Receive and create a profile for the user**
- ***`/api/v1/user-sites/sites/`*** - **List sites**
- - ***`/api/v1/user-sites/proxy/<uuid:site_id>/`*** - **Replacing a link for an attribute **

---