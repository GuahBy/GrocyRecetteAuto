# Intégration dans votre docker-compose.yml

## Option 1 : Ajout direct dans votre docker-compose existant

Ajoutez ce service à votre fichier docker-compose.yml actuel :

```yaml
  grocy-recipe-importer:
    build: ./grocy-recipe-importer
    container_name: grocy-recipe-importer
    environment:
      # Utilisez l'URL interne Docker de Grocy (port 80, pas 8081)
      - GROCY_URL=http://app:80
      # Mettez votre clé API Grocy ici
      - GROCY_API_KEY=VOTRE_CLE_API_ICI
    volumes:
      # Montage pour accéder aux fichiers HTML locaux
      - /srv/dev-disk-by-uuid-c3c3f421-e7ed-4bbf-b963-879042d8766a/NAS/downloads/recettes:/recettes
    # Pas de restart car c'est un outil CLI, pas un daemon
    restart: "no"
    depends_on:
      - app  # Dépend de Grocy (nextcloud "app")
```

## Utilisation avec Docker

### Importer depuis une URL
```bash
docker-compose run --rm grocy-recipe-importer \
  "https://www.marmiton.org/recettes/recette_poulet-curry.aspx"
```

### Importer depuis un fichier HTML local
```bash
# 1. Sauvegardez votre recette HTML dans le dossier recettes
# 2. Importez-la
docker-compose run --rm grocy-recipe-importer \
  "/recettes/ma-recette.html"
```

### Mode dry-run (prévisualisation)
```bash
docker-compose run --rm grocy-recipe-importer \
  "https://750g.com/recette.htm" \
  --dry-run
```

## Option 2 : Utilisation hors Docker (sur votre serveur)

Si vous préférez ne pas utiliser Docker pour cet outil :

```bash
# 1. Copier le dossier sur votre serveur
scp -r grocy-recipe-importer user@server:/chemin/vers/

# 2. Se connecter au serveur
ssh user@server

# 3. Installer les dépendances
cd /chemin/vers/grocy-recipe-importer
pip3 install -r requirements.txt

# 4. Configurer
cp .env.example .env
nano .env  # Modifier avec vos paramètres

# 5. Utiliser
source .env
./import-recette.sh "https://recette.com/..."
```

## Option 3 : Créer un alias pratique

Ajoutez dans votre `.bashrc` ou `.zshrc` sur le serveur :

```bash
alias import-recette='docker-compose -f /chemin/vers/docker-compose.yml run --rm grocy-recipe-importer'
```

Puis utilisez simplement :
```bash
import-recette "https://marmiton.org/recette.aspx"
```

## Récupérer votre clé API Grocy

1. Connectez-vous à Grocy : http://votre-serveur:8081
2. Cliquez sur l'icône de clé en haut à droite
3. Allez dans "Manage API keys"
4. Cliquez sur "+ Add" pour créer une nouvelle clé
5. Copiez la clé générée
6. Collez-la dans votre docker-compose.yml ou .env

## Déboguer les problèmes

### Le conteneur ne trouve pas Grocy
```bash
# Vérifier que Grocy est accessible depuis le conteneur
docker-compose run --rm grocy-recipe-importer curl http://app:80/api/system/info
```

### Voir les logs complets
```bash
docker-compose run --rm grocy-recipe-importer \
  "URL" \
  --grocy-url http://app:80 \
  --api-key VOTRE_CLE \
  -v  # Mode verbose (à implémenter si besoin)
```

## Notes importantes

- **URL interne Docker** : Utilisez `http://app:80` dans docker-compose (pas `localhost:8081`)
- **Clé API** : Ne committez JAMAIS votre clé API dans Git
- **Network** : Le conteneur doit être sur le même réseau Docker que Grocy (automatique avec docker-compose)
- **Performance** : Le premier run prendra plus de temps (téléchargement des dépendances Python)

## Structure des volumes

```
/srv/.../NAS/downloads/recettes/  ← Vos fichiers HTML locaux
    ↓ monté comme
/recettes/  ← Dans le conteneur
```

Donc si vous avez `/srv/.../recettes/tarte.html` sur votre serveur,
utilisez `/recettes/tarte.html` dans la commande Docker.
