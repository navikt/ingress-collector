# ingress-collector
Small application that collect ingresses from a kubernetes cluster and publish to a kafka topic.


## Inspiration

https://github.com/navikt/naisflow-decorators


```

docker-compose up -d --remove-orphans --build
```

```
k exec -it ingress-collector-857d9bc4fd-4ftr7  -- /bin/sh
```