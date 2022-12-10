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

`docker-compose up --build xmpp`
`docker-compose up --build server_ws`
`docker-compose up --build web_client`
`docker-compose up --build agent_1`

# TODO

https://github.com/javipalanca/spade/tree/master/examples

https://spade-mas.readthedocs.io/en/latest/behaviours.html

https://gist.github.com/sikorski-as/9435c54404b4008a2a3faa1974911a15

https://spade-mas.readthedocs.io/en/latest/agents.html

- FSM State (Maciej G.)
- Komunikacja messages (Adrian T.)
- Sektory (Kamil) + rysowanie tego w p5.js
