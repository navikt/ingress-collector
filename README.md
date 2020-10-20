# ingress-collector
Small application that collect ingresses from a kubernetes cluster and push them to a REST endpoint
on `amplitude-proxy`


## Inspiration
https://github.com/navikt/naisflow-decorators

## Contract
Post an array containing all entries at one endpoint:
endpoint `PUT /ingresses/{collector}` this will reset all
entries for this cluster(?). Typical at collector startup.
After this changes can be pushed to the endpoint with 
`PATCH /ingresses/{collector}`

```json
{
  "uid": "something-unique-that-identifies-this-entry",
  "ingresses": [
    "http://mydomain.com/a-contextpath",
    "http://another-domain-that-for-some-reason-resolves.com/a-contextpath"
  ],
  "collector": "preprod-collector",
  "props": {
    "team": "my-team",
    "cluster": "my-cluster",
    "env": "prod or what ever",
    "custom-random-thing-that-should-be-tracked": "42"
  }
}
```

### Docker
```
docker-compose up -d --remove-orphans --build
```


