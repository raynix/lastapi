# lastapi
The Omni REST API Client

This is still WIP, but I've got prototype working which is for the update DNS function using CloudFlare API.

The project is written in Python 3. You can install dependencies with
```
pip3 install --user -r requirements.txt
```

## Walk-through

### REST API schema
The schema is defined in [schemas/cloudflare.yaml](https://github.com/raynix/lastapi/blob/master/schemas/cloudflare.yaml)
```
---
Name: cloudflare
Base:
  Protocol: https
  Host: api.cloudflare.com
Headers:
  X-Auth-Key: ${auth_key}
  X-Auth-Email: ${auth_email}
  Content-Type: application/json

Actions:
  update_dns:
    Path:
      - /client/v4/zones/
      - ${zone_id}
      - /dns_records/
      - ${dns_id}
    Method: PUT
    Payload:
      type: ${dns_type}
      name: ${dns_name}
      content: ${dns_content}
      ttl: 1
      proxied: true
```
This will be verified against [schemas/schema.yaml](https://github.com/raynix/lastapi/blob/master/schemas/schema.yaml) using pykwalify.

### Global parameters
Global parameters for the API, usually API key and account stuff, are in [schemas/cloudflare-params.yaml.example](https://github.com/raynix/lastapi/blob/master/schemas/cloudflare-params.yaml.example). You should duplicate it and remove the `.example` suffix and put in real credential.
```
---
auth_key: sample-api-key
auth_email: raynix@some.email
```

### Invoking an Action in the schema
To invoke the `update_dns` action defined in the schema, run:
```
./lapi --schema schemas/cloudflare --func update_dns --vars zone_id=xxx,dns_id=xxx,dns_type=A,dns_name=mydomain.com,dns_content=1.2.3.4
```

Please comment or raise an issue if this doesn't work for you.
