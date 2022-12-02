# AASD

### How to start

```docker-compose up --build```

### Additional commands
run xmpp server:
```
docker run --name ejabberd -d -p 5222:5222 --init ejabberd/ecs
```
create admin user in xmpp server:
```
docker exec -it ejabberd bin/ejabberdctl register admin localhost passw0rd
```
