```
docker build -t nats-pathway-app .
```

```
docker run --rm --network=host nats-pathway-app
```

```
docker run --rm --network=host -e RUN_MODE=notebook nats-pathway-app
```

