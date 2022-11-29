# Nom_de_l'appli
Ce projet a été réalisé dans le contexte du cours de Systèmes Distribués pour le Traitement des Données (SDTD), suivi à l'Ensimag.

Notre application a pour objectif de faire de la détection d'émotions sur les visages des streamers depuis un flux vidéo [Twitch](https://www.twitch.tv/).

TODO : nom de l'appli, logo, description détaillée de l'appli / de l'infra / du RSE

# Déploiement de l'application sur Google Cloud Plateform
## Depuis l'interface web GCP
### Créer un nouveau projet
Avant toute chose, il faut créer un nouveau projet sur GCP: vous pouvez lui donner le nom et l'identifiant que vous souhaitez. En revanche, il faudra se souvenir de l'ID du projet pour plus tard. Il n'y a pas besoin de renseigner de zone.

### Activer les API Google
Le déploiement de notre application sur Google Cloud Plateform nécessite l'activation des API suivantes, dans l'onglet "API et services/API et services activés" du menu de l'interface Google Cloud :
- Compute Engine API
- Cloud Logging API
- Identity and Access Management (IAM) API
- Cloud Resource Manager API

### Créer un compte de service
La création d'un compte de service va permettre à nos scripts Terraform de pouvoir s'authentifier auprès des API Google Cloud et d'autoriser l'accès aux ressources du projet, ce qui va permettre le bon déploiement de notre application.

Dans l'onglet "IAM et administration/Comptes de service" du menu de l'interface Google Cloud, créer un nouveau compte de service; choisissez le nom du compte et l'identifiant que vous souhaitez, il faudra juste se souvenir de l'e-mail du compte pour plus tard.

## Depuis votre machine en local
### Installer les outils de déploiement
Pour déployer notre application nous utilisons les outils Terraform et Ansible. Vous aurez également probablement besoin de kubectl pour communiquer avec notre cluster Kubernetes une fois ce dernier déployé, ainsi que de Python3 pour exécuter le script de déploiement automatisé.

Distributions Debian/Ubuntu :
```
sudo apt-get install terraform python3 python3-pip
python3 -m pip install ansible
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

Distributions Manjaro/Arch :
```
sudo pacman -Sy terraform ansible kubectl python3
```

Distributions OSX :
```
brew install terraform ansible kubectl python3
```

### Cloner le dépôt du projet
Le dépôt étant composé de plusieurs sous-dépôts indépendants, appelés "modules" dans GitLab, il est nécessaire de cloner le dépôt récursivement afin de récupérer également ces sous-dépôts :

```
git clone --recursive git@gitlab.ensimag.fr:sdtd_2022-my-awesome-group/devops/deploy-infrastructure.git
```

### Dans le dossier `terraform-resources`
#### Mettre à disposition la clé publique SSH que Terraform va utiliser
Si vous n'avez pas de clé SSH ou voulez en générer une nouvelle, vous pouvez suivre [ce tutoriel](https://docs.oracle.com/en/cloud/cloud-at-customer/occ-get-started/generate-ssh-key-pair.html).

Copiez ensuite la clé publique générée dans ce dossier, sous le nom `terraform_key.pub`.

#### Créer une clé pour le compte de service
Depuis l'interface web Google Cloud, ajouter une clé pour le compte de service créé précédemment depuis l'onglet "IAM et administration/Comptes de service/" du menu Google Cloud, en séléctionnant votre compte et en allant dans l'onglet "Clés". Créer une clé, la télécharger au format JSON, et la copier dans ce dossier sous le nom `credentials.json`

#### Configurer les variables Terraform`
Copier le fichier `main.example.tfvars` dans un fichier `main.auto.tfvars` et le compléter avec les informations requises :
- l'identifiant du projet GCP (ex: "red-provider-365410")
- le nom de l'utilisateur local a qui appartient la clé SSH créée précédemment (ex: "leo")
- le nom du fichier qui contient la clé publique de la clé SSH créée précédemment (ex:" `terraform_key.pub`")
- le nombre d'instances que l'on souhaite créer (ex: 3)
- les réseaux autorisés à se connecter aux instances (format CIDR); ici, il faut qu'il y ait au moins le nôtre (ex: 130.190.0.0/16)

#### Lancer le script de déploiement
Si les étapes précédentes ont été réalisées correctement, le déploiement de notre application sur la plateforme Google Cloud ne devrait soulever aucune erreur. Pour cela, il faut lancer le script Python `deploy.py` :

```
python3 deploy.py
```


# Destruction des ressources allouées par notre application sur Google Cloud Plateform

Pour détruire toutes les ressources allouées par notre projet sur GCP, il suffit de lancer le script Python `destroy.py` dans le dossier `terraform-resources` :

```
cd terraform-resources && python3 destroy.py
```

# Limitations connues
TODO