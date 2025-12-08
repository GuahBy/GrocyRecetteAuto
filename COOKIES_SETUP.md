# 🍪 Configuration cookies Instagram

## Ajouter le volume dans docker-compose.yml

Édite ton fichier `~/docker/docker-compose.yml` et ajoute le volume pour les cookies :

```yaml
recipe-api:
  build:
    context: ./GrocyRecetteAuto
    dockerfile: Dockerfile.api
  container_name: recipe-api
  environment:
    - GROCY_URL=http://grocy:80
    - GROCY_API_KEY=6GjzdHjcghEXlDkaGmpiC7sn2T2NxwGJzO8OEjYaKFW3FkLxmc
  ports:
    - 5000:5000
  volumes:
    - ./GrocyRecetteAuto/cookies:/app/cookies:ro  # ← AJOUTER CETTE LIGNE
  restart: unless-stopped
  depends_on:
    - grocy
```

Le `:ro` signifie "read-only" pour plus de sécurité.

## Puis restart

```bash
cd ~/docker
docker compose restart recipe-api
```

✅ Fait !
