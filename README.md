## Build the Containerized App.

```
docker build -t nats-pathway-app .
```

## Run the Python script

```
docker run --rm --network=host nats-pathway-app
```

## Run the Notebook as a script(Non interactive)

```
docker run --rm --network=host -e RUN_MODE=notebook nats-pathway-app
```

## Run the Notebook Interactive


```
docker run --rm -it -p 8888:8888 -e RUN_MODE=jupyter nats-pathway-app
```