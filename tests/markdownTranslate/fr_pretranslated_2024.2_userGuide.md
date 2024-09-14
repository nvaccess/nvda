# Guide de l'utilisateur de NVDA NVDA_VERSION

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Résumé des commandes -->



## Introduction {#Introduction}

Bienvenue dans NVDA !

NonVisual Desktop Access (NVDA) est une revue d'écran gratuite et à source ouverte pour le système d'exploitation Microsoft Windows.
En donnant des informations via une voix synthétique et le braille, il permet aux personnes aveugles ou malvoyantes d'accéder à un ordinateur sans coût additionnel par rapport à une personne voyante.
NVDA est développé par [NV Access](https://www.nvaccess.org/), avec des contributions de la communauté.

### Caractéristiques Générales {#GeneralFeatures}

En restituant l'information par synthèse vocale ou en braille, NVDA permet aux personnes aveugles et malvoyantes d'utiliser le système d'exploitation Windows ainsi que beaucoup d'applications disponibles dans cet environnement.

Une courte vidéo de démonstration en anglais, ["Qu'est-ce que NVDA ?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) est disponible sur la chaîne Youtube de NV Access.

Ses points forts sont :

* La prise en charge d'applications grand-public telles que des navigateurs Web, clients e-mail, programmes de tchat sur Internet et suites bureautiques
* Un synthétiseur intégré prenant en charge plus de 80 langues
* L'annonce, quand c'est possible, d'informations de mise en forme du texte telles que le nom et la taille de la police, le style et les fautes d'orthographe
* L'annonce automatique du texte sous la souris et, en option, l'indication sonore de la position de la souris
* La prise en charge de nombreux afficheurs braille, incluant la capacité de détecter automatiquement beaucoup d'entre eux ainsi que la saisie pour les afficheurs disposant d'un clavier braille
* La possibilité de s'exécuter entièrement depuis une clé USB ou tout autre média portable sans avoir à installer
* Un installateur parlant facile à utiliser
* Une traduction dans 54 langues
* La prise en charge des environnements Windows modernes, incluant les versions 32 et 64 bits
* L'accès à l'écran de connexion à Windows et aux [autres écrans sécurisés](#SecureScreens).
* L'annonce des contrôles et du texte durant l'utilisation de gestes tactiles
* Le support des interfaces d'accessibilité communes telles que Microsoft Active Accessibility, Java Access Bridge, IAccessible2 et UI Automation
* Le support de l'invite de commandes Windows et des applications en mode console
* La possibilité de mettre en évidence le focus système

### Configuration Système Requise {#SystemRequirements}

* Systèmes d'Exploitation : toutes les éditions 32-bit et 64-bit de Windows 8.1, Windows 10, Windows 11, et toutes les versions serveur à partir de Windows Server 2012 R2.
  * les variantes AMD64 et ARM64 de Windows sont prises en charge.
* au moins 150 Mo d'espace de stockage.

### Internationalisation {#Internationalization}

Il est important que chacun, partout dans le monde, quelle que soit sa langue, ait le même accès aux technologies.
Outre l'anglais, NVDA a été traduit en 52 langues : l'afrikaans, l'albanais, l'amharique, l'arabe, l'aragonais, le portugais (Brésil et Portugal), le bulgare, le birman, le catalan, l'espagnol (Colombie et Espagne), le croate, le tchèque, le danois, le néerlandais, le persan, le finnois, le français, le galicien, le Géorgien, l'allemand (Allemagne et Suisse), le grec, l'hébreu, l'hindi, le hongrois, l'islandais, l'irlandais, l'italien, le japonais, le kannada, le coréen, le kirghize, le lituanien, le macédonien, le Mongol, le népalais, le norvégien, le polonais, le portugais, le punjabi, le roumain, le russe, le serbe, le slovaque, le slovène, l'espagnol, le suédois, le tamoul, le thaï, le chinois traditionnel et simplifié, le turc, l'ukrainien et le vietnamien.

### Support des Synthèses Vocales {#SpeechSynthesizerSupport}

En plus de proposer ses messages et son interface en plusieurs langues, NVDA permet également à l'utilisateur de lire les contenus dans n'importe quelle langue, dans la mesure où il possède un synthétiseur parlant cette langue.

NVDA est fourni avec [eSpeak NG](https://github.com/espeak-ng/espeak-ng), un synthétiseur de parole gratuit, à source ouverte, multilingue.

Pour des informations concernant les autres synthétiseurs de parole pris en charge par NVDA, reportez-vous à la section [Synthétiseurs de parole pris en charge](#SupportedSpeechSynths).

### Support du Braille {#BrailleSupport}

Pour les utilisateurs possédant un terminal braille, NVDA peut afficher ses informations en braille.
NVDA utilise le traducteur braille à source ouverte [LibLouis](https://liblouis.io/) pour générer des séquences braille à partir de texte.
La saisie braille en intégral ou abrégé via un clavier braille est également supportée.
De plus, NVDA détectera automatiquement beaucoup de terminaux braille par défaut.
Reportez-vous à la section [Terminaux braille pris en charge](#SupportedBrailleDisplays) pour les informations concernant les terminaux braille.

NVDA propose de nombreux codes braille couvrant un grand ensemble de langues. Dans bien des cas, le braille intégral et abrégé sont disponibles. Pour les utilisateurs francophones, le braille français unifié est disponible en intégral et abrégé.

### Licence et Copyright {#LicenseAndCopyright}

NVDA est Copyright (C) NVDA_COPYRIGHT_YEARS NVDA contributors.

NVDA est disponible sous la licence GNU General Public License Version 2), avec deux exceptions spéciales.
Les exceptions sont précisées dans le document de licence dans la section "Non-GPL Components in Plugins and Drivers" et "Microsoft Distributable Code".
NVDA inclut et utilise également des composants qui sont disponibles sous différentes licences libres et open source.
Vous avez le droit de distribuer ou modifier ce logiciel comme il vous plaît pourvu que vous distribuiez la licence avec le logiciel, et rendiez disponible l'intégralité du code source pour toute personne qui le veut.
Ceci s'applique aussi bien à la version originale qu'aux copies modifiées de ce logiciel, et aussi à tout travail dérivé.

Pour plus de détails, vous pouvez [lire l'intégralité de la licence.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Pour les détails concernant les exceptions, veuillez consulter le document de licence depuis le menu NVDA dans la section "Aide".

## Guide de Démarrage Rapide de NVDA {#NVDAQuickStartGuide}

Ce guide de démarrage rapide contient trois sections principales : téléchargement, configuration initiale et exécution de NVDA.
Celles-ci sont suivies d'informations sur l'ajustement des préférences, l'utilisation des extensions, la participation à la communauté et l'obtention d'aide.
Les informations contenues dans ce guide sont condensées à partir d'autres parties du Guide de l'utilisateur NVDA.
Veuillez vous reporter au Guide de l'utilisateur complet pour obtenir des informations plus détaillées sur chaque sujet.

### Télécharger NVDA {#GettingAndSettingUpNVDA}

NVDA est entièrement gratuit pour tout le monde.
Il ne nécessite pas de clé de licence ni d'abonnement coûteux à payer.
NVDA est mis à jour, en moyenne, quatre fois par an.
La dernière version de NVDA est toujours disponible à partir de la page "Télécharger" du [site Web de NV Access](NVDA_URL).

NVDA fonctionne avec toutes les versions récentes de Microsoft Windows.
Vérifiez les [Configurations requises](#SystemRequirements) pour plus de détails.

#### Étapes pour Télécharger NVDA {#StepsForDownloadingNVDA}

Ces étapes supposent une certaine familiarité avec la navigation sur une page Web.

* Ouvrez votre navigateur Web (appuyez sur la touche `Windows`, tapez le mot "internet" sans les guillemets et appuyez sur `entrer`)
* Chargez la page de téléchargement de NV Access (Appuyez sur `alt+d`, tapez l'adresse suivante et appuyez sur `entrée`):
https://www.nvaccess.org/download
* Activez le bouton "télécharger"
* Le navigateur peut ou non demander une action à effectuer après le téléchargement, puis lancer le téléchargement
* Selon le navigateur, le fichier peut s'exécuter automatiquement après son téléchargement
* Si le fichier doit être lancé manuellement, appuyez sur `alt+n` pour accéder à la zone de notification, puis sur `alt+r` pour exécuter le fichier (ou les étapes de votre navigateur)

### Mise en place de NVDA {#SettingUpNVDA}

Démarrer le fichier téléchargé exécutera une version temporaire de NVDA.
Il vous sera alors demandé si vous souhaitez installer NVDA, créer une copie portable ou simplement continuer à utiliser la copie temporaire.

NVDA n'a pas besoin d'accéder à Internet pour s'exécuter ou s'installer une fois le lanceur téléchargé.
Si elle est disponible, une connexion Internet permet à NVDA de vérifier périodiquement les mises à jour.

#### Étapes pour exécuter le lanceur téléchargé {#StepsForRunningTheDownloadLauncher}

Le fichier d'installation est nommé "nvda_2022.1.exe" ou similaire.
L'année et la version changent entre les mises à jour pour refléter la version actuelle.

1. Exécutez le fichier téléchargé.
Une musique est jouée pendant le chargement d'une copie temporaire de NVDA.
Une fois chargé, NVDA parlera tout au long du processus.
1. La fenêtre du Lanceur NVDA apparaît avec le contrat de licence.
Appuyez sur `flècheBas` pour lire le contrat de licence si vous le souhaitez.
1. Appuyez sur `tab` pour passer à la case "J'accepte", puis appuyez sur la `barre d'espace` pour la cocher.
1. Appuyez sur `tab` pour parcourir les options, puis appuyez sur `entrée` sur l'option souhaitée.

Les options sont :

* "Installer NVDA sur cet ordinateur" : C'est l'option principale que la plupart des utilisateurs souhaitent pour une utilisation facile de NVDA.
* "Créer une copie portable" : Cela permet à NVDA d'être copié dans n'importe quel dossier sans installation.
Ceci est utile sur les ordinateurs sans droits d'administrateur ou sur une clé USB à emporter avec vous.
Lorsque cette option est sélectionnée, NVDA parcourt les étapes pour créer une copie portable.
La principale chose que NVDA doit connaître est le dossier dans lequel configurer la copie portable.
* "Continuer l'exécution" : Cela permet de maintenir la copie temporaire de NVDA en cours d'exécution.
Ceci est utile pour tester les fonctionnalités d'une nouvelle version avant de l'installer.
Lorsque cette option est sélectionnée, la fenêtre du lanceur se ferme et la copie temporaire de NVDA continue de s'exécuter jusqu'à ce qu'elle soit fermée ou que le PC soit arrêté.
Notez que les modifications apportées aux paramètres ne sont pas enregistrées.
* "Quitter" : Cela ferme NVDA sans effectuer aucune action.

Si vous prévoyez de toujours utiliser NVDA sur cet ordinateur, vous choisirez d'installer NVDA.
L'installation de NVDA permettra des fonctionnalités supplémentaires telles que le démarrage automatique après la connexion, la possibilité de lire l'écran de connexion Windows et [les écrans sécurisés](#SecureScreens).
Cela ne peut pas être fait avec des copies portables ou temporaires.
Pour plus de détails sur les limitations lors de l'exécution d'une copie portable ou temporaire de NVDA, veuillez consulter les [Restrictions relatives aux copies portables et temporaires](#PortableAndTemporaryCopyRestrictions).

L'installation propose également de créer des raccourcis dans le menu Démarrer et sur le bureau, et permet à NVDA d'être démarré avec `contrôle+alt+n`.

#### Étapes pour installer NVDA depuis le lanceur {#StepsForInstallingNVDAFromTheLauncher}

Ces étapes décrivent les options de configuration les plus courantes.
Pour plus de détails sur les options disponibles, veuillez consulter [Options d'installation](#InstallingNVDA).

1. Depuis le lanceur, assurez-vous que la case à cocher pour accepter la licence est cochée.
1. Appuyez sur `Tab` jusqu'au bouton "Installer NVDA sur cet ordinateur" et activez-le.
1. Ensuite, viennent des options pour utiliser NVDA lors de la connexion à Windows et pour créer un raccourci sur le bureau.
Celles-ci sont cochées par défaut.
Si vous le souhaitez, appuyez sur `tabulation` et `barre d'espace` pour modifier l'une de ces options, ou laissez-les par défaut.
1. Appuyez sur `entrée` pour continuer.
1. Un dialogue Windows "Contrôle de compte d'utilisateur (UAC)" apparaît et vous demande "Voulez-vous autoriser cette application à apporter des modifications à votre PC ?".
1. Appuyez sur `alt+o` pour accepter l'invite UAC.
1. Une barre de progression se remplit au fur et à mesure de l'installation de NVDA.
Au cours de ce processus, NVDA émet un bip de plus en plus aigu.
Ce processus est souvent rapide et peut ne pas être remarqué.
1. Un dialogue apparaît confirmant que l'installation de NVDA a réussi.
Le message demande d'"Appuyer sur OK pour démarrer la copie installée".
Appuyez sur `entrée` pour démarrer la copie installée.
1. Le dialogue "Bienvenue dans NVDA" apparaît et NVDA lit un message de bienvenue.
Le focus est mis sur le menu déroulant "Disposition du clavier".
Par défaut, la disposition du clavier "Ordinateur de bureau" utilise le pavé numérique pour certaines fonctions.
Si vous le souhaitez, appuyez sur `flècheBas` pour choisir la disposition du clavier "Ordinateur portable" afin de réaffecter les fonctions du pavé numérique à d'autres touches.
1. Appuyez sur `tab` pour passer à "Utiliser `verrouillage majuscule` comme touche de modification NVDA".
`Insert` est défini comme touche de modification NVDA par défaut.
Appuyez sur `barre d'espace` pour sélectionner `verrouillage majuscule` comme touche de modification alternative.
Notez que la disposition du clavier est définie séparément de la touche de modification NVDA.
La touche de modification NVDA et la disposition du clavier peuvent être modifiées ultérieurement à partir des paramètres du clavier.
1. Utilisez `tab` et `barre d'espace` pour ajuster les autres options sur cet écran.
Celles-ci définissent si NVDA doit démarrer automatiquement.
1. Appuyez sur `entrée` pour fermer le dialogue avec NVDA en cours d'exécution.

### Exécuter NVDA {#RunningNVDA}

Le guide de l'utilisateur complet de NVDA contient toutes les commandes NVDA, divisées en différentes sections pour référence.
Les tableaux de commandes sont également disponibles dans le "Résumé des Commandes".
Le module de formation NVDA "Basic Training for NVDA" (en anglais) étudie chaque commande plus en profondeur avec des activités étape par étape.
"Basic Training for NVDA" est disponible dans la [boutique NV Access](http://www.nvaccess.org/shop).

Voici quelques commandes de base fréquemment utilisées.
Toutes les commandes sont configurables, ce sont donc les frappes par défaut pour ces fonctions.

#### La Touche de Modification NVDA {#NVDAModifierKey}

La touche de modification NVDA par défaut est soit `pavnumZéro`, (avec `verrouillage numérique` désactivé), soit la touche `insert`, près des touches `effacement`, `début` et `fin`.
La touche de modification NVDA peut également être définie sur la touche `verrouillage majuscule`.

#### Aide à la Saisie {#InputHelp}

Pour apprendre et pratiquer l'emplacement des touches, appuyez sur `NVDA+1` pour activer l'aide à la saisie.
En mode d'aide à la saisie, effectuer n'importe quel geste de saisie (comme appuyer sur une touche ou effectuer un geste tactile) signalera l'action et décrira ce qu'elle fait (le cas échéant).
Les commandes réelles ne s'exécuteront pas en mode d'aide à la saisie.

#### Démarrer et Arrêter NVDA {#StartingAndStoppingNVDA}

| Nom |Touche ordinateur de bureau |Touche ordinateur portable |Description|
|---|---|---|---|
|Démarrer NVDA |`contrôle+alt+n` |`contrôle+alt+n` |Démarre ou redémarre NVDA|
|Quitter NVDA |`NVDA+q`, puis `entrée` |`NVDA+q`, puis `entrée` |quitte NVDA|
|Interrompre ou relancer la parole |`majuscule` |`majuscule` |Interrompt instantanément la parole. Un nouvel appui reprendra la parole là où elle s'est arrêtée|
|Arrêt de la parole |`contrôle` |`contrôle` |Interrompt instantanément la parole|

#### Lire du texte {#ReadingText}

| Nom |Touche ordinateur de bureau |Touche ordinateur portable |Description|
|---|---|---|---|
|Dire tout |`NVDA+flècheBas` |`NVDA+a` |Commence à lire à partir de la position courante en la déplaçant au fur et à mesure|
|Lire la ligne courante |`NVDA+flècheHaut` |`NVDA+l` |Lit la ligne. Un double appui épelle la ligne. Un triple appui épelle la ligne en utilisant la description de caractères (Alpha, Bravo, Charlie, etc)|
|Lire la sélection |`NVDA+maj+flècheHaut` |`NVDA+maj+s` |Lit tout texte sélectionné. Un double appui épelle l'information. Un triple appui l'épelle en code international|
|Lire le texte du presse-papiers |`NVDA+c` |`NVDA+c` |Lit tout texte dans le presse-papiers. Un double appui épelle l'information. Un triple appui l'épelle en code international|

#### Annoncer la position et autres informations {#ReportingLocation}

| Nom |Touche ordinateur de bureau |Touche ordinateur portable |Description|
|---|---|---|---|
|Titre de la fenêtre |`NVDA+t` |`NVDA+t` |Annonce le titre de la fenêtre actuellement active. Un double appui épelle l'information. Un triple appui la copie dans le presse-papiers|
|Annoncer le focus |`NVDA+tab` |`NVDA+tab` |Annonce le contrôle actuellement en focus. Un double appui épelle l'information. Un triple appui l'épelle en code international|
|Lire la fenêtre |`NVDA+b` |`NVDA+b` |Lit entièrement la fenêtre courante (utile pour les dialogues)|
|Lire la barre d'état |`NVDA+fin` |`NVDA+maj+fin` |Annonce la barre d'état si NVDA en trouve une. Un double appui épelle l'information. Un triple appui la copie dans le presse-papiers|
|Lire l'heure |`NVDA+f12` |`NVDA+f12` |Un appui annonce l'heure courante, un double appui annonce la date. L'heure et la date sont annoncées dans le format spécifié dans les paramètres Windows pour l'horloge de la barre d'état système.|
|Annoncer la mise en forme du texte |`NVDA+f` |`NVDA+f` |Annonce la mise en forme du texte. Un double appui affiche l'information dans une fenêtre|
|Annoncer la destination du lien |`NVDA+k` |`NVDA+k` |Un appui annonce l'URL de destination du lien à la position courante du curseur ou du focus. Deux appuis l'affichent dans une fenêtre pour une revue plus attentive|

#### Choisir les informations lues par NVDA {#ToggleWhichInformationNVDAReads}

| Nom |Touche ordinateur de bureau |Touche ordinateur portable |Description|
|---|---|---|---|
|Dire les caractères tapés |`NVDA+2` |`NVDA+2` |Lorsqu'activé, NVDA annoncera tous les caractères que vous tapez sur le clavier.|
|Dire les mots tapés |`NVDA+3` |`NVDA+3` |Lorsqu'activé, NVDA annoncera les mots que vous tapez sur le clavier.|
|Dire les touches de commande |`NVDA+4` |`NVDA+4` |Lorsqu'activé, annoncera toutes les touches n'étant pas des caractères que vous taperez sur le clavier. Cela inclut les combinaisons de touches telles que contrôle plus une autre lettre.|
|Activer le suivi de la souris |`NVDA+m` |`NVDA+m` |Lorsqu'activé, NVDA annoncera le texte actuellement sous le pointeur souris, tandis que vous le déplacez sur l'écran. Cela vous permet de trouver les choses sur l'écran, en déplaçant physiquement la souris, plutôt que d'essayer de les trouver en utilisant la navigation par objet.|

#### La boucle des paramètres synthétiseur {#TheSynthSettingsRing}

| Nom |Touche ordinateur de bureau |Touche ordinateur portable |Description|
|---|---|---|---|
|Aller au paramètre synthétiseur suivant |`NVDA+contrôle+flècheDroit` |`NVDA+maj+contrôle+flècheDroit` |Va au paramètre vocal suivant disponible, retournant au premier après le dernier|
|Aller au paramètre synthétiseur précédent |`NVDA+contrôle+flècheGauche` |`NVDA+maj+contrôle+flècheGauche` |Va au paramètre vocal précédent disponible, retournant au dernier après le premier|
|Augmenter le paramètre synthétiseur courant |`NVDA+contrôle+flècheHaut` |`NVDA+maj+contrôle+flècheHaut` |Augmente le paramètre vocal sur lequel vous vous trouvez. Ex. augmente le débit, choisit la voix suivante, augmente le volume|
|Augmenter le paramètre courant dans la boucle des paramètres du synthétiseur d'un interval plus important |`NVDA+contrôle+pagePrec` |`NVDA+maj+contrôle+pagePrec` |Augmente d'un pas plus important la valeur du paramètre vocal courant sur lequel vous vous trouvez. Ex. lorsque vous êtes sur le paramètre du choix de la voix, avancer de 20 voix ; lorsque vous êtes sur un paramètres avec potentiomètre (débit, hauteur, etc.), la valeur sera incrémentée de 20%|
|Diminuer le paramètre synthétiseur courant |`NVDA+contrôle+flècheBas` |`NVDA+maj+contrôle+flècheBas` |diminue le paramètre vocal sur lequel vous vous trouvez. Ex. diminue le débit, choisit la voix précédente, diminue le volume|
|Diminuer le paramètre courant dans la boucle des paramètres du synthétiseur d'un interval plus important |`NVDA+contrôle+pageSuiv` |`NVDA+maj+contrôle+pageSuiv` |Diminue d'un pas plus important la valeur du paramètre vocal courant sur lequel vous vous trouvez. Ex. lorsque vous êtes sur le paramètre du choix de la voix, reculer de 20 voix ; lorsque vous êtes sur un paramètres avec potentiomètre (débit, hauteur, etc.), la valeur sera décrémentée de 20%|

Il est également possible de sauter à la première ou à la dernière valeur du paramètre de synthétiseur courant en attribuant des gestes personnalisés dans la [boîte de dialogue Gestes de commandes](#InputGestures), sous la catégorie parole.
Par exemple, cela signifie que lorsque le débit est le paramètre courant, le débit sera modifié à 0 ou 100.
Lorsque vous êtes sur le paramètre voix, la première ou la dernière voix sera activée.

#### Navigation sur le web {#WebNavigation}

La liste complète des touches de navigation à lettre unique se trouve dans la section [Mode Navigation](#BrowseMode) du guide de l'utilisateur.

| Commande |Frappe |Description|
|---|---|---|
|Titre |`h` |Aller au titre suivant|
|Titre de niveau 1, 2, ou 3 |`1`, `2`, `3` |Aller au titre suivant au niveau spécifié|
|Champ de formulaire |`f` |Aller au champ de formulaire suivant (zone d'édition, bouton, etc)|
|Lien |`k` |Aller au lien suivant|
|Région |`d` |Aller à la région suivante|
|Liste |`l` |Aller à la liste suivante|
|Tableau |`t` |Aller au tableau suivant|
|Revenir en arrière |`maj+lettre` |Pressez `maj` et n'importe laquelle des lettres ci-dessus pour aller à l'élément précédent de ce type|
|Liste des éléments |`NVDA+f7` |Liste différents types d'éléments, tels que liens et titres|

### Préférences {#Preferences}

La plupart des fonctions NVDA peuvent être activées ou modifiées via les paramètres NVDA.
Les paramètres et d'autres options sont disponibles via le menu de NVDA.
Pour ouvrir le menu de NVDA, appuyez sur `NVDA+n`.
Pour ouvrir directement le dialogue des paramètres généraux de NVDA, appuyez sur `NVDA+contrôle+g`.
De nombreux écrans de paramètres ont des touches pour les ouvrir directement, comme `NVDA+contrôle+s` pour le synthétiseur, ou `NVDA+contrôle+v` pour les autres options de parole.

### Extensions {#Addons}
Les extension sont des programmes qui fournissent des fonctionnalités nouvelles ou modifiées pour NVDA.
Les extensions sont développées par la communauté NVDA ou par des sociétés externes et ne sont pas affiliés à NV Access.
Comme pour tout logiciel, il est important de faire confiance au développeur d'une extension avant de l’utiliser.
Veuillez consulter [Installation d'extensions](#AddonStoreInstalling) pour savoir comment vérifier les extensions avant l'installation.

La première fois que l'Add-on Store est ouvert, NVDA affiche un avertissement concernant les extensions.
Les extensions ne sont pas approuvées par NV Access et peuvent avoir des fonctionnalités et un accès aux informations sans restriction.
Appuyez sur `espace` si vous avez lu l'avertissement et que vous n'avez pas besoin de le voir la prochaine fois.
Appuyez sur `tab` pour atteindre le bouton "OK", puis sur `Entrée` pour accepter l'avertissement et accéder à l'Add-on Store.
La section "[Extensions et Add-on Store](#AddonsManager)" du guide de l'utilisateur contient des informations sur chaque fonctionnalité de l'Add-on Store.

L'Add-on Store est disponible dans le menu Outils.
Appuyez sur `NVDA+n` pour ouvrir le menu NVDA, puis sur `o` pour Outils, puis sur `s` pour Add-on Store.
Lorsque l'Add-on Store s'ouvre, il affiche "Extensions disponibles" si aucune extension n'est installée.
Lorsque des extensions sont déjà installées, l'Add-on Store s'ouvre sur l'onglet "Extensions installées".

#### Extensions disponibles {#AvailableAddons}
Lorsque la fenêtre s'ouvre pour la première fois, le chargement des extensions peut prendre quelques secondes.
NVDA lira le nom de la première extension une fois que le chargement de la liste des extensions est terminé.
Les extensions disponibles sont listées par ordre alphabétique dans une liste à plusieurs colonnes.
Pour parcourir la liste et trouver une extension spécifique :

1. Utilisez les touches fléchées ou appuyez sur la première lettre du nom d'une extension pour vous déplacer dans la liste.
1. Appuyez une fois sur `tab` pour passer à une description de l'extension actuellement sélectionné.
1. Utilisez les [touches de lecture](#ReadingText) ou les touches fléchées pour lire la description complète.
1. Appuyez sur `tab` pour atteindre le bouton "Actions", qui peut être utilisé pour installer l'extension entre autres actions.
1. Appuyez sur `tab` jusqu'au champ "Autres détails", qui répertorie des détails tels que l'éditeur, la version et la page web.
1. Pour revenir à la liste des extensions, appuyez sur `alt+e`, ou `maj+tab` jusqu'à atteindre la liste.

#### Rechercher des extensions {#SearchingForAddons}
En plus de pouvoir parcourir toutes les extensions disponibles, il est possible de filtrer les extensions affichées.
Pour effectuer une recherche, appuyez sur `alt+r` pour accéder au champ "Recherche" et tapez le texte à rechercher.
La recherche vérifie les correspondances dans les champs ID, nom affiché, éditeur, auteur ou description de l'extension.
La liste se met à jour au cours de la saisie des termes de recherche.
Une fois la saisie terminée, appuyez sur `tab` pour accéder à la liste filtrée des extensions et parcourir les résultats.

#### Installer des extensions {#InstallingAddons}

Pour installer une extension :

1. Lorsque le focus se trouve sur une extension que vous souhaitez installer, appuyez sur `entrée`.
1. Le menu d'actions s'ouvre avec une liste d'actions ; la première action est "Installer".
1. Pour installer l'extension, appuyez sur `i` ou `flècheBas` pour atteindre "Installer" et appuyez sur `entrée`.
1. Le focus revient sur l'extension dans la liste et NVDA lira les détails de cette extension.
1. L'information "État" annoncée par NVDA passent de "Disponible" à "Téléchargement en cours".
1. Une fois le téléchargement de l'extension terminé, elle passe à l'état "Téléchargé, en attente d'installation".
1. Répétez cette procédure pour toutes les extensions que vous souhaitez également installer.
1. Une fois que vous avez fini, appuyez sur `tab` jusqu'à ce que le focus soit sur le bouton "Fermer", puis appuyez sur `entrée`.
1. Les extensions téléchargées démarreront leur processus d'installation dès la fermeture de l'Add-on Store.
Pendant le processus d'installation, les extensions peuvent afficher des boîtes de dialogue auxquelles vous devrez répondre.
1. Une fois que les extensions sont installées, une boîte de dialogue apparaît vous informant que des modifications ont été apportées et vous devez redémarrer NVDA pour que l'installation des extensions soit terminée.
1. Appuyez sur `entrée` pour redémarrer NVDA.

#### Gérer les extensions {#ManagingInstalledAddons}
Appuyez sur `contrôle+tab` pour vous déplacer entre les onglets de l'Add-on Store.
Les onglets sont : "Extensions installées", "Mises à jour", "Extensions disponibles" et "Extensions incompatibles installés".
Chacun des onglets est présenté de manière similaire, sous la forme d'une liste d'extensions, d'un panneau pour plus de détails sur l'extension sélectionné et d'un bouton pour effectuer des actions pour l'extension sélectionnée.
Le menu d'actions des extensions installés comprend les actions "Désactiver" et "Supprimer" au lieu de "Installer".
La désactivation d'une extension empêche NVDA de la charger, mais la garde installée.
Pour réactiver une extension désactivée, appuyez sur "Activer" dans le menu actions.
Après avoir activé, désactivé ou supprimé des extensions, vous serez invité à redémarrer NVDA lors de la fermeture de l'Add-on Store.
Ces modifications ne prendront effet qu'une fois NVDA redémarré.
Veuillez noter que dans la fenêtre de l'Add-on Store, `échap` fonctionne de la même manière que le bouton Fermer.

#### Mettre à jour des extensions {#UpdatingAddons}
Lorsqu'une mise à jour pour une extension que vous avez installée est disponible, elle sera listée dans l'onglet "Mises à jour".
Appuyez sur `contrôle+tab` pour accéder à cet onglet depuis n'importe où dans l'Add-on Store.
L'état de l'extension sera "Mise à jour disponible".
La liste indiquera la version actuellement installée et la version disponible.
Appuyez sur `entrée` sur l'extension pour ouvrir la liste d'actions ; choisissez "Mettre à jour".

### Communauté {#Community}

NVDA a une communauté d'utilisateurs dynamique.
Il existe une [liste de diffusion  principale en anglais](https://nvda.groups.io/g/nvda) et une page complète de [groupes de langues locales](https://github.com/nvaccess/nvda-community/wiki/Connect) .
NV Access, développeur de NVDA, est actif sur Twitter [Twitter](https://twitter.com/nvaccess) et [Facebook](https://www.facebook.com/NVAccess).
NV Access a également un [blog In-Process](https://www.nvaccess.org/category/in-process/) régulier.

Il existe également un programme [NVDA Certified Expert](https://certification.nvaccess.org/).
Il s'agit d'un examen en ligne que vous pouvez passer pour démontrer vos compétences dans NVDA.
[Les experts certifiés NVDA](https://certification.nvaccess.org/) peuvent répertorier leurs coordonnées et les détails commerciaux pertinents.

### Obtenir de l'aide {#GettingHelp}

Pour obtenir de l'aide sur NVDA, appuyez sur `NVDA+n` pour ouvrir le menu, puis sur `h` pour obtenir de l'aide.
À partir de ce sous-menu, vous pouvez accéder au Guide de l'utilisateur, à une référence rapide des commandes, à l'historique des nouvelles fonctionnalités et bien plus encore.
Ces trois premières options s'ouvrent dans le navigateur Web par défaut.
Il existe également du matériel de formation plus complet (en anglais) disponible dans la [Boutique NV Access](https://www.nvaccess.org/shop).

Nous vous recommandons de commencer par le module "Formation de base pour NVDA".
Ce module couvre les concepts allant de la mise en route à la navigation sur le Web et à l'utilisation de la navigation par objet.
Il est disponible en :

* [Texte électronique](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), qui inclut les formats Word DOCX, page Web HTML, eBook ePub et Kindle KFX.
* [Lecture vocale (voix humaine), audio mp3](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Version papier Braille UEB](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) avec livraison incluse partout dans le monde.

D'autres modules, et le [Pack de productivité NVDA](https://www.nvaccess.org/product/nvda-productivity-bundle/) à prix réduit, sont disponibles dans la [Boutique NV Access](https://www.nvaccess.org/shop/).

NV Access vend également une [assistance téléphonique](https://www.nvaccess.org/product/nvda-telephone-support/), soit en blocs, soit dans le cadre du [Pack de Productivité NVDA](https://www.nvaccess.org/product/nvda-productivity-bundle/).
L'assistance téléphonique est disponible pour les numéros situés en Australie et aux États-Unis.

Les [groupes d'utilisateurs par e-mail](https://github.com/nvaccess/nvda/wiki/Connect) sont une excellente source d'aide communautaire, tout comme les [experts NVDA certifiés](https://certification.nvaccess.org/).

Vous pouvez créer des rapports de bogues ou des demandes de fonctionnalités via [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
Les [contribution guidelines](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) (en anglais) contiennent des informations précieuses pour contribuer à la communauté.

## Plus d'Options de Configuration {#MoreSetupOptions}
### Options d'Installation {#InstallingNVDA}

Si vous installez NVDA directement depuis le lanceur NVDA téléchargé, appuyez sur le bouton Installer NVDA.
Si vous avez déjà fermé ce dialogue ou souhaitez installer à partir d'une copie portable, veuillez choisir l'élément de menu Installer NVDA qui se trouve sous Outils dans le menu NVDA.

Le dialogue d'installation qui apparaît demandera de confirmer si vous souhaitez installer NVDA et vous indiquera également si cette installation mettra à jour une installation précédente.
Appuyez sur le bouton Continuer pour lancer l'installation de NVDA.
Il y a aussi quelques options dans ce dialogue qui sont expliquées ci-dessous.
Une fois l'installation terminée, un message apparaîtra vous indiquant qu'elle a réussi.
Appuyer sur OK à ce stade redémarrera la copie nouvellement installée de NVDA.

#### Avertissement d'extensions incompatibles {#InstallWithIncompatibleAddons}

Si vous avez déjà installé des extensions, il peut également y avoir un avertissement indiquant que les extensions incompatibles seront désactivées.
Avant de pouvoir presser le bouton Continuer, vous devrez utiliser la case à cocher pour confirmer que vous comprenez que ces extensions seront désactivées.
Il y aura également un bouton pour lister les extensions qui seront désactivées.
Veuillez consulter la section [dialogue des extensions incompatibles](#incompatibleAddonsManager) pour plus d'aide concernant ce bouton.
Après l'installation, vous pouvez réactiver les extensions incompatibles à vos risques et périls à partir de l'[Add-on Store](#AddonsManager).

#### Utiliser NVDA lors de la connexion {#StartAtWindowsLogon}

Cette option vous permet de choisir si NVDA doit ou non démarrer automatiquement lorsque vous êtes sur l'écran de connexion Windows, avant que vous ayez entré un mot de passe.
Cela inclut également le contrôle de compte d'utilisateur et [autres écrans sécurisés](#SecureScreens).
Cette option est activée par défaut pour les nouvelles installations.

#### Créer un raccourci sur le bureau (ctrl+alt+n) {#CreateDesktopShortcut}

Cette option vous permet de choisir si NVDA doit ou non créer un raccourci sur le bureau pour démarrer NVDA.
S'il est créé, ce raccourci se verra également attribuer une touche de raccourci `contrôle+alt+n`, vous permettant de démarrer NVDA à tout moment avec cette touche.

#### Copier la configuration portable sur le compte d'utilisateur actuel {#CopyPortableConfigurationToCurrentUserAccount}

Cette option vous permet de choisir si NVDA doit ou non copier la configuration utilisateur de NVDA en cours d'exécution dans la configuration de l'utilisateur actuellement connecté, pour la copie installée de NVDA.
Cela ne copiera pas la configuration pour les autres utilisateurs de ce système ni dans la configuration du système à utiliser lors de la connexion à Windows et [autres écrans sécurisés](#SecureScreens).
Cette option n'est disponible que lors de l'installation à partir d'une copie portable, et non lors de l'installation directement à partir du Lanceur téléchargé.

### Création d'une copie portable {#CreatingAPortableCopy}

Si vous créez une copie portable directement à partir du package de téléchargement NVDA, appuyez sur le bouton Créer une copie portable.
Si vous avez déjà fermé ce dialogue ou si vous exécutez une copie installée de NVDA, choisissez l'élément de menu Créer une copie portable qui se trouve sous Outils dans le menu NVDA.

Le dialogue qui apparaît vous permet de choisir où la copie portable doit être créée.
Il peut s'agir d'un répertoire sur votre disque dur ou d'un emplacement sur une clé USB ou un autre support portable.
Il existe également une option pour choisir si NVDA doit copier la configuration NVDA actuelle de l'utilisateur connecté pour l'utiliser avec la copie portable nouvellement créée.
Cette option n'est disponible que lors de la création d'une copie portable à partir d'une copie installée, pas lors de la création à partir du package de téléchargement.
Appuyer sur Continuer créera la copie portable.
Une fois la création terminée, un message apparaîtra vous indiquant qu'elle a réussi.
Appuyez sur OK pour fermer ce dialogue.

### Restrictions des Versions Portables et Temporaires {#PortableAndTemporaryCopyRestrictions}

Si vous souhaitez emporter NVDA avec vous sur une clé USB ou un autre support inscriptible, vous devez choisir de créer une copie portable.
La copie installée est également capable de créer une copie portable d'elle-même à tout moment.
La copie portable a également la capacité de s'installer sur n'importe quel ordinateur ultérieurement.
Cependant, si vous souhaitez copier NVDA sur un support en lecture seule tel qu'un CD, vous devez simplement copier le package de téléchargement.
L'exécution de la version portable directement à partir d'un support en lecture seule n'est pas prise en charge pour le moment.

Le [programme d'installation de NVDA](#StepsForRunningTheDownloadLauncher) peut être utilisé comme une copie temporaire de NVDA.
Les copies temporaires empêchent l'enregistrement des paramètres de NVDA.
Cela inclut la désactivation de l'utilisation de l'[Add-on Store](#AddonsManager).

Les copies portables et temporaires de NVDA ont les restrictions suivantes :

* L'impossibilité de démarrer automatiquement pendant et/ou après la connexion.
* L'impossibilité d'interagir avec les applications démarrées avec les privilèges administrateur, sauf bien sûr si NVDA a été démarré avec ces privilèges (non recommandé) ;
* L'impossibilité de lire les écrans de contrôle de compte utilisateur (UAC) lorsque l'on tente de démarrer une application avec les privilèges administrateur ;
* L'impossibilité d'utiliser un écran tactile comme support d'entrée ;
* L'impossibilité de prendre en charge des fonctionnalités comme le mode navigation ou l'annonce des caractères saisis dans les applications du Windows Store.
* L'atténuation audio n'est pas supportée.

## Prendre en Main NVDA {#GettingStartedWithNVDA}
### Démarrer NVDA {#LaunchingNVDA}

Si NVDA a été installé à l'aide de l'installateur, alors il suffit, soit de frapper la combinaison contrôle+alt+n, soit de choisir dans le menu Démarrer / Programmes / NVDA / NVDA.
De plus, Vous pouvez taper NVDA dans le dialogue "Exécuter" puis appuyer sur "Entrée".
Si NVDA est déjà en cours d'exécution, il sera redémarré.
Vous pouvez aussi ajouter quelques [options de ligne de commande](#CommandLineOptions) vous permettant de quitter (-q), désactiver les extensions (--disable-addons), etc.

Pour les copies installées, NVDA enregistre la configuration dans le dossier de données applicatives roaming de l'utilisateur courant par défaut (ex : "`C:\Users\<user>\AppData\Roaming`").
Il est possible de modifier cela de manière à ce que NVDA charge sa configuration depuis le dossier de données applicatives local.
Consultez la section concernant les [paramètres système](#SystemWideParameters) pour plus de détails.

Pour démarrer la copie portable, rendez-vous dans le dossier où NVDA a été décompressé, et appuyez sur "Entrée" ou double-cliquez sur nvda.exe.
Si NVDA est déjà en cours d'exécution, il s'arrêtera pour démarrer la version portable.

Au démarrage de NVDA, on entend d'abord une série de sons ascendants (indiquant que NVDA se charge).
Suivant la rapidité de votre ordinateur, ou si vous exécutez NVDA à partir d'une clé USB ou d'un autre périphérique lent, le démarrage peut demander un certain temps.
Si le démarrage est vraiment lent, vous entendrez le message "Chargement de NVDA, veuillez patienter...".

Si vous n'entendez rien de tout cela, ou si vous entendez le signal sonore d'erreur de Windows, ou une série de sons descendants, cela indique un problème de NVDA et vous pourrez, si vous le voulez, envoyer un rapport d'erreur aux développeurs.
Reportez-vous au site Web de NVDA pour les détails de la procédure.

#### Dialogue de Bienvenue {#WelcomeDialog}

Quand NVDA démarre pour la première fois, vous êtes accueilli par un dialogue vous donnant des informations de base sur la touche NVDA et le menu NVDA.
Veuillez consulter les sections ci-après pour plus d'informations sur ces sujets.
Le dialogue contient également une liste déroulante et trois cases à cocher.
La liste déroulante vous permet de sélectionner la configuration clavier.
La première case à cocher vous permet de choisir si vous voulez utiliser la touche de verrouillage majuscules comme touche NVDA.
La deuxième spécifie si NVDA doit démarrer à l'ouverture de votre session et est disponible uniquement sur la version installée.
La troisième permet d'indiquer si ce dialogue d'accueil doit apparaître à chaque démarrage.

#### Dialogue de statistiques d'utilisation des données {#UsageStatsDialog}

Depuis NVDA 2018.3, il est demandé à l'utilisateur s'il veut autoriser l'envoi de données d'utilisation à NV Access afin d'aider à l'amélioration de NVDA à l'avenir.
Au premier démarrage de NVDA, un dialogue vous demandant si vous désirer envoyer des données à NV Access durant l'utilisation de NVDA apparaîtra.
Vous pouvez obtenir plus d'informations concernant les données recueillies par NV Access dans la section paramètres généraux, [Autoriser NV Access à recueillir des statistiques d'utilisation](#GeneralSettingsGatherUsageStats).
Note : l'appui sur "oui" ou "non" sauvegardera ce choix et ce dialogue n'apparaîtra plus à moins que vous réinstalliez NVDA.
Cependant, vous pouvez activer ou désactiver le processus de collecte de données manuellement dans l'écran de paramètres généraux de NVDA. Pour modifier ce paramètre manuellement, vous pouvez cocher ou décocher la case appelée [Autoriser le projet NVDA à recueillir des statistiques d'utilisation](#GeneralSettingsGatherUsageStats).

### À Propos des Commandes Clavier de NVDA {#AboutNVDAKeyboardCommands}
#### La Touche NVDA {#TheNVDAModifierKey}

La plupart des commandes spécifiques de NVDA se font en appuyant sur la touche NVDA en conjonction avec une ou plusieurs autres touches.
Les fonctions de revue de texte qui n'utilisent que le pavé numérique constituent une des quelques exceptions.

NVDA peut être configuré pour que les touches "Insert" du pavé numérique, "Insert" du clavier étendu ou verrouillage majuscules puissent être utilisées comme touche NVDA.
Par défaut, les touches "Insert" du pavé numérique et du clavier étendu sont définies comme touche NVDA.

Si vous souhaitez que l'une des touches NVDA se comporte comme d'habitude, comme si NVDA n'était pas en cours d'exécution (par exemple si vous voulez utiliser verrouillage majuscules pour verrouiller les majuscules après l'avoir définie comme touche NVDA) vous devrez appuyer deux fois rapidement sur la touche.

#### Les Configurations Clavier {#KeyboardLayouts}

NVDA comporte actuellement deux configurations clavier : une pour les ordinateurs de bureau (Desktop) et une pour les ordinateurs portables (Laptop).
Par défaut, NVDA est configuré pour un ordinateur de bureau. Pour passer en configuration ordinateur portable, allez dans la catégorie Clavier du dialogue [Paramètres](#NVDASettings) qui se trouve dans le menu Préférences de NVDA.

La configuration pour ordinateur de bureau fait un usage intensif du pavé numérique (avec le verrouillage numérique désactivé).
Bien que la plupart des ordinateurs portables ne comportent pas de pavé numérique, certains peuvent l'émuler en maintenant enfoncée la touche "FN" puis en appuyant sur les lettres et les chiffres à la droite du clavier ( 7 8 9 u i o j k l etc.).
Si votre ordinateur portable ne peut pas le faire ou ne vous permet pas de désactiver le verrouillage numérique, vous pourrez alors basculer vers la disposition Ordinateur Portable.

### Gestes Tactiles de NVDA {#NVDATouchGestures}

Si vous utilisez NVDA sur un système possédant un écran tactile, vous pouvez aussi contrôler NVDA directement via l'écran tactile.
Tant que NVDA est actif, à moins que le support de l'interaction tactile soit désactivée, toutes les manipulations sur l'écran tactile vont directement à NVDA.
Ainsi, toutes les actions qui peuvent être faites normalement sans NVDA ne fonctionneront pas.
<!-- KC:beginInclude -->
Pour activer/désactiver le support d'interaction tactile, pressez NVDA+contrôle+alt+t.
<!-- KC:endInclude -->
Vous pouvez aussi activer ou désactiver le [support d'interaction tactile](#TouchSupportEnable) depuis la catégorie Interaction Tactile des paramètres de NVDA.

#### Explorer l'Écran {#ExploringTheScreen}

L'action la plus basique que vous pouvez effectuer avec l'écran tactile est d'obtenir l'annonce du texte ou de l'élément à n'importe quel point de l'écran.
Pour ce faire, placez un doigt n'importe où sur l'écran.
Vous pouvez également garder votre doigt sur l'écran et le déplacer pour lire les autres éléments et textes sur lesquels votre doigt se place.

#### Gestes Tactiles {#TouchGestures}

Lorsque les commandes NVDA sont décrites dans ce guide utilisateur, elles peuvent comporter un geste tactile qui peut être utilisé pour activer cette commande avec l'écran tactile.
Voici quelques instructions sur la manière d'effectuer les différents gestes tactiles.

##### Tapes {#Taps}

Tapoter rapidement sur l'écran avec un ou plusieurs doigts.

Tapoter une fois avec un seul doigt s'appelle une simple tape.
Tapoter une fois avec deux doigts s'appelle une tape à deux doigts et ainsi de suite.

Si la même tape est faite une fois ou plus dans une succession rapide, NVDA la prendra comme un geste tactile multi-tape.
Tapoter deux fois sera une double-tape.
Tapoter trois fois sera une triple-tape et ainsi de suite.
Bien sûr, ces gestes à tapes multiples reconnaissent combien de doigts sont utilisés, il est donc possible d'avoir des gestes tel qu'une triple-tape à deux doigts, ou une tape à quatre doigts, etc.

##### Glisser {#Flicks}

Glissez rapidement votre doigt sur l'écran.

On peut glisser dans les quatre directions : glissé gauche, glissé droite, glissé bas, glissé haut.

Exactement comme pour les tapes, il est possible d'utiliser plusieurs doigts.
Il est donc possible d'avoir un glissé à deux doigts vers le haut ou trois vers la droite.

#### Modes Tactiles {#TouchModes}

Comme il y a plus de commandes NVDA que de gestes tactiles possibles, NVDA a plusieurs modes tactiles entre lesquels on peut basculer, qui rendent un certain nombre de commandes disponibles.
Les deux modes sont le mode texte et le mode objet.
Certaines commandes listées dans ce manuel peuvent avoir un mode indiqué entre parenthèses après le geste.
Par exemple, glissé haut (mode texte) signifie que cette commande sera exécutée si vous glissez vers le haut, mais seulement en mode texte.
Si la commande n'a aucun mode associé, le geste fonctionnera dans tous les modes.

<!-- KC:beginInclude -->
Pour basculer entre les modes, faites une tape avec trois doigts.
<!-- KC:endInclude -->

#### Clavier Tactile {#TouchKeyboard}

Le clavier tactile sert à entrer du texte et des commandes à partir d'un écran tactile.
Quand le focus est sur un champ de saisie, vous pouvez faire apparaître le clavier tactile d'une double-tape sur l'icône du clavier tactile au bas de l'écran.
Sur les tablettes comme la Microsoft Surface Pro, le clavier tactile est toujours disponible quand le clavier est déconnecté
Pour masquer le clavier tactile, faites une double-tape sur son icône ou quittez la zone de saisie.

Quand le clavier tactile est activé, pour repérer une touche, placez vos doigts à l'endroit où se situe le clavier tactile (généralement au bas de l'écran), puis déplacez-vous sur le clavier avec un doigt.
Quand vous avez trouvé la touche que vous voulez presser, double-tapez la touche ou retirez votre doigt, selon les options définies dans la catégorie [Paramètres d'Interaction Tactile](#TouchInteraction)des Paramètres NVDA.

### Aide des Commandes {#InputHelpMode}

Des commandes clavier et tactiles sont mentionnées tout au long de ce guide utilisateur, mais une manière simple d'explorer les différentes touches de commandes est d'activer l'aide clavier.

Pour activer l'aide clavier, appuyez sur NVDA+1.
Pour la désactiver, appuyez à nouveau sur NVDA+1.
Quand l'aide clavier est activée, l'appui sur une touche braille ou clavier, ou faire un geste à l'écran tactile annonce sa fonction (si elle en a une).
La fonction n'est pas réellement exécutée, vous pouvez donc appuyer sur n'importe quelle touche sans crainte.

### Le Menu NVDA {#TheNVDAMenu}

Le menu NVDA vous permet de gérer les paramètres de NVDA, d'obtenir de l'aide, sauvegarder ou recharger la configuration, modifier le dictionnaire de prononciation, accéder à des outils additionnels ou quitter NVDA.

Pour accéder au menu NVDA depuis n'importe où dans Windows pendant que NVDA est en cours d'exécution, vous pouvez effectuer l'une des actions suivantes :

* appuyez sur `NVDA+n` sur le clavier.
* Effectuez une double-tape à 2 doigts sur l'écran tactile.
* Accédez à la barre d'état système en appuyant sur `Windows+b`, `flècheBas` jusqu'à l'icône NVDA, et appuyez sur `entrée`.
* Alternativement, accédez à la barre d'état système en appuyant sur `Windows+b`, `flècheBas` jusqu'à l'icône NVDA, et ouvrez le menu contextuel en appuyant sur la touche `applications` située à côté de la touche de contrôle droite sur la plupart des claviers.
Sur un clavier sans touche `applications`, appuyez sur `maj+f10` à la place.
* Faites un clic droit sur l'icône NVDA située dans la barre d'état système de Windows

Lorsque le menu apparaît, vous pouvez utiliser les touches fléchées pour naviguer dans le menu et la touche `entrée` pour activer un élément.

### Commandes de Base {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Tactile |Description|
|---|---|---|---|---|
|Démarrer ou redémarrer NVDA |Contrôle+alt+n |Contrôle+alt+n |aucun |Démarre ou redémarre NVDA depuis le bureau, si ce raccourci Windows est activé durant le processus d'installation de NVDA. Ceci est un raccourci spécifique à Windows et de ce fait il ne peut être réassigné dans le dialogue gestes de commandes.|
|Arrêt parole |Contrôle |Contrôle |tape 2 doigts |Arrêt instantané de la parole|
|Pause parole |Maj |Maj |Aucun |Pause instantanée de la parole, un second appui reprend la parole là où elle s'était arrêtée|
|Menu NVDA |NVDA+n |NVDA+n |Double-tape 2 doigts |Affiche le menu NVDA pour vous permettre d'accéder aux préférences, outils, aide etc.|
|Passage en mode aide à la saisie |NVDA+1 |NVDA+1 |Aucun |Dans ce mode, l'appui sur n'importe quelle touche donnera son nom et la description de la commande NVDA qui lui est éventuellement associée|
|Quitter NVDA |NVDA+q |NVDA+q |Aucun |Quitter NVDA|
|Ignorer la touche suivante |NVDA+f2 |NVDA+f2 |Aucun |Indique à NVDA de passer la touche suivante directement à l'application - même si cette touche correspond normalement à une commande NVDA|
|Bascule du mode veille |NVDA+maj+s |NVDA+maj+z |Aucun |Le mode veille désactive toutes les commandes NVDA ainsi que la parole et le braille pour l'application en cours. Ceci est utile dans les applications fournissant leur propre système de revue d'écran. Appuyez à nouveau la combinaison pour désactiver le mode veille.|

<!-- KC:endInclude -->

### Annonce des Informations système {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Annoncer date/heure |NVDA+f12 |Un appui annonce l'heure, deux appuis annoncent la date|
|Annoncer l'état de la batterie |NVDA+maj+b |Annonce le pourcentage de charge de la batterie ou si l'adaptateur secteur est connectée|
|Annoncer le contenu du presse-papiers |NVDA+c |Lit le contenu du presse-papier s'il y a lieu|

<!-- KC:endInclude -->

### Mode de parole {#SpeechModes}

Le mode de parole détermine la façon dont le contenu de l'écran, les notifications, les réponses aux commandes et autres sorties sont prononcés pendant le fonctionnement de NVDA.
Le mode par défaut est "activée", où la parole est utilisée dans les situations attendues lors de l'utilisation d'un lecteur d'écran.
Cependant, dans certaines circonstances, ou lors de l'exécution de programmes particuliers, l'un des autres modes de parole peut s'avérer utile.

Les quatre modes de parole disponibles sont :

* Activée (par défaut) : NVDA parlera normalement en réaction aux changements d'écran, aux notifications et aux actions telles que déplacer le focus ou émettre des commandes.
* À la demande : NVDA ne parlera que lorsque vous utilisez des commandes avec une fonction d'annonce (par exemple annoncer le titre de la fenêtre) ; mais il ne parlera pas en réaction à des actions telles que le déplacement du focus ou du curseur.
* Désactivée : NVDA ne dira rien, mais contrairement au mode veille, il réagira silencieusement aux commandes.
* remplacée par des bips : NVDA remplacera la parole normale par des bips courts.

Le mode bips peut être utile lorsqu'une sortie très importante défile dans une fenêtre de terminal, mais vous ne vous souciez pas de ce que c'est, seulement du fait qu'elle continue à défiler ; ou dans d’autres circonstances où le fait qu’il y ait une sortie est plus pertinent que la production elle-même.

Le mode À la demande peut s'avérer utile lorsque vous n'avez pas besoin d'un retour constant sur ce qui se passe à l'écran ou sur l'ordinateur, mais que vous devez périodiquement vérifier des éléments particuliers à l'aide de commandes de revue, etc.
Les exemples incluent lors d'un enregistrement audio, lors de l'utilisation d'un agrandissement de l'écran, lors d'une réunion ou d'un appel, ou comme alternative au mode bips.

Un geste permet de parcourir les différents modes de parole :
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Faire défiler les modes de parole |`NVDA+s` |Passer d’un mode vocal à l’autre|

<!-- KC:endInclude -->

Si vous avez seulement besoin de basculer entre un sous-ensemble limité de modes de parole, voir [Modes disponibles dans la commande Faire défiler les modes de parole](#SpeechModesDisabling) pour savoir comment désactiver les modes non souhaités.

## Naviguer avec NVDA {#NavigatingWithNVDA}

NVDA vous permet de naviguer dans le système ou de l'explorer de différentes manières, soit en interaction normale, soit en revue.

### Objets {#Objects}

Chaque application et le système d'exploitation lui-même se composent d'un grand nombre d'objets.
Un objet est un élément simple tel qu'un morceau de texte, un bouton, une case à cocher, un potentiomètre, une liste ou une zone d'édition.

### Naviguer avec le Focus Système {#SystemFocus}

Le focus système, ou plus simplement focus, est [l'objet](#Objects) qui reçoit les touches tapées au clavier.
Par exemple, si vous tapez du texte dans une zone d'édition, cette zone d'édition a le focus.

La manière la plus commune de naviguer dans Windows avec NVDA, est de simplement se déplacer avec des commandes clavier normales, comme "Tabulation" et "Majuscule+Tabulation" pour se déplacer entre les contrôles, "Alt" pour aller au menu puis "Flèches" pour naviguer dans les menus, utiliser "Alt+Tabulation" pour passer d'une application à l'autre. Cela déplace le focus système, c'est-à-dire l'objet qui reçoit les touches que vous tapez au clavier.
Quand vous faites cela, NVDA donne des informations sur l'objet ayant le focus, telles que son nom, son type, son état, sa valeur, sa description, son raccourci clavier et sa position.
Quand la [Mise en Évidence Visuelle](#VisionFocusHighlight) est activée, la position du focus système courant est également présentée visuellement.

Quelques touches de commandes utiles pour naviguer avec le focus :
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Description|
|---|---|---|---|
|Annonce du focus courant |NVDA+tab |NVDA+tab |Annonce l'objet en cours ou le contrôle qui a le focus système. Un double appui épelle l'information|
|Annonce du titre |NVDA+t |NVDA+t |Annonce le titre de la fenêtre active. Un double appui épelle l'information, un triple appui la copie dans le presse-papiers|
|Lecture de la fenêtre active |NVDA+b |NVDA+b |lit tous les contrôles de la fenêtre active (utile pour les dialogues)|
|Annonce de la barre d'état |NVDA+fin |NVDA+maj+fin |Lit la barre d'état si NVDA en trouve une. Un double appui épelle l'information. Un triple appui la copie dans le presse-papiers|
|Annoncer le Raccourci Clavier |`maj+pavnum2` |`NVDA+contrôle+maj+point-virgule` |Annonce le raccourci clavier (accélérateur) de l'objet actuellement en focus|

<!-- KC:endInclude -->

### Naviguer avec le Curseur Système {#SystemCaret}

Quand un [objet](#Objects) qui autorise la navigation ou l'édition de texte a le [focus](#SystemFocus), vous pouvez vous déplacer dans le texte en utilisant le curseur système ou curseur d'édition.

Quand le focus est sur un objet ayant un curseur d'édition, vous pouvez utiliser les flèches, les touches début, fin, page précédente, page suivante pour vous déplacer dans le texte.
Vous pouvez également modifier le texte si le champ le permet.
NVDA annonce le déplacement par caractère, mot ou ligne, et annonce aussi la sélection et la désélection de texte.

NVDA fournit les commandes clavier suivantes relatives au curseur système :
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Description|
|---|---|---|---|
|Dire tout |NVDA+flèche bas |NVDA+a |Démarre la lecture depuis la position du curseur système en lui faisant suivre la lecture|
|Lire ligne courante |NVDA+flèche haut |NVDA+l |Lit la ligne où se trouve le curseur système. Un double appui épelle la ligne. Un triple appui l'épelle en code international.|
|Lire texte sélectionné |NVDA+Maj+flèche haut |NVDA+Maj+s |Lit tout le texte actuellement sélectionné|
|Annoncer la mise en forme du texte |NVDA+f |NVDA+f |annonce la mise en forme du texte à la position actuelle du curseur. Un double appui présente l'information en mode navigation|
|Annoncer la destination du lien |`NVDA+k` |`NVDA+k` |Un appui annonce l'URL de destination du lien à la position courante du curseur ou du focus. Deux appuis l'affichent dans une fenêtre pour une revue plus attentive|
|Annoncer la position du curseur |NVDA+pavnumEffacement |NVDA+effacement |Annonce des informations sur l'emplacement du texte ou de l'objet à la position du curseur système. Par exemple, cela peut inclure le pourcentage dans le document, la distance depuis le bord de la page ou la position exacte sur l'écran. Appuyer deux fois peut fournir plus de détails.|
|Phrase suivante |alt+flècheBas |alt+flècheBas |Amène le curseur à la phrase suivante et la lit. (Supporté seulement sous Microsoft Word et Outlook)|
|Phrase précédente |alt+flècheHaut |alt+flècheHaut |Amène le curseur à la phrase précédente et la lit. (Supporté seulement sous Microsoft Word et Outlook)|

Dans un tableau, vous disposez également des touches de commandes suivantes :

| Nom |Touche |Description|
|---|---|---|
|Aller à la colonne précédente |contrôle+alt+flèche gauche |Déplace le curseur système à la colonne précédente en restant sur la même ligne|
|Aller à la colonne suivante |contrôle+alt+flèche droite |Déplace le curseur système à la colonne suivante en restant sur la même ligne|
|Aller à la ligne précédente |contrôle+alt+flèche haut |Déplace le curseur système à la ligne précédente en restant sur la même colonne|
|Aller à la ligne suivante |contrôle+alt+flèche bas |Déplace le curseur système à la ligne suivante en restant sur la même colonne|
|Aller à la première colonne |contrôle+alt+début |Déplace le curseur système à la première colonne (en restant sur la même ligne)|
|Aller à la dernière colonne |contrôle+alt+fin |Déplace le curseur système à la dernière colonne (en restant sur la même ligne)|
|Aller à la première ligne |contrôle+alt+PagePrec |Déplace le curseur système à la première ligne (en restant sur la même colonne)|
|Aller à la dernière ligne |contrôle+alt+pageSuiv |Déplace le curseur système à la dernière ligne (en restant sur la même colonne)|
|Dire tout dans la colonne |`NVDA+contrôle+alt+flècheBas` |Lit la colonne verticalement depuis la cellule courante jusqu'à la dernière cellule de la colonne.|
|Dire tout dans la ligne |`NVDA+contrôle+alt+flècheDroit` |Lit la ligne horizontalement depuis la cellule courante jusqu'à la dernière cellule de la ligne.|
|Lire toute la colonne |`NVDA+contrôle+alt+flècheHaut` |Lit la colonne courante verticalement du début à la fin sans déplacer le curseur système.|
|Lire toute la ligne |`NVDA+contrôle+alt+flècheGauche` |Lit la ligne courante horizontalement de gauche à droite sans déplacer le curseur système.|

<!-- KC:endInclude -->

### Naviguer par Objet {#ObjectNavigation}

La plupart du temps, vous travaillerez avec les applications en utilisant des commandes qui déplacent le [focus](#SystemFocus) et le [curseur](#SystemCaret).
Cependant, vous pouvez parfois avoir besoin d'explorer l'application en cours ou le système sans déplacer le focus ou le curseur.
Vous pouvez aussi avoir besoin d'accéder à des [objets](#Objects) inaccessibles par les commandes clavier habituelles.
Dans ces cas, vous pouvez utiliser la navigation par objet.

La navigation par objet vous permet de vous déplacer parmi les différents [objets](#Objects) et d'obtenir des informations à leur sujet.
Quand vous atteignez un objet, NVDA l'annoncera de la même manière qu'il annonce le focus système.
Si vous désirez explorer tout le texte tel qu'il se présente à l'écran, vous pouvez également utiliser la [revue d'écran](#ScreenReview).

Pour ne pas avoir à errer entre tous les objets présents dans le système, ceux-ci sont groupés hiérarchiquement.
Cela signifie que vous devez entrer dans certains objets pour voir les objets qu'ils contiennent.
Par exemple, une liste contient des éléments de liste, vous devez donc entrer dans la liste pour voir ces éléments.
Si vous êtes sur un élément de liste, aller à l'élément suivant ou précédent vous amènera à un autre élément de la même liste.
Si vous allez sur l'objet contenant les éléments de la liste, vous serez ramené à la liste.
Vous pourrez alors la quitter si vous désirez accéder à d'autres objets.
De la même manière, une barre d'outils contient des contrôles, vous devrez donc entrer dans la barre d'outils pour accéder aux contrôles qu'elle contient.

Si vous préférez plutôt vous déplacer entre chaque objet simple du système, vous pouvez utiliser des commandes pour passer à l'objet précédent/suivant dans une vue à plat.
Par exemple, si vous vous déplacez vers l'objet suivant dans cette vue à plat et que l'objet actuel contient d'autres objets, NVDA se déplacera automatiquement vers le premier objet contenu.
Au contraire, si l'objet courant ne contient aucun objet, NVDA passera à l'objet suivant au niveau courant de la hiérarchie.
S'il n'y a pas d'objet suivant de ce type, NVDA essaiera de trouver l'objet suivant dans la hiérarchie en fonction des objets contenants jusqu'à ce qu'il n'y ait plus d'objets vers lesquels se déplacer.
Les mêmes règles s'appliquent pour reculer dans la hiérarchie.

L'objet en cours de revue s'appelle l'objet navigateur.
Quand vous atteignez un objet, vous pouvez examiner son contenu en utilisant les [commandes de revue de texte](#ReviewingText) en étant en [mode Revue d'objet](#ObjectReview).
Quand la [Mise en Évidence Visuelle](#VisionFocusHighlight) est activée, la position de l'objet navigateur courant est également présentée visuellement.
Par défaut, l'objet navigateur suit le focus système, mais ce comportement peut être désactivé.

Note : Le suivi de la Navigation par Objet par le Braille peut être configuré via [Braille Suit](#BrailleTether).

Pour naviguer par objet, utilisez les commandes suivantes :

<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Tactile |Description|
|---|---|---|---|---|
|Annonce de l'objet courant |NVDA+pavnum5 |NVDA+Maj+o |Aucun |Annonce l'objet navigateur courant, deux appuis épellent l'information, trois appuis copient le nom et le contenu de l'objet dans le presse-papiers|
|Aller à l'objet parent |NVDA+pavnum8 |NVDA+maj+flèche haut |Glisser vers le haut (mode objet) |Va à l'objet parent (qui contient l'objet navigateur courant)|
|Aller à l'objet précédent |NVDA+pavnum4 |NVDA+maj+flèchegauche |aucun |Se déplace vers l'objet avant l'objet navigateur courant|
|Aller à l'objet précédent en vue à plat |NVDA+pavnum9 |NVDA+maj+ù |glisser vers la gauche (mode objet) |Passe à l'objet précédent dans une vue à plat de la hiérarchie de navigation d'objets|
|Passer à l'objet suivant |NVDA+pavnum6 |NVDA+maj+flècheDroite |aucun |Se déplace vers l'objet après l'objet navigateur courant|
|Passer à l'objet suivant dans la vue à plat |NVDA+pavnum3 |NVDA+maj+* |glisser vers la droite (mode objet) |Passe à l'objet suivant dans une vue à plat de la hiérarchie de navigation d'objets|
|Aller au premier objet inclus |NVDA+pavnum2 |NVDA+maj+flèche bas |Glisser vers le bas (mode objet) |Va au premier objet inclus dans l'objet navigateur courant|
|Aller à l'objet en focus |NVDA+pavnumMoins |NVDA+retour arrière |Aucun |Va à l'objet ayant le focus système, et place le curseur de revue sur le curseur système s'il est présent|
|Activer l'objet navigateur courant |NVDA+pavnumEntrer |NVDA+entrée |Double tape |Active l'objet navigateur courant (similaire à un clic de souris ou à appuyer la barre d'espace quand l'objet a le focus système)|
|Amener le focus système à l'objet navigateur courant |NVDA+maj+pavnumMoins |NVDA+maj+retour arrière |Aucun |Amène le focus système à l'objet navigateur courant si c'est possible|
|Annoncer la position du curseur de revue |NVDA+pavnumEffacement |NVDA+effacement |Aucun |Annonce la position du texte ou de l'objet sous le curseur de revue. Cela peut inclure, par exemple, le pourcentage dans le document, la distance au bord de la page ou la position exacte sur l'écran. Un double appui annonce éventuellement des informations supplémentaires.|
|Amener le curseur de revue à la barre d'état |aucun |aucun |aucun |Annonce la barre d'état si NVDA en trouve une. Amène également l'objet navigateur à sa position.|

<!-- KC:endInclude -->

Note : Les touches du pavé numérique nécessitent de désactiver le verrouillage numérique pour fonctionner correctement.

### Revue de Texte {#ReviewingText}

NVDA vous permet de lire le contenu de [l'écran](#ScreenReview), du [document](#DocumentReview) ou de [l'objet](#ObjectReview) par caractère, mot ou ligne.
Ceci est particulièrement utile dans la console de commandes Windows et d'autres applications où le [curseur système](#SystemCaret) est inexistant.
Par exemple, cela peut servir à consulter le texte d'un long message dans un dialogue.

Quand vous déplacez le curseur de revue, le curseur système ne bouge pas, ainsi vous pouvez explorer un texte sans perdre votre position d'édition actuelle.
Cependant, par défaut, quand le curseur système bouge, le curseur de revue le suit.
Ceci peut être désactivé.

Note : Le suivi de la Navigation par Objet par le Braille peut être configuré via [Braille Suit](#BrailleTether).

Vous disposez des commandes suivantes pour explorer du texte :
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Tactile |Description|
|---|---|---|---|---|
|Aller à la première ligne en revue |Maj+pavnum7 |NVDA+contrôle+début |Aucun |Amène le curseur de revue à la première ligne du texte|
|Aller à la ligne précédente en revue |pavnum7 |NVDA+flèche haut |Glisser vers le haut (mode texte) |Amène le curseur de revue sur la ligne de texte précédente|
|Annoncer la ligne courante en revue |pavnum8 |NVDA+maj+point-virgule |Aucun |Lit la ligne de texte sous le curseur de revue, un double appui épelle la ligne|
|Aller à la ligne suivante en revue |pavnum9 |NVDA+flèche bas |Glisser vers le bas (mode texte) |Amène le curseur de revue à la ligne de texte suivante|
|Aller à la dernière ligne en revue |maj+pavnum9 |NVDA+contrôle+fin |Aucun |Amène le curseur de revue à la dernière ligne de texte|
|Aller au mot précédent en revue |pavnum4 |NVDA+contrôle+flèche gauche |Glisser vers la gauche 2 doigts (mode texte) |Amène le curseur de revue au mot précédent dans le texte|
|Annoncer le mot courant en revue |pavnum5 |NVDA+contrôle+point-virgule |Aucun |Lit le mot à la position du curseur de revue, un double appui épelle le mot|
|Aller au mot suivant en revue |pavnum6 |NVDA+contrôle+flèche droite |Glisser vers la droite 2 doigts (mode texte) |Amène le curseur de revue au mot suivant|
|Aller au début de la ligne en revue |maj+pavnum1 |NVDA+début |Aucun |Amène le curseur de revue au début de la ligne courante|
|Aller au caractère précédent en revue |pavnum1 |NVDA+flèche gauche |Glisser vers la gauche (mode texte) |Amène le curseur de revue au caractère précédent de la ligne courante|
|Annoncer le caractère courant en revue |pavnum2 |NVDA+point-virgule |Aucun |Annonce le caractère courant sous le curseur de revue, un double appui annonce la valeur du caractère en décimal et hexadécimal|
|Aller au caractère suivant en revue |pavnum3 |NVDA+flèche droite |Glisser vers la droite (mode texte) |Amène le curseur de revue au caractère suivant de la ligne courante|
|Aller en fin de ligne en revue |maj+pavnum3 |NVDA+fin |Aucun |Amène le curseur de revue à la fin de la ligne courante|
|Aller à la page précédente en revue |`NVDA+pagePrec` |`NVDA+maj+pagePrec` |aucune |Amène le curseur de revue à la page précédente de texte si supporté par l'application|
|Aller à la page suivante en revue |`NVDA+pageSuiv` |`NVDA+maj+pageSuiv` |aucune |Amène le curseur de revue à la page suivante de texte si supporté par l'application|
|Dire tout en revue |pavnumPlus |NVDA+maj+a |Glisser vers le bas 3 doigts (mode texte) |Lit en partant de la position du curseur de revue, celui-ci suivant la lecture|
|Sélectionner puis copier à partir du curseur de revue |NVDA+f9 |NVDA+f9 |Aucun |Commence à sélectionner puis copier le texte depuis la position du curseur de revue. La copie ne s'effectue pas tant qu'on n'a pas indiqué la fin du texte à copier|
|Sélectionner puis copier jusqu'au curseur de revue |NVDA+f10 |NVDA+f10 |Aucun |Au premier appui, le texte est sélectionné depuis la position préalablement définie par "copier à partir du curseur de revue" jusqu'à la position actuelle du curseur de revue. Si le curseur système peut atteindre le texte, il sera amené au texte sélectionné. Au second appui, le texte est copié dans le presse-papiers de Windows.|
|aller au marqueur de début de copie en mode revue |NVDA+maj+f9 |NVDA+maj+f9 |aucun |Amène le curseur de revue à la position préalablement définiee comme marqueur de début de copie|
|Annoncer la mise en forme du texte |NVDA+maj+f |NVDA+maj+f |Aucun |Annonce la mise en forme du texte à la position du curseur de revue. Un double appui affiche l'information en mode navigation|
|Annonce le remplacement du symbole courant |Aucun |Aucun |aucun |Dit le symbole à la position du curseur de revue. Un double appui montre le symbole et le texte utilisé pour le remplacer en mode navigation.|

<!-- KC:endInclude -->

Note : Les touches du pavé numérique nécessitent de désactiver le verrouillage numérique pour fonctionner correctement.

Pour vous aider à mémoriser les touches de commandes de la disposition ordinateur de bureau, notez que les commandes de base de revue de texte sont organisées selon une grille de 3 sur 3 avec, de haut en bas, lignes, mots, caractères et, de gauche à droite, précédent, courant, suivant.
La disposition se présente ainsi :

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Ligne précédente |Ligne courante |Ligne suivante|
|Mot précédent |Mot courant |Mot suivant|
|Caractère précédent |Caractère courant |Caractère suivant|

### Modes de Revue {#ReviewModes}

Les commandes de [revue](#ReviewingText) de NVDA permettent de lire le contenu de l'objet courant du navigateur, le document courant ou l'écran, selon le mode de revue sélectionné.

Les commandes suivantes basculent entre les modes de revue :
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Tactile |Description|
|---|---|---|---|---|
|Passer au mode revue suivant |NVDA+pavnum7 |NVDA+PagePrec |Glisser vers le haut 2 doigts |Passe au mode de revue suivant disponible supérieur au mode actuel.|
|Passer au mode revue précédent |NVDA+pavnum1 |NVDA+PageSuiv |Glisser vers le bas 2 doigts |Passe au mode de revue suivant disponible inférieur au mode actuel.|

<!-- KC:endInclude -->

#### Revue d'Objet {#ObjectReview}

En mode revue d'objet, vous pouvez explorer seulement le contenu de [l'objet du navigateur](#ObjectNavigation).
Pour les objets comme les champs d'édition ou les documents basiques, cela sera généralement le texte contenu.
Pour les autres objets, cela peut être le nom ou la valeur.

#### Revue de Document {#DocumentReview}

Quand [l'objet du navigateur](#ObjectNavigation) est dans un document comme une page web ou un document complexe (ex : document Lotus Symphony), il est possible de passer en mode revue de document.
Le mode revue de document vous permet de relire le contenu du document en entier.

En passant du mode revue d'objet au mode revue de document, le curseur de revue se place là où se trouve le navigateur d'objet.
En bougeant le curseur de revue, le navigateur d'objet est déplacé à la même position que le curseur de revue.

Notez que NVDA basculera automatiquement au mode revue de document depuis le mode revue d'objet lors d'un déplacement dans le document en mode navigation.

#### Revue de l'Écran {#ScreenReview}

Le mode revue de l'écran vous permet de lire le texte visible tel qu'il apparaît à l'écran dans l'application courante.
Cela est très similaire aux fonctionnalités mode revue ou curseur souris des autres lecteurs d'écran sous Windows.

En basculant en mode revue de l'écran, le curseur de revue est placé à la position de [l'objet du navigateur](#ObjectNavigation).
En se déplaçant sur l'écran avec le curseur de revue, le navigateur d'objet est déplacé à l'objet trouvé à la position du curseur de revue.

Notez que dans certaines nouvelles applications, NVDA ne pourra pas lire tout ou partie du texte à l'écran, étant donné qu'elles utilisent des techniques d'affichage qui ne peuvent être gérées actuellement.

### Naviguer avec la Souris {#NavigatingWithTheMouse}

Lorsqu'on déplace la souris, NVDA annonce par défaut le texte se trouvant directement sous le pointeur de la souris.
Quand c'est possible, NVDA lira un paragraphe, cependant certains contrôles ne peuvent être lus que par ligne.

NVDA peut être configuré pour annoncer également le type d'[objet](#Objects) sous la souris lors de son déplacement (par exemple liste, bouton, etc.).
Cela peut être utile pour les personnes complètement aveugles car le texte n'est pas toujours suffisant.

NVDA offre à l'utilisateur un moyen d'évaluer la position de la souris sur l'écran en émettant des bips audio représentant les coordonnées de la souris.
Plus la souris est haut sur l'écran, plus les bips sont aigus.
Plus la souris va à gauche ou à droite, plus le son viendra de gauche ou de droite dans la mesure où l'utilisateur possède des haut-parleurs stéréo.

Par défaut, ces fonctions additionnelles de la souris ne sont pas activées.
Si vous voulez en tirer profit, vous pouvez les configurer dans la catégorie [Souris](#MouseSettings) du dialogue [Paramètres](#NVDASettings) qui se trouve dans le menu "Préférences" de NVDA.

Bien qu'une souris physique ou un pavé tactile devrait être utilisée pour naviguer à la souris, NVDA possède quelques commandes clavier liées à la souris :
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Tactile |Description|
|---|---|---|---|---|
|Clic gauche |pavnumDiviser |NVDA+uAccentGrave |Aucun |Simple clic gauche. Le double clic s'obtient par deux appuis rapides|
|Verrouillage du bouton gauche de la souris |maj+pavnumDiviser |NVDA+maj+uAccentGrave |Aucun |Verrouille le bouton gauche de la souris en position enfoncée. Un second appui déverrouille le bouton. Pour glisser-déposer avec la souris, verrouillez le bouton puis déplacez la souris soit physiquement ou par l'une des commandes NVDA prévues à cet effet|
|Clic droit |pavnumMultiplier |NVDA+astérisque |Taper et maintenir |Simple clic droit|
|Verrouillage du bouton droit de la souris |maj+pavnumMultiplier |NVDA+maj+astérisque |Aucun |Verrouille le bouton droit de la souris en position enfoncée, un second appui déverrouille le bouton. Pour glisser-déposer avec la souris, verrouillez le bouton puis déplacez la souris soit physiquement ou par l'une des commandes NVDA prévues à cet effet|
|Amener la souris à l'objet navigateur courant |NVDA+pavnumDiviser |NVDA+maj+m |Aucun |Amène la souris à la position de l'objet navigateur courant puis au curseur de revue|
|Aller à l'objet sous la souris |NVDA+pavnumMultiplier |NVDA+maj+n |Aucun |Amène l'objet navigateur à l'objet situé à la position de la souris|

<!-- KC:endInclude -->

## Le mode Navigation {#BrowseMode}

Les documents complexes, tels que les pages web, sont représentés sous NVDA en utilisant le Mode Navigation.
Cela inclut les documents dans les applications suivantes :

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* Les messages HTML sous Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Les livres supportés sous Amazon Kindle pour PC

Le mode navigation est aussi disponible en option pour les documents Microsoft Word.

Le mode navigation offre une représentation platement textuelle du document dans laquelle on peut se déplacer avec les flèches de navigation.
Dans ce mode, toutes les touches de commandes du [mode curseur](#SystemCaret) fonctionneront (ex : dire tout, annonce de la mise en forme, touches de navigation dans les tableaux etc.).
Quand la [Mise en Évidence Visuelle](#VisionFocusHighlight) est activée, la position du curseur virtuel de mode navigation est également présentée visuellement.
Des informations indiquant si le texte est un lien, un titre etc., sont annoncées avec le texte pendant que vous vous déplacez.

Parfois, vous devrez interagir directement avec les contrôles contenus dans ces documents.
Par exemple, vous devrez le faire pour les zones d'édition et les listes pour pouvoir entrer du texte ou utiliser le curseur pour travailler avec les contrôles.
Cela se fait en passant en mode formulaire, mode dans lequel presque toutes les touches sont passées directement au contrôle.
En mode navigation, par défaut, NVDA passera automatiquement en mode formulaire si vous tabulez ou cliquez sur un champ qui le requiert.
Inversement, tabuler ou cliquer sur un contrôle qui ne requiert pas le mode formulaire rebasculera NVDA en mode navigation.
Appuyer sur la "barre d'espace" ou la touche "entrée" passera également NVDA en mode formulaire si le champ le permet.
Appuyer sur la touche "échap" repassera NVDA en mode navigation.
De plus, vous pouvez aussi passer manuellement NVDA en mode formulaire, après quoi il y restera jusqu'à ce que vous choisissiez de le désactiver.

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Bascule entre mode formulaire et mode navigation |NVDA+espace |Bascule entre le mode formulaire et le mode navigation|
|Quitter le mode formulaire |échap |Retourne en mode navigation si le mode formulaire a préalablement été activé automatiquement|
|Réactualiser le document |NVDA+f5 |Recharge le document en cours, (utile si le contenu de la page semble incomplet. Non disponible sous Microsoft Word et Outlook.)|
|Rechercher |NVDA+contrôle+f |Affiche un dialogue qui vous permet de rechercher du texte dans le document courant. Voir [chercher du texte](#SearchingForText) pour plus d'information|
|Rechercher suivant |NVDA+f3 |Recherche l'occurrence suivante du texte que vous avez préalablement recherché dans le document|
|Rechercher précédent |NVDA+maj+f3 |Recherche l'occurrence précédente du texte que vous avez préalablement recherché dans le document|

<!-- KC:endInclude -->

### Les Touches de Navigation Rapide {#SingleLetterNavigation}

En mode navigation, pour une navigation plus rapide, NVDA dispose de raccourcis clavier où l'appui d'une seule touche amène à certains champs dans le document.
Notez que toutes ces commandes ne sont pas disponibles dans tous les types de documents.

<!-- KC:beginInclude -->
Les touches suivantes permettent d'aller à l'élément suivant. En les combinant avec maj, on retourne à l'élément précédent.

* h : titre
* l : liste
* i : élément de liste
* t : tableau
* k : lien
* n : texte hors lien
* f : champ de formulaire
* u : lien non visité
* v : lien visité
* e : zone d'édition
* b : bouton
* x : case à cocher
* c : liste déroulante
* r : bouton radio
* q : balise de citation
* s : séparateur
* m : cadre
* g : graphique
* d : région
* o : objet embarqué (lecteur audio et vidéo, application, dialogue etc.)
* 1 ... 6 : Titres 1 ... 6.
* a: annotation (commentaire, modification de l'éditeur, etc.)
* `p` : paragraphe de texte
* w: fautes d'orthographe

Pour se déplacer au début ou à la fin des éléments contenants comme les listes et tableaux :

| Nom |Touche |Description|
|---|---|---|
|Aller au début du conteneur |maj+virgule |Se déplace au début du conteneur (liste, tableau etc.) où le curseur est positionné|
|Aller après la fin du conteneur |virgule |Se déplace après la fin du conteneur (liste, tableau etc.) où le curseur se trouve|

<!-- KC:endInclude -->

Quelques applications web comme Gmail, Twitter et Facebook utilisent de simple lettres comme touches de raccourci.
Si vous voulez les utiliser tout en restant capable d'utiliser vos touches curseur en mode navigation, vous pouvez désactiver temporairement les touches de navigation rapide de NVDA.
<!-- KC:beginInclude -->
Pour activer ou désactiver la navigation rapide pour le document courant, pressez NVDA+maj+espace.
<!-- KC:endInclude -->

#### Commande de navigation par paragraphe de texte {#TextNavigationCommand}

Vous pouvez passer au paragraphe de texte suivant ou précédent en appuyant sur `p` ou `maj+p`.
Les paragraphes de texte sont définis comme un groupe de texte qui semble être écrit sous forme de phrases complètes.
Cela peut être utile pour trouver le début du contenu à lire sur diverses pages Web, telles que :

* Les sites d'actualités
* Les forums
* Les articles de blog

Ces commandes peuvent également être utiles pour éviter certains types de contenu, tels que :

* Les publicités
* Les menus
* Les titres

Veuillez noter cependant que même si NVDA fait de son mieux pour identifier les paragraphes de texte, l'algorithme n'est pas parfait et peut parfois commettre des erreurs.
De plus, cette commande est différente des commandes de navigation par paragraphe `contrôle+flècheBas/flècheHaut`.
La navigation par paragraphes de texte saute uniquement entre les paragraphes de texte, tandis que les commandes de navigation par paragraphe amènent le curseur aux paragraphe précédent/suivant, qu'ils contiennent ou non du texte.

#### Autres commandes de navigation {#OtherNavigationCommands}

En plus des commandes de navigation rapide répertoriées ci-dessus, NVDA dispose de commandes auxquelles aucune touche par défaut n'est attribuée.
Pour utiliser ces commandes, vous devez d'abord leur attribuer des gestes à l'aide de la [boîte de dialogue Gestes de commandes](#InputGestures).
Voici une liste des commandes disponibles:

* Article
* Figure
* Regroupement
* Onglet
* Menu item
* Bouton à bascule
* Barre de progression
* Formule mathématique
* Paragraphe aligné verticalement
* Texte de même style
* Texte de style différent

Gardez à l'esprit qu'il existe deux commandes pour chaque type d'élément, pour avancer et reculer dans le document, et vous devez attribuer des gestes aux deux commandes afin de pouvoir naviguer rapidement dans les deux sens.
Par exemple, si vous souhaitez utiliser les touches `y` / `maj+y` pour naviguer rapidement dans les onglets, procédez comme suit:

1. Ouvrez la boîte de dialogue des gestes de commandes à partir du mode navigation.
1. Recherchez l'élément "Aller à l'onglet suivant" dans la section Mode navigation.
1. Attribuez la touche `y` pour le geste trouvé.
1. Recherchez l'élément "Aller à l'onglet précédent".
1. Attribuez `maj+y` pour le geste trouvé.

### La Liste d'Éléments {#ElementsList}

La liste d'éléments donne accès à une liste de différents types d'éléments dans le document, de manière appropriée à l'application.
Par exemple, dans les navigateurs web, la liste d'éléments peut afficher les liens, les titres, les champs de formulaire, les boutons ou les régions.
Des boutons radio vous permettent de choisir entre les différents types d'éléments.
Une zone d'édition est également présente dans le dialogue, elle vous permet de filtrer la liste pour faciliter la recherche d'un élément particulier dans la page.
Quand vous avez choisi un élément, des boutons vous permettent de vous y rendre ou de l'activer.
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Liste d'éléments du document |NVDA+f7 |Liste les différents types d'éléments du document courant|

<!-- KC:endInclude -->

### Chercher du texte {#SearchingForText}

Ce dialogue vous permet de rechercher des termes dans le document courant.
Dans le champ "Entrez le texte à rechercher", le texte à trouver peut être saisi.
La case à cocher "Respecter la casse" force la recherche à différencier les lettres majuscules et minuscules.
Par exemple, quand Respecter la casse est sélectionné, vous trouverez " NV Access " mais pas " nv access ".
Utilisez les touches suivantes pour effectuer des recherches :
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Rechercher du texte |NVDA+contrôle+f |Ouvre le dialogue de recherche|
|Trouver l'occurrence suivante |NVDA+f3 |recherche l'occurrence suivante du terme en cours de recherche|
|Trouver l'occurrence précédente |NVDA+maj+f3 |recherche l'occurrence précédente du terme en cours de recherche|

<!-- KC:endInclude -->

### Les Objets Embarqués {#ImbeddedObjects}

Certaines pages peuvent inclure du contenu riche utilisant des technologies comme Oracle Java et HTML5, tout comme des applications ou des dialogues.
Quand il en rencontre dans un document, NVDA annonce "objet embarqué", "application", ou "dialogue" respectivement.
Vous pouvez vous y rendre rapidement en utilisant les touches de navigation rapide pour objets embarqués o et maj+o.
Pour interagir avec ces objets, vous pouvez presser Entrée sur eux.
Si l'objet est accessible, vous pourrez interagir avec lui comme n'importe quelle autre application.
Une touche de commande permet de retourner à la page contenant l'objet embarqué.
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Aller au document contenant l'objet |NVDA+contrôle+espace |Retire le focus à l'objet embarqué en cours et le rend au document contenant l'objet|

<!-- KC:endInclude -->

### Mode sélection native {#NativeSelectionMode}

Par défaut lors de la sélection de texte avec les touches `maj+flèche` en mode navigation, la sélection est seulement effectuée dans la représentation du document en mode navigation de NVDA, et non dans l'application elle-même.
Cela signifie que la sélection n'est pas visible à l'écran, et la copie du texte avec `contrôle+c` copiera seulement la représentation du contenu en texte brut par NVDA. C'est-à-dire que le formatage des tableaux ou comme lien ne sera pas copié.
Cependant, NVDA dispose d'un mode de sélection native qui peut être activé dans certains documents en mode navigation (pour l'instant seulement dans Mozilla Firefox), ce qui fait que la sélection native dans le document suit la sélection du mode navigation de NVDA.

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Activer ou désactiver le mode de sélection native |`NVDA+maj+f10` |Active ou désactive le mode de sélection native|

<!-- KC:endInclude -->

Lorsque le mode de sélection native est activé, la copie de la sélection avec `contrôle+c` utilisera également la fonctionnalité de copie de l'application elle-même, ce qui signifie que le contenu riche sera copié dans le presse-papiers, au lieu du texte brut.
Cela signifie que le collage de ce contenu dans un programme tel que Microsoft Word ou Excel, le formatage tel que des tableaux ou le fait qu'un élément soit un lien seront inclus.
Veuillez noter cependant qu'en mode de sélection natif, certains labels accessibles ou autres informations générées par NVDA en mode Navigation ne seront pas inclus.
De plus, bien que l'application fasse de son mieux pour faire correspondre la sélection native à la sélection du mode navigation de NVDA, elle peut ne pas toujours être complètement exacte.
Cependant, pour les scénarios dans lesquels vous souhaitez copier un tableau ou un paragraphe entier de contenu riche, cette fonctionnalité devrait s'avérer utile.

## Lecture de Contenu Mathématique {#ReadingMath}

NVDA peut lire et naviguer dans du contenu mathématique sur le Web et dans d'autres applications, offrant un accès à la fois en parole et en braille.
Cependant, pour que NVDA puisse lire et interagir avec le contenu mathématique, vous devrez d'abord installer un composant mathématique pour NVDA.
Il existe plusieures extensions NVDA disponibles dans l'Add-on Store de NVDA qui prennent en charge les mathématiques, notamment l'[extension MathCAT NVDA](https://nsoiffer.github.io/MathCAT/) et [Access8Math](https://github.com/tsengwoody/Access8Math).
Veuillez vous référer à la [section Add-on Store](#AddonsManager) pour savoir comment découvrir et installer les extensions disponibles dans NVDA.
NVDA peut également utiliser l'ancien logiciel [MathPlayer](https://info.wiris.com/mathplayer-info) de Wiris s'il se trouve sur votre système, bien que ce logiciel ne soit plus maintenu.

### Contenu mathématique pris en charge {#SupportedMathContent}

Avec un composant mathématique approprié installé, NVDA supporte les types de contenu mathématiques suivants :

* MathML sous Mozilla Firefox, Microsoft Internet Explorer et Google Chrome.
* Microsoft Word 365 Modern Math Equations via UI automation :
NVDA est capable de lire et d'interagir avec des équations mathématiques dans Microsoft Word 365/2016 build 14326 et supérieur.
Notez cependant que toutes les équations MathType créées précédemment doivent d'abord être converties en Office Math.
Cela peut être fait en sélectionnant chaque équation et en choisissant "Options d'équation", puis "Convertir en Office Math" dans le menu contextuel.
Assurez-vous que votre version de MathType est la dernière version avant de faire cela.
Microsoft Word fournit une navigation linéaire basée sur des symboles à travers les équations elles-mêmes et prend en charge la saisie de mathématiques à l'aide de plusieurs syntaxes, y compris LateX.
Pour plus de détails, veuillez consulter [Équations au format linéaire utilisant UnicodeMath et LaTeX dans Word](https://support.microsoft.com/fr-fr/office/%C3%A9quations-au-format-lin%C3%A9aire-utilisant-unicodemath-et-latex-dans-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint et les anciennes versions de Microsoft Word :
NVDA peut lire et parcourir les équations MathType dans Microsoft Powerpoint et Microsoft Word.
MathType doit être installé pour que cela fonctionne.
La version de démonstration est suffisante.
Elle peut être téléchargée depuis la [page de présentation de MathType](https://www.wiris.com/en/mathtype/).
* Adobe Reader.
Notez que ceci n'est pas un standard officiel, ce qui fait qu'actuellement, il n'existe pas de logiciels grand public pouvant produire ce contenu.
* Kindle Reader pour PC :
NVDA peut lire et parcourir Math dans Kindle pour PC pour les livres avec des mathématiques accessibles.

Durant la lecture d'un document, NVDA annoncera tout contenu mathématique supporté quand il se présente.
Si vous utilisez un afficheur braille, ce contenu sera aussi affiché en braille.

### Navigation Interactive {#InteractiveNavigation}

Si vous travaillez principalement à la synthèse vocale, dans la plupart des cas, vous souhaiterez probablement examiner l'expression en plus petits segments plutôt qu'entendre toute l'expression en une seule fois.

Si vous êtes en mode navigation, vous pouvez le faire en amenant le curseur sur le contenu mathématique et en appuyant sur Entrée.

Si vous n'êtes pas en mode navigation :

1. Amenez le curseur de revue sur le contenu mathématique.
Par défaut, le curseur de revue suit le curseur système, vous pouvez donc généralement utiliser le curseur système pour aller au contenu désiré.
1. Ensuite, activez la commande suivante :

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Interagir avec le contenu mathématique |NVDA+alt+m |Commence l'interaction avec le contenu mathématique.|

<!-- KC:endInclude -->

A ce stade, NVDA entrera en mode mathématiques, dans lequel vous pouvez utiliser les commandes telles que les flèches pour explorer l'expression.
Par exemple, vous pouvez vous déplacer dans l'expression avec les flèches gauche et droite puis zoomer sur une partie de l'expression telle qu'une fraction en utilisant la flèche basse.

Quand vous voulez retourner au document, appuyez simplement sur la touche échap.

Pour plus d'informations sur les commandes disponibles et les préférences pour la lecture et la navigation dans le contenu mathématique, veuillez vous référer à la documentation du composant mathématique particulier que vous avez installé.

* [Documentation MathCAT](https://nsoiffer.github.io/MathCAT/users.html)
* [Documentation Access8Math](https://github.com/tsengwoody/Access8Math)
* [Documentation MathPlayer](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Parfois le contenu mathématique peut être affiché comme un bouton ou autre type d'élément qui, quand activé, peut afficher un dialogue ou plus d'informations relatives à la formule.
Pour activer le bouton ou l'élément contenant la formule, appuyez sur ctrl+entrée.

### Installation de MathPlayer {#InstallingMathPlayer}

Bien qu'il soit généralement recommandé d'utiliser l'une des extensions NVDA les plus récentes pour prendre en charge les mathématiques dans NVDA, dans certains scénarios limités, MathPlayer peut toujours être un choix plus approprié.
Par exemple. MathPlayer peut prendre en charge une langue particulière ou un code braille qui n'est pas pris en charge dans les extensions plus récentes.
MathPlayer est disponible gratuitement sur le site Wiris.
[Télécharger MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Après avoir installé MathPlayer, vous devrez redémarrer NVDA.
Veuillez noter que les informations sur MathPlayer peuvent indiquer qu'il est uniquement destiné aux navigateurs plus anciens tels qu'Internet Explorer 8.
Cela fait uniquement référence à l'utilisation de MathPlayer pour afficher visuellement du contenu mathématique et peut être ignoré par ceux qui l'utilisent pour lire ou naviguer dans les mathématiques avec NVDA.

## Braille {#Braille}

Si vous possédez un afficheur braille, NVDA peut afficher des informations en braille.
Si votre terminal braille possède un clavier de type Perkins, vous pouvez également saisir du texte en intégral ou abrégé.
Le Braille peut aussi être affiché à l'écran en utilisant [la Visionneuse Braille](#BrailleViewer) en remplacement ou en parallèle d'un afficheur braille physique.

Veuillez consulter la section [Terminaux Braille Pris en Charge](#SupportedBrailleDisplays) pour des informations concernant les terminaux braille pris en charge.
Cette section contient également des informations sur les terminaux qui supportent la détection automatique de terminaux braille en arrière-plan.
Vous pouvez configurer le braille dans la catégorie [Braille](#BrailleSettings) du dialogue [Paramètres](#NVDASettings).

### Abréviations des Types, États des Contrôles et Repères en Braille {#BrailleAbbreviations}

Dans le but de loger autant d'informations que possible sur un afficheur braille, les abréviations suivantes ont été définies pour indiquer le type et l'état des contrôles ainsi que les repères.

| Abréviation |Type de contrôle|
|---|---|
|app |application|
|art |article|
|ctn |citation|
|btn |bouton|
|btnd |bouton déroulant|
|btnrot |bouton rotatif|
|btnp |bouton partagé|
|bsc |bascule|
|lég |légende|
|lstd |liste déroulante|
|càc |case à cocher|
|dlg |dialogue|
|doc |document|
|éd |zone d'édition|
|édmdp |édition de mot de passe|
|objemb |objet embarqué|
|notef |note de fin|
|fig |figure|
|noteb |note de bas de page|
|gra |graphique|
|grp |groupe|
|tN |titre de niveau n, ex : t1, t2.|
|aid |bulle d'aide|
|rgn |repère|
|ln |lien|
|lnv |lien visité|
|lst |liste|
|mnu |menu|
|bmnu |barre de menu|
|btnmnu |bouton de menu|
|élmnu |élément de menu|
|pn |panneau|
|bpr |barre de progression|
|indoc |indicateur d'occupation|
|btnr |bouton radio|
|bdéf |barre de défilement|
|sect |section|
|bét |barre d'état|
|ong |Contrôle d'onglet|
|tb |tableau|
|cN |colonne n d'un tableau, ex : c1, c2.|
|lN |ligne n d'un tableau, ex : l1, l2.|
|term |terminal|
|bo |barre d'outils|
|sug |suggestion|
|arb |arborescence|
|btnarb |bouton d'arborescence|
|élarb |élément d'arborescence|
|nv N |un élément d'arborescence a un niveau hiérarchique N|
|fen |fenêtre|
|⠤⠤⠤⠤⠤ |séparateur|
|mrq |contenu marqué|

Les indicateurs d'état suivants sont également définis :

| Abréviation |État du contrôle|
|---|---|
|... |affiché quand un objet supporte l'autocomplétion|
|⢎⣿⡱ |affiché quand un objet (ex : une bascule) est enfoncé|
|⢎⣀⡱ |affiché quand un objet (ex : une bascule) n'est pas enfoncé|
|⣏⣿⣹ |affiché quand un objet (ex : une case à cocher) est coché|
|⣏⣸⣹ |affiché quand un objet (ex : une case à cocher) est semi-coché|
|⣏⣀⣹ |affiché quand un objet (ex : une case à cocher) n'est pas coché|
|- |affiché quand un objet tel qu'un élément d'arborescence peut être réduit|
|+ |affiché quand un objet tel qu'un élément d'arborescence peut être développé|
|*** |affiché quand on rencontre un contrôle ou un document protégé|
|clq |affiché quand un objet est cliquable|
|cmnt |affiché quand il y a un commentaire pour une cellule de feuille de travail ou un document|
|frml |affiché quand il y a une formule dans une cellule de feuille de travail|
|invl |affiché lors d'une saisie invalide|
|ldesc |affiché quand un objet, généralement un graphique, a une description longue|
|mléd |affiché quand un champ d'édition permet la frappe de plusieurs lignes de texte comme les zones de commentaire sur les sites web|
|oblg |affiché quand on rencontre un champ de saisie obligatoire|
|ls |affiché quand un objet tel qu'une zone d'édition est en lecture seule|
|sél |affiché quand un objet est sélectionné|
|nsél |affiché quand un objet n'est pas sélectionné|
|tcro |affiché quand un objet est trié en ordre croissant|
|tdéc |affiché quand un objet est trié en ordre décroissant|
|smnu |affiché quand un objet a un sous-menu|

Enfin, les abréviations de repères suivantes sont définies :

| Abréviation |Repère|
|---|---|
|bnr |bannière|
|cinf |information sur le contenu|
|cmp |complémentaire|
|form |formulaire|
|prc |principale|
|nav |navigation|
|rch |recherche|
|rgn |région|

### Saisie en Braille {#BrailleInput}

NVDA supporte la saisie de braille intégral ou abrégé via un clavier braille.
Vous pouvez sélectionner la table de conversion utilisée pour convertir le braille en texte en utilisant le paramètre [Table de saisie](#BrailleSettingsInputTable) de la catégorie Braille du dialogue [Paramètres](#NVDASettings).

Quand on utilise le braille intégral , le texte est inséré aussitôt qu'il est entré.
Quand on utilise le braille abrégé, le texte est inséré quand on presse espace ou entrée à la fin d'un mot.
Notez que la conversion ne concerne que les mots braille que vous êtes en train de taper et ne peut pas considérer du texte existant.
Par exemple, si vous utilisez un code braille dont les nombres doivent commencer par un indicateur numérique et pressez retour arrière pour aller à la fin d'un nombre, vous devrez entrer à nouveau l'indicateur numérique pour entrer des chiffres supplémentaires.

<!-- KC:beginInclude -->
L'appui sur le point 7 efface la dernière cellule ou le dernier caractère braille saisi.
Le point 8 traduit toute saisie braille puis appuie sur la touche Entrée.
L'appui simultané sur les points 7 et 8 traduit toute saisie braille sans ajouter d'espace ou actionner la touche entrée.
<!-- KC:endInclude -->

#### Saisie de raccourcis clavier {#BrailleKeyboardShortcuts}

NVDA prend en charge la saisie de raccourcis clavier et l'émulation de touches à l'aide de l'afficheur braille.
Cette émulation se présente sous deux formes : l'attribution d'une entrée braille directement à un appui sur une touche et l'utilisation des touches de modification virtuelles.

Les touches couramment utilisées, telles que les touches fléchées ou l'appui sur Alt pour accéder aux menus, peuvent être mappées directement sur la saisie braille.
Le pilote de chaque afficheur braille est pré-équipé avec certaines de ces affectations.
Vous pouvez modifier ces affectations ou ajouter de nouvelles touches émulées à partir du [dialogue Gestes de commandes](#InputGestures).

Bien que cette approche soit utile pour les touches fréquemment pressées ou uniques (telles que la tabulation), vous ne souhaiterez peut-être pas attribuer un ensemble unique de touches à chaque raccourci clavier.
Pour permettre l'émulation de pression de touches lorsque les touches de modification sont maintenues enfoncées, NVDA fournit des commandes pour basculer entre les touches contrôle, alt, majuscule, windows et NVDA, ainsi que des commandes pour certaines combinaisons de ces touches.
Pour utiliser ces bascules, appuyez d'abord sur la commande (ou la séquence de commandes) des touches de modification sur lesquelles vous souhaitez appuyer.
Saisissez ensuite le caractère faisant partie du raccourci clavier que vous souhaitez saisir.
Par exemple, pour produire contrôle+f, utilisez la commande "bascule de touche contrôle" puis tapez un f,
et pour saisir contrôle+alt+t, utilisez soit les commandes "bascule de touche contrôle" et "bascule de touche alt", dans n'importe quel ordre, soit la commande "bascule de touches Contrôle et alt", suivie de la saisie d'un t.

Si vous basculez accidentellement les touches de modification, exécuter à nouveau la commande bascule supprimera le modificateur.

Lors de la saisie en braille abrégé, l'utilisation des touches de modification entraînera la traduction de votre entrée comme si vous aviez appuyé sur les points 7 + 8.
De plus, la touche émulée ne peut pas refléter le braille tapé avant que la touche de modification ne soit enfoncée.
Cela signifie que, pour taper alt+2 avec un code braille qui utilise un signe dièse, vous devez d'abord basculer Alt puis taper un signe dièse.

## Vision {#Vision}

Bien que NVDA soit en premier lieu destiné à des personnes aveugles ou malvoyantes qui utilisent principalement la parole ou le braille pour accéder à un ordinateur, il offre aussi des facilités internes pour changer le contenu de l'écran.
Sous NVDA, une telle aide visuelle est appelée un service d'amélioration visuelle.

NVDA offre plusieurs services d'amélioration visuelle décrits ci-dessous.
Des services d'amélioration visuelle additionnels peuvent être apportés dans des [Extensions NVDA](#AddonsManager).

Les paramètres de vision de NVDA peuvent être modifiés dans la [catégorie vision](#VisionSettings) du dialogue [Paramètres NVDA](#NVDASettings).

### Mise en Évidence Visuelle {#VisionFocusHighlight}

La mise en évidence Visuelle peut aider à identifier la position du [focus système](#SystemFocus), de [l'objet navigateur](#ObjectNavigation) et du [mode navigation](#BrowseMode).
Ces positions sont mises en évidence avec un contour rectangulaire coloré.

* Le bleu continu indique la position d'un objet navigateur combiné au focus système (ex : lorsque [l'objet navigateur suit le curseur système](#ReviewCursorFollowFocus)).
* Le bleu pointillé indique juste l'objet ayant le focus système.
* Le rose continu indique juste l'objet navigateur.
* Le jaune continu indique le curseur virtuel utilisé en mode navigation (quand il n'y a pas de curseur physique comme dans les navigateurs web).

Quand la Mise en Évidence Visuelle est activée dans la [catégorie vision](#VisionSettings) du dialogue [Paramètres de NVDA](#NVDASettings), vous pouvez [choisir de mettre en évidence ou non le focus, l'objet navigateur ou le curseur du mode navigation](#VisionSettingsFocusHighlight).

### Le Rideau d'Écran {#VisionScreenCurtain}

En tant qu'utilisateur aveugle ou malvoyant, il est parfois impossible ou inutile de voir le contenu de l'écran.
Par ailleurs, il peut être difficile de s'assurer que personne ne regarde par-dessus votre épaule.
Pour cette situation, NVDA contient une fonctionnalité appelée "Rideau d'Écran" qui peut être activée pour rendre l'écran noir.

Vous pouvez activer le Rideau d'Écran dans la [catégorie vision](#VisionSettings) du dialogue [Paramètres NVDA Settings](#NVDASettings).

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Activer ou désactiver le rideau d'écran |`NVDA+contrôle+échap` |Activer pour rendre l'écran noir ou désactiver pour afficher le contenu de l'écran. Un appui active le rideau d'écran jusqu'au prochain redémarrage de NVDA. Deux appuis activent le rideau d'écran jusqu'à ce que vous le désactiviez.|

<!-- KC:endInclude -->

Quand le Rideau d'Écran est activé, certaines tâches directement liées à ce qui apparaît sur l'écran telles que [la reconnaissance optique de caractères](#Win10Ocr) ou la prise d'une copie d'écran ne peuvent pas être effectuées.

En raison d'un changement dans l'API de grossissement de Windows, le Rideau d'Écran a dû être mis à jour pour prendre en charge les dernières versions de Windows.
Utilisez NVDA 2021.2 pour activer le Rideau d'Écran avec Windows 10 21H2 (10.0.19044) ou une version ultérieure.
Pour des raisons de sécurité, lorsque vous utilisez une nouvelle version de Windows, obtenez une confirmation visuelle que le rideau d'écran rend l'écran entièrement noir.

Veuillez noter que lorsque la Loupe Windows est en cours d'exécution et que les couleurs d'écran inversées sont utilisées, le rideau d'écran ne peut pas être activé.

## Reconnaissance de Contenu {#ContentRecognition}

Quand les auteurs ne fournissent pas assez d'informations pour qu'un utilisateur de revue d'écran puisse déterminer le contenu de quelque chose, divers outils peuvent être utilisés pour tenter de reconnaître le contenu à partir d'une image.
NVDA supporte la fonctionnalité de reconnaissance optique de caractères (OCR) disponible sous Windows 10 et versions ultérieures pour reconnaître le texte dans les images.
Des outils de reconnaissance de contenu additionnels peuvent être fournis dans des extensions de NVDA.

Quand vous utilisez une commande de reconnaissance de contenu, NVDA reconnaît le contenu de [l'objet navigateur courant](#ObjectNavigation).
Par défaut, l'objet navigateur suit le focus système ou le curseur du mode navigation, il vous suffit donc généralement d'amener le focus ou le curseur de navigation à l'endroit désiré.
Par exemple, si vous amenez le curseur de navigation sur un graphique, la reconnaissance reconnaîtra le contenu de ce graphique par défaut.
Cependant, vous pouvez utiliser directement la navigation par objet pour, par exemple, reconnaître tout le contenu d'une fenêtre d'application.

Une fois la reconnaissance terminée, le résultat sera présenté dans un document similaire au mode navigation, vous permettant de lire les informations avec les touches curseur, etc.
L'appui sur la touche Entrée ou Espace activera (clic normal) le texte sous le curseur si possible.
L'appui sur échap quitte et efface le résultat de reconnaissance.

### Reconnaissance Optique de Caractères de Windows {#Win10Ocr}

Windows 10 et les versions ultérieures incluent la reconnaissance optique de caractères pour beaucoup de langues.
NVDA peut l'utiliser pour extraire le texte d'images ou d'applications inaccessibles.

Vous pouvez définir la langue à utiliser pour la reconnaissance de texte dans la catégorie [Reconnaissance Optique De Caractères de Windows](#Win10OcrSettings) du dialogue [Paramètres](#NVDASettings).
Des langues additionnelles peuvent être installées en ouvrant le menu Démarrer, choisir Paramètres, Sélectionner Heure et Langue -> Région & Langue puis choisir Ajouter une langue.

Lorsque vous souhaitez surveiller un contenu en constante évolution, par exemple lorsque vous regardez une vidéo avec sous-titres, vous pouvez éventuellement activer l'actualisation automatique du contenu reconnu.
Cela peut également être fait dans la [Catégorie Reconnaissance optique de caractères de Windows](#Win10OcrSettings) de la boîte de dialogue [Paramètres NVDA](#NVDASettings).

La reconnaissance optique de caractères de Windows peut être partiellement ou totalement incompatible avec [les améliorations visuelles de NVDA](#Vision) ou autres aides visuelles externes. Vous devrez désactiver ces aides avant de procéder à une reconnaissance.

<!-- KC:beginInclude -->
Pour reconnaître le texte dans l'objet navigateur courant en utilisant la reconnaissance optique de caractères de Windows, pressez NVDA+r.
<!-- KC:endInclude -->

## Fonctionnalités Spécifiques à Certaines Applications {#ApplicationSpecificFeatures}

NVDA fournit ses propres fonctionnalités additionnelles dans quelques applications pour rendre certaines tâches plus faciles ou pour donner accès à certaines fonctions qui ne seraient pas accessibles autrement.

### Microsoft Word {#MicrosoftWord}
#### Lecture Automatique des En-têtes de Lignes et de Colonnes {#WordAutomaticColumnAndRowHeaderReading}

NVDA est capable d'annoncer automatiquement les en-têtes des lignes et des colonnes quand on navigue dans un tableau sous Microsoft Word.
Ceci nécessite que l'option "En-têtes de ligne et de colonne" soit activée dans la catégorie "Mise en Forme des Documents" qui se trouve dans le dialogue [Paramètres](#NVDASettings) de NVDA.

Si vous utilisez [UIA pour accéder aux documents Word](#MSWordUIA), qui est le choix par défaut pour les versions récentes de Word et Windows, les cellules de la première ligne seront automatiquement considérées comme en-têtes de colonnes ; de même, les cellules de la première colonne seront automatiquement considérées comme en-têtes de lignes.

Au contraire, si vous n'utilisez pas [UIA pour accéder aux documents Word](#MSWordUIA), vous devrez indiquer à NVDA quelle ligne ou colonne contient les en-têtes pour chaque tableau.
Après vous être placé sur la première cellule dans la colonne ou la ligne contenant les titres, utilisez l'une des commandes suivantes :
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Définir les titres de colonnes |NVDA+maj+c |Appuyer une fois indique à NVDA que cette cellule est la première de la ligne contenant les titres de colonnes, qui devraient être annoncés automatiquement en naviguant entre les colonnes sous cette ligne. Appuyer deux fois permet d'effacer le paramétrage.|
|Définir les titres de lignes |NVDA+maj+r |Appuyer une fois indique à NVDA que cette cellule est la première de la colonne contenant les titres de lignes, qui devraient être annoncés automatiquement en naviguant entre les lignes après cette colonne. Appuyer deux fois permet d'effacer le paramétrage.|

<!-- KC:endInclude -->
Ces paramètres seront enregistrés dans le document comme des signets, compatibles avec d'autres revues d'écran comme JAWS.
Cela signifie que d'autres utilisateurs de revues d'écran ouvrant ce document ultérieurement auront automatiquement les titres des lignes et colonnes déjà définis.

#### Mode Navigation sous Microsoft Word {#BrowseModeInMicrosoftWord}

Comme sur le web, le mode navigation peut être utilisé sous Microsoft Word pour vous permettre d'utiliser des fonctionnalités telles que la navigation rapide et la Liste d'éléments.
<!-- KC:beginInclude -->
Pour activer ou désactiver le mode navigation sous Microsoft Word, pressez NVDA+espace.
<!-- KC:endInclude -->
Pour plus d'information sur le mode navigation et la navigation rapide, consultez la [section Mode navigation](#BrowseMode).

##### La Liste d'Éléments {#WordElementsList}

<!-- KC:beginInclude -->
Quand vous êtes en mode navigation sous Microsoft Word, vous pouvez accéder à la liste d'éléments en pressant NVDA+f7.
<!-- KC:endInclude -->
La liste d'éléments peut lister les titres, les liens, annotations (incluant inclut les commentaires et les demandes de changement) et les erreurs (actuellement limité aux fautes d'orthographe).

#### Annonce des Commentaires {#WordReportingComments}

<!-- KC:beginInclude -->
Pour annoncer tout commentaire à la position actuelle du curseur, pressez NVDA+alt+c.
<!-- KC:endInclude -->
Tous les commentaires pour le document ainsi que les autres demandes de modification peuvent aussi être listés dans la liste d'éléments de NVDA en choisissant le type Annotations.

### Microsoft Excel {#MicrosoftExcel}
#### Lecture Automatique des En-têtes de Lignes et de Colonnes {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA est capable d'annoncer automatiquement les en-têtes des lignes et des colonnes quand on navigue dans un tableau dans une feuille de calcul Excel.
Ceci nécessite d'abord que l'option "En-têtes de ligne et de colonne" soit activée dans la catégorie "Mise en Forme des Documents" qui se trouve dans le dialogue [Paramètres](#NVDASettings) de NVDA.
Ensuite, NVDA doit savoir quelle ligne ou colonne contient les titres dans le tableau considéré.
Après vous être placé sur la première cellule dans la colonne ou la ligne contenant les titres, utilisez l'une des commandes suivantes :
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Définir les titres de colonnes |NVDA+maj+c |Appuyer une fois indique à NVDA que cette cellule est la première de la ligne contenant les titres de colonnes, qui devraient être annoncés automatiquement en naviguant entre les colonnes sous cette ligne. Appuyer deux fois permet d'effacer le paramétrage.|
|Définir les titres de lignes |NVDA+maj+r |Appuyer une fois indique à NVDA que cette cellule est la première de la colonne contenant les titres de lignes, qui devraient être annoncés automatiquement en naviguant entre les lignes après cette colonne. Appuyer deux fois permet d'effacer le paramétrage.|

<!-- KC:endInclude -->
Ces paramètres seront enregistrés dans le document comme plages de noms définis, compatibles avec d'autres revues d'écran comme JAWS.
Cela signifie que d'autres utilisateurs de revues d'écran ouvrant ce document ultérieurement auront automatiquement les titres des lignes et colonnes déjà définis.

#### La Liste d'Éléments {#ExcelElementsList}

Comme sur le web, NVDA a une liste d'éléments pour Microsoft Excel permettant d'accéder à différents types d'informations.
<!-- KC:beginInclude -->
Pour accéder à la liste d'éléments sous Excel, pressez NVDA+f7.
<!-- KC:endInclude -->
Les différents types d'informations disponibles dans la liste d'éléments sont :

* Diagrammes : Ceci liste tous les diagrammes dans la feuille de travail active.
Sélectionner un diagramme et appuyer sur la touche Entrée ou le bouton "Aller à" amène le focus au diagramme pour naviguer et lire avec les flèches.
* Commentaires : Ceci liste toutes les cellules de la feuille de travail active contenant des commentaires.
L'adresse de la cellule et ses commentaires sont présentés pour chaque cellule.
L'appui sur la touche Entrée ou le bouton Aller à sur un commentaire de la liste vous amènera directement à cette cellule.
* Formules : Ceci liste toutes les cellules de la feuille de travail contenant une formule.
L'adresse de la cellule et sa formule sont présentés pour chaque cellule.
L'appui sur la touche Entrée ou le bouton Aller à sur une formule de la liste vous amènera directement à cette cellule.
* feuilles : Ceci liste toutes les feuilles du classeur.
L'appui sur f2 sur une feuille de la liste vous permet de renommer cette feuille.
L'appui sur la touche Entrée ou le bouton Aller à sur une feuille de la liste vous amènera directement à cette feuille.
* Champs de formulaire : Ceci liste tous les champs de formulaire dans la feuille de travail active.
Pour chaque champ de formulaire, la liste d'éléments présente le texte alternatif du champ avec l'adresse des cellules concernées.
La sélection d'un champ de formulaire et l'appui sur entrée ou le bouton Aller à amènent à ce champ en mode navigation.

#### Annonce des Notes {#ExcelReportingComments}

<!-- KC:beginInclude -->
Pour annoncer toute note pour la cellule actuellement en focus, pressez NVDA+alt+c.
Sous Microsoft 2016, 365 et plus récents, les commentaires classiques sous Microsoft Excel ont été renommés en "notes".
<!-- KC:endInclude -->
Toutes les notes de la feuille de calcul peuvent aussi être listés dans la liste d'éléments de NVDAaprès appui sur NVDA+f7.

NVDA peut aussi afficher un dialogue spécifique pour ajouter ou éditer une note particulière.
NVDA remplace la zone d'édition de note originale de MS Excel en raison de contraintes d'accessibilité, mais le raccourci clavier pour afficher le dialogue est hérité de MS Excel et fonctionne aussi sans que NVDA soit actif.
<!-- KC:beginInclude -->
Pour ajouter ou éditer une note, dans une cellule en focus, pressez maj+f2.
<!-- KC:endInclude -->

Ce raccourci n'apparaît pas et ne peut être remplacé dans le dialogue Geste de Commandes de NVDA.

Note : il est également possible d'ouvrir la zone d'édition de note de MS Excel par le menu contextuel de n'importe quelle cellule de la feuille de calcul.
Cependant, cela ouvrira la zone d'édition de note inaccessible et non le dialogue spécifique d'édition de commentaire de NVDA.

Sous Microsoft Office 2016, 365 et plus récents, un nouveau genre de dialogue de commentaire a été ajouté.
Ce dialogue est accessible et apporte plus de fonctionnalités telles que la réponse aux commentaires, etc.
Il peut aussi être ouvert depuis le menu contextuel d'une cellule.
Les commentaires ajoutés au cellules via le nouveau dialogue de commentaire ne sont pas liés aux "notes".

#### Lecture des Cellules Protégées {#ExcelReadingProtectedCells}

Si un classeur a été protégé, il peut être impossible d'amener le focus à certaines cellules ayant été protégées en écriture.
<!-- KC:beginInclude -->
Pour pouvoir aller aux cellules protégées, passer en mode navigation en pressant NVDA+espace, puis utilisez les commandes standards de mouvement d'Excel telles que les flèches pour vous déplacer parmi les cellules de la feuille en cours.
<!-- KC:endInclude -->

#### Champs de Formulaire {#ExcelFormFields}

Les feuilles de travail Excel peuvent inclure des champs de formulaire.
Vous pouvez y accéder en utilisant la liste d'éléments ou les touches de navigation rapide f et maj+f.
Quand vous êtes sur un champ de formulaire en mode navigation, vous pouvez appuyer sur Entrée ou Espace pour l'activer ou passer en mode formulaire pour pouvoir interagir avec lui, selon le type de contrôle.
Pour plus d'information concernant le mode navigation et la navigation par lettre, veuillez consulter la [section Mode Navigation](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Basculer l'arrêt de la lecture vocale |contrôle+maj+s |Lorsque l'on est dans un diaporama en cours de lecture, cette commande basculera entre les notes du commentateur du diaporama et le contenu de celui-ci. Cela n'affecte que ce que NVDA lira, pas l'affichage à l'écran.|

<!-- KC:endInclude -->

### Foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Annonce du temps restant |contrôle+maj+r |Annonce le temps restant pour le morceau en cours.|
|Annonce du temps écoulé |contrôle+maj+e |annonce le temps écoulé de la piste en cours.|
|Annonce de la longueur de la piste |contrôle+maj+t |Annonce la longueur de la piste en cours.|

<!-- KC:endInclude -->

Note : Les raccourcis ci-dessus fonctionnent seulement avec le format de chaîne par défaut pour la barre d'état de Foobar.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Annonce de message récent |NVDA+contrôle+1-4 |Annonce un des messages récents selon le chiffre appuyé ; ex : NVDA+contrôle+2 lit le second message le plus récent.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA offre un support amélioré pour Poedit 3.4 ou plus récent.

<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Annonce des notes pour les traducteurs |`contrôle+maj+a` |Annonce les notes pour les traducteurs. Deux appuis présente les notes en mode navigation|
|Annonce de la fenêtre de commentaires |`contrôle+maj+c` |Annonce tout commentaire dans la fenêtre de commentaires. Deux appuis présente le commentaire en mode navigation|
|Annonce de l'ancien texte source |`contrôle+maj+o` |Annonce l'ancien texte source s'il y en a un. Deux appuis présente le texte en mode navigation|
|Annonce l'avertissement de traduction |`contrôle+maj+w` |Annonce l'avertissement de traduction, s'il y en a un. Deux appuis présente l'avertissement en mode navigation|

<!-- KC:endInclude -->

### Kindle pour PC {#Kindle}

NVDA supporte la lecture et la navigation dans les livres sous Amazon Kindle pour PC.
Cette fonctionnalité est disponible seulement dans les livres Kindle signalés par "Support des revues d'écran", ce que vous pouvez vérifier sur la page de détails du livre.

On utilise le mode navigation pour lire les livres.
Il est activé automatiquement quand vous ouvrez un livre ou quand vous placez le focus sur la zone du livre.
La page sera tournée automatiquement quand vous déplacerez le curseur ou utiliserez la commande dire tout.
<!-- KC:beginInclude -->
Vous pouvez aller manuellement à la page suivante en pressant la touche PageSuiv ou à la page précédente en pressant la touche PagePrec.
<!-- KC:endInclude -->

La navigation par simple lettre est supportée pour les liens et les graphiques, mais seulement dans la page en cours.
La navigation par liens inclut également les notes de bas de page.

NVDA fournit une ébauche de support pour la lecture et la navigation interactive de contenu mathématique pour les livres avec du contenu mathématique accessible.
Veuillez consulter la section [Lecture de Contenu Mathématique](#ReadingMath) pour plus d'informations.

#### Sélection de Texte {#KindleTextSelection}

Kindle vous permet d'exécuter diverses fonctions relatives au texte sélectionné, incluant l'obtention d'une définition du dictionnaire, l'ajout de notes et de surlignages, la copie du texte dans le presse-papiers et la recherche sur le web.
Pour faire cela, sélectionnez d'abord le texte comme vous le feriez normalement en mode navigation; ex: en utilisant maj et les touches curseur.
<!-- KC:beginInclude -->
Une fois que vous avez sélectionné le texte, pressez la touche applications ou maj+f10 pour afficher les options disponibles pour travailler avec la sélection.
<!-- KC:endInclude -->
Si vous faites ceci sans avoir sélectionné de texte, les options pour le mot sous le curseur seront affichées.

#### Notes de l'Utilisateur {#KindleUserNotes}

Vous pouvez ajouter une note concernant un mot ou un passage du texte.
Pour faire cela, sélectionnez d'abord le texte concerné et accédez aux options de sélection comme décrit plus haut.
Ensuite, choisissez Ajouter une Note.

Durant la lecture en mode navigation, NVDA fait référence à cette note comme un commentaire.

Pour afficher, éditer ou effacer une note.

1. Amenez le curseur au texte contenant la note.
1. Accédez aux options de sélection comme décrit plus haut.
1. Choisissez Éditer la Note.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Quand vous êtes dans le tableau des livres ajoutés :

| Nom |Touche |Description|
|---|---|---|
|Entrée |entrée |Ouvre le livre sélectionné.|
|Menu contextuel |applications |Ouvre le menu contextuel pour le livre sélectionné.|

<!-- KC:endInclude -->

### Console Windows {#WinConsole}

NVDA fournit un support pour la console de commande de Windows utilisée par l'invite de commandes, PowerShell, et le sous-système Windows pour Linux.
La console Windows est de taille fixe, typiquement beaucoup plus petite que le tampon contenant l'affichage.
Quand du nouveau texte est écrit, le contenu défile vers le haut et le texte précédent n'est plus visible.
Sur les versions de Windows antérieures à Windows 11 22H2, le texte de la console qui n'est pas visiblement affiché dans la fenêtre n'est pas accessible avec les commandes de revue de texte de NVDA.
Ainsi, il est nécessaire de faire défiler la fenêtre de la console pour lire le texte plus ancien.
Dans les versions plus récentes de la console et dans Windows Terminal, il est possible de consulter librement l'intégralité du tampon de texte sans avoir à faire défiler la fenêtre.
<!-- KC:beginInclude -->
Les raccourcis clavier propres à Windows suivants peuvent être utiles pour [revoir du texte](#ReviewingText) avec NVDA dans les versions plus anciennes de la Console Windows :

| Nom |Touche |Description|
|---|---|---|
|Défilement vers le haut |contrôle+flècheHaute |Fait défiler la fenêtre de la console vers le haut pour que le texte plus ancien puisse être lu.|
|Défilement vers le bas |contrôle+flècheBasse |Fait défiler la fenêtre de la console vers le bas pour que le texte plus récent puisse être lu.|
|Aller au début |contrôle+début |Aligne la fenêtre de la console sur le début du tampon.|
|Aller à la fin |contrôle+fin |Aligne la fenêtre de la console sur la fin du tampon.|

<!-- KC:endInclude -->

## Configurer NVDA {#ConfiguringNVDA}

La plupart des paramètres de NVDA peuvent être modifiés en utilisant les dialogues accessibles par le sous-menu "Préférences" du menu NVDA.
Beaucoup de ces paramètres se trouvent dans le dialogue multipage [Paramètres](#NVDASettings).
Dans tous les dialogues, appuyez sur le bouton "OK" pour valider vos modifications.
Pour annuler les modifications, appuyez sur le bouton "Annuler" ou sur la touche "échap".
Pour certains dialogues, vous pouvez activer le bouton Appliquer pour que les paramètres prennent effet immédiatement sans fermer le dialogue.
La plupart des dialogue NVDA prennent en charge l'aide contextuelle.
<!-- KC:beginInclude -->
Dans un dialogue, un appui sur `f1` ouvre le guide de l'utilisateur au paragraphe relatif au paramètre sélectionné ou au dialogue actuel.
<!-- KC:endInclude -->
Certains paramètres peuvent aussi être modifiés en utilisant des raccourcis clavier que vous trouverez dans les sections ci-dessous.

### Paramètres de NVDA {#NVDASettings}

<!-- KC:settingsSection: || Nom | Ordinateur de bureau | Ordinateur portable | Description | -->
NVDA fournit de nombreux paramètres de configuration qui peuvent être modifiés à l'aide de la boîte de dialogue des paramètres.
Pour faciliter la recherche du type de paramètres que vous souhaitez modifier, la boîte de dialogue affiche une liste de catégories de configuration parmi lesquelles choisir.
Lorsque vous sélectionnez une catégorie, tous les paramètres qui s'y rapportent s'affichent dans la boîte de dialogue.
Pour vous déplacer entre les catégories, utilisez `tab` ou `maj+tab` pour atteindre la liste des catégories, puis utilisez les touches fléchées haut et bas pour naviguer dans la liste.
De n'importe où dans la boîte de dialogue, vous pouvez également avancer d'une catégorie en appuyant sur `ctrl+tab`, ou reculer d'une catégorie en appuyant sur `maj+ctrl+tab`.

Une fois que vous avez modifié un ou plusieurs paramètres, les paramètres peuvent être appliqués à l'aide du bouton Appliquer, auquel cas la boîte de dialogue restera ouverte, vous permettant de modifier d'autres paramètres ou de choisir une autre catégorie.
Si vous voulez sauvegarder vos paramètres et fermer le dialogue Paramètres, vous pouvez utiliser le bouton "OK".

Certaines catégories de paramètres ont un raccourci clavier dédié.
Si on le presse, ce raccourci ouvrira le dialogue Paramètres directement dans cette catégorie particulière.
Par défaut, toutes les catégories ne peuvent pas être atteintes via un raccourci clavier.
Si vous accédez fréquemment à une catégorie qui n'a pas de raccourci dédié, utilisez le dialogue [Geste de Commandes](#InputGestures) pour ajouter un geste personnalisé tel qu'un raccourci clavier ou un geste tactile pour cette catégorie.

Les catégories de paramètres du dialogue Paramètres sont décrite ci-dessous.

#### Général {#GeneralSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres généraux {#OpenGeneralSettings}

Raccourci clavier : `NVDA+contrôle+g`

La catégorie Général du dialogue Paramètres définit le comportement global de NVDA tel que la langue de l'interface et la vérification des mises à jour.
Elle contient les options suivantes :

##### Langue {#GeneralSettingsLanguage}

C'est une liste déroulante qui permet de choisir la langue de l'interface utilisateur et des messages de NVDA.
La liste comporte de nombreuses langues et le choix par défaut est dénommé "Utilisateur par défaut".
Ce choix indique à NVDA d'utiliser la langue de Windows.

Noter qu'il faut relancer NVDA quand on change la langue.
Quand le dialogue de confirmation apparaît, sélectionnez "redémarrer maintenant" ou "redémarrer plus tard" selon que vous voulez utiliser la nouvelle langue maintenant ou ultérieurement, respectivement. Si "redémarrer plus tard" est sélectionné, la configuration doit être sauvegardée (soit manuellement soit en utilisant la fonctionnalité sauvegarder la configuration en quittant).

##### Sauvegarder la configuration en quittant {#GeneralSettingsSaveConfig}

C'est une case à cocher qui, une fois cochée, indique à NVDA de sauvegarder automatiquement la configuration courante lorsqu'on arrête NVDA.

##### Afficher les options d'arrêt avant de quitter NVDA {#GeneralSettingsShowExitOptions}

Cette option est une case à cocher qui vous permet de décider si un dialogue doit s'afficher ou non lorsque vous quittez NVDA, pour demander quelle action vous souhaitez effectuer.
Quand elle est cochée, un dialogue apparaît lorsque vous voulez quitter NVDA, vous demandant si vous voulez quitter, redémarrer, redémarrer sans extensions ou installer des mises à jour en attente s'il y en a.
Quand elle n'est pas cochée, NVDA s'arrête immédiatement.

##### Jouer des sons au démarrage ou à l'arrêt de NVDA {#GeneralSettingsPlaySounds}

Cette option est une case à cocher qui, quand elle est cochée, dit à NVDA de jouer des sons lors de son démarrage ou de son arrêt.

##### Niveau de journalisation {#GeneralSettingsLogLevel}

C'est une liste déroulante qui vous permet de choisir la quantité d'informations que NVDA consignera dans son journal durant son exécution.
Généralement, l'utilisateur n'aura pas besoin d'y toucher dans la mesure où assez peu d'informations sont consignées.
Cependant, si vous voulez fournir des informations lors d'un rapport d'erreur, ou activer/désactiver la journalisation, cette option peut être utile.

Les niveaux de journalisation disponibles sont :

* Désactivé : À l'exception d'un bref message de démarrage, NVDA ne journalisera rien durant son exécution.
* Info : NVDA journalisera des informations de base telles que les messages de démarrage et des informations utiles pour les développeurs.
* Avertissements de débogage : Les messages d'avertissement qui ne sont pas causés par des erreurs graves seront journalisés.
* Entrées/sorties : Les entrées du clavier et des terminaux braille, ainsi que les sorties en parole et en braille seront journalisées.
Si la confidentialité vous préoccupe, ne définissez pas le niveau de journalisation sur cette option.
* Débogage : En plus des messages d'info, avertissements et entrées/sorties, des messages additionnels de débogage seront journalisés.
Tout comme pour entrées/sorties, si la confidentialité vous préoccupe, vous ne devez pas définir le niveau de journalisation sur cette option.

##### Démarrer NVDA automatiquement après ma connexion à Windows {#GeneralSettingsStartAfterLogOn}

Si cette option est activée, NVDA démarrera automatiquement dès que vous vous connecterez à Windows.
Cette option n'existe que dans les versions installées de NVDA.

##### Utiliser NVDA sur l'écran de connexion à Windows (nécessite des privilèges administrateur) {#GeneralSettingsStartOnLogOnScreen}

Si vous vous connectez à Windows en fournissant un nom d'utilisateur et un mot de passe, l'activation de cette option permettra à NVDA de démarrer automatiquement dès l'écran de connexion au démarrage de Windows.
Cette option n'existe que dans les versions installées de NVDA.

##### Utiliser les paramètres actuellement sauvegardés sur l'écran de connexion et les autres écrans sécurisés {#GeneralSettingsCopySettings}

L'appui sur ce bouton copie votre configuration utilisateur actuellement sauvegardée dans le répertoire système de NVDA, ainsi, NVDA peut l'utiliser quand il s'exécute sur l'écran de connexion et les [autres écrans sécurisés](#SecureScreens).
Pour vous assurer que tous vos paramètres sont transférés, enregistrez d'abord votre configuration avec contrôle+NVDA+c ou Enregistrer la configuration dans le menu NVDA.
Cette option n'existe que dans les versions installées de NVDA.

##### Vérifier automatiquement les mises à jour de NVDA {#GeneralSettingsCheckForUpdates}

Si ceci est activé, NVDA recherchera automatiquement les versions mises à jour et vous informera lorsqu'une mise à jour est disponible.
Vous pouvez également vérifier manuellement les mises à jour en sélectionnant "Recherche d'une Mise à Jour..." sous "Aide" du menu NVDA.
Lors d'une vérification manuelle ou automatique des mises à jour, NVDA doit envoyer certaines informations au serveur pour recevoir la mise à jour appropriée à votre système.
Les informations suivantes sont toujours envoyées :

* Version courante de NVDA
* Version du système d'exploitation
* Système d'exploitation 32 ou 64 bits

##### Autoriser NV Access à recueillir des statistiques d'utilisation {#GeneralSettingsGatherUsageStats}

Si ceci est activé, NV Access utilisera les informations de la vérification de mises à jour pour connaître le nombre d'utilisateurs de NVDA en incluant certaines informations démographiques telles que le système d'exploitation et le pays d'origine.
Bien que votre adresse IP soit utilisée pour déterminer votre pays durant la mise à jour, elle ne sera jamais conservée.
En plus des informations obligatoires nécessaires à la mise à jour, les informations supplémentaires suivantes sont également envoyées :

* La langue d'interface de NVDA
* Copie en cours de NVDA installée ou portables
* Le nom du synthétiseur vocal actuellement utilisé (incluant le nom de l'extension dont provient le pilote)
* Le nom du terminal braille actuellement utilisé (incluant le nom de l'extension dont provient le pilote)
* La table d'affichage braille en cours (si le braille est activé)

Ces informations aident grandement NV Access pour prioritiser les futurs développements de NVDA.

##### Avertir des mises à jour en attente au démarrage {#GeneralSettingsNotifyPendingUpdates}

Si ceci est activé, NVDA vous informera quand il y a une mise à jour en attente au démarrage, et vous offrira la possibilité de l'installer.
Vous pouvez aussi installer manuellement la mise à jour en attente depuis le dialogue de sortie de NVDA (si activé), depuis le menu NVDA, ou quand vous exécutez une vérification depuis le menu Aide.

#### Parole {#SpeechSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres de parole {#OpenSpeechSettings}

Raccourci clavier : `NVDA+contrôle+v`

La catégorie "Parole" dans le dialogue Paramètres de NVDA, contient des options vous permettant de changer le synthétiseur vocal ainsi que les caractéristiques de la voix pour le synthétiseur choisi.
Pour une manière plus rapide de contrôler les paramètres vocaux depuis n'importe où, reportez-vous à la section [boucle des paramètres synthétiseur](#SynthSettingsRing).

La catégorie Parole contient les options suivantes :

##### Changer de synthétiseur {#SpeechSettingsChange}

La première option dans la catégorie Parole est le bouton Changer... Ce bouton active le dialogue [Choisir le Synthétiseur](#SelectSynthesizer) qui vous permet de choisir le synthétiseur actif et le périphérique de sortie.
Ce dialogue s'ouvre par-dessus le dialogue Paramètres.
Sauvegarder ou annuler les paramètres dans le dialogue de choix du synthétiseur vous ramènera au dialogue Paramètres.

##### Voix {#SpeechSettingsVoice}

L'option Voix est une liste déroulante contenant, pour le synthétiseur en cours, toutes les voix que vous avez installées.
Vous pouvez utiliser les flèches pour entendre les différents choix possibles.
Les flèches gauche et haut vous font monter dans la liste et les flèches droit et bas vous font descendre.

##### Variante {#SpeechSettingsVariant}

Si vous utilisez le synthétiseur Espeak NG fourni avec NVDA, cette liste déroulante vous permettra de choisir la variante avec laquelle le synthétiseur doit parler.
Les variantes ESpeak NG sont comme des voix, dans la mesure où elles ajoutent des attributs légèrement différents à la voix ESpeak NG.
Certaines variantes ressembleront à un homme, d'autres à une femme, d'autres même à une grenouille.
Si vous utilisez un synthétiseur tiers, vous pourrez peut-être changer cette valeur aussi, si la voix que vous aurez choisie prend cela en charge.

##### Débit {#SpeechSettingsRate}

Cette option vous permet de modifier le débit de la parole.
C'est un potentiomètre qui va de 0 à 100, (0 étant la vitesse la plus lente et 100 la plus rapide).

##### Débit augmenté {#SpeechSettingsRateBoost}

Activer cette option augmentera significativement le débit de la parole, si le synthétiseur courant le permet.

##### Hauteur {#SpeechSettingsPitch}

Cette option vous permet de modifier la hauteur de la voix.
C'est un potentiomètre qui va de 0 à 100 - 0 étant le son le plus grave et 100 le plus aigu.

##### Volume {#SpeechSettingsVolume}

Cette option est un potentiomètre qui va de 0 à 100 - 0 étant le volume le plus bas et 100 le plus élevé.

##### Inflexion {#SpeechSettingsInflection}

Cette option est un potentiomètre qui vous permet de choisir le degré d'inflexion (augmentation et diminution de la hauteur) que le synthétiseur doit utiliser pour parler.

##### Changement automatique de langue {#SpeechSettingsLanguageSwitching}

Cette case à cocher vous permet de choisir si NVDA doit changer de langue à la volée si une balise de langue est présente dans le texte en cours de lecture.
Cette option est activée par défaut.

##### Changement automatique de dialecte {#SpeechSettingsDialectSwitching}

Cette case à cocher vous permet de choisir si les changements de dialecte doivent être pris en compte en plus des changements de langue réels.
Par exemple, un texte peut être en Anglais Américain et comporter des passages marqués comme Anglais Britannique. Si cette option est activée, le synthétiseur respectera les changements d'accent.
Par défaut, cette option est désactivée.

<!-- KC:setting -->

##### Niveau des ponctuations et symboles {#SpeechSettingsSymbolLevel}

Raccourci clavier : NVDA+p

Ceci vous permet de choisir la quantité de ponctuations et autres symboles qui seront prononcés.
Par exemple, si vous choisissez "Tous", tous les symboles seront annoncés.
Cette option s'applique à tous les synthétiseurs, pas uniquement au synthétiseur courant.

##### Se baser sur la langue de la voix pour le traitement des symboles et caractères {#SpeechSettingsTrust}

Activée par défaut, cette option indique à NVDA si la langue de la voix en cours peut être utilisée pour le traitement des symboles et caractères.
Si vous trouvez que NVDA lit les ponctuations dans la mauvaise langue pour une voix ou un synthétiseur particulier, vous pouvez désactiver ce comportement pour forcer NVDA à utiliser ses paramètres généraux de langue à la place.

##### Inclure les données du Consortium Unicode (incluant les emoji) dans le traitement des caractères et symboles {#SpeechSettingsCLDR}

Quand cette case est cochée, NVDA inclura des dictionnaires de prononciation de symboles additionels lorsqu'il prononce des caractères et des symboles.
Ces dictionnaires contiennent des descriptions de symboles (en particulier les emoji) qui sont fournies par le [Consortium Unicode](https://www.unicode.org/consortium/) comme faisant partie de leur [référentiel commun de données locales Repository](https://cldr.unicode.org/).
Si vous voulez que NVDA annonce la descriptions des caractères emoji en se basant sur ces données, vous devez activer cette option.
Cependant, si vous utilisez un synthétiseur vocal supportant nativement ces descriptions, vous pouvez la désactiver.

Notez que les descriptions de caractères ajoutées manuellement ou modifiées sont sauvegardées dans vos paramètres personnels.
Ainsi, si vous changez la description d'un emoji particulier, votre description personnalisée sera annoncée pour cet emoji que cette option soit activée ou non.
Vous pouvez ajouter, modifier ou supprimer des descriptions de symboles par le dialogue [Prononciation des ponctuations et symboles](#SymbolPronunciation) de NVDA.

Pour activer/désactiver l'inclusion des données du Consortium Unicode de n'importe où, veuillez assigner un geste personnalisé en utilisant le [dialogue des Gestes de Commandes](#InputGestures).

##### Pourcentage de changement de la hauteur pour indiquer les majuscules {#SpeechSettingsCapPitchChange}

Ce champ d'édition vous permet d'entrer la valeur du changement de hauteur de la voix à l'annonce d'une lettre majuscule.
Cette valeur est un pourcentage, une valeur négative réduit la hauteur, une valeur positive l'augmente.
Pour n'avoir aucun changement de hauteur, entrez la valeur 0.
D'ordinaire, NVDA augmente légèrement la tonalité pour chaque lettre majuscule, mais certains synthétiseurs peuvent ne pas supporter cela correctement.
Si le changement de hauteur pour les majuscules n'est pas supporté, optez pour [Dire "majuscule" après les majuscules](#SpeechSettingsSayCapBefore) et/ou [ Émettre un bip pour signaler les majuscules](#SpeechSettingsBeepForCaps) à la place.

##### Dire "majuscule" après les majuscules {#SpeechSettingsSayCapBefore}

Ce paramètre est une case à cocher qui, si cochée, indique à NVDA de dire "maj" pour une lettre en majuscule quand on l'atteint par les flèches de direction ou lors de la frappe.

##### Annoncer les majuscules par des bips {#SpeechSettingsBeepForCaps}

Quand cette case à cocher est cochée, NVDA émettra un petit "bip" chaque fois qu'il rencontre un caractère majuscule.

##### Utiliser la fonction d'épellation si elle est supportée {#SpeechSettingsUseSpelling}

Certains mots ne comportent qu'un seul caractère, mais la prononciation est différente selon que le caractère est prononcé comme un caractère unique (épellation) ou comme un mot.
Par exemple, en Français, "y" est à la fois une lettre et un mot et se prononce différemment selon le cas.
Cette option permet au synthétiseur de différencier les deux cas si le synthétiseur la supporte.
La plupart des synthétiseurs la supportent.

En général, cette option devrait être activée.
Cependant, certains synthétiseurs utilisant les API de parole Microsoft se comportent bizarrement quand cette option est activée.
Si vous rencontrez des problèmes à l'épellation de caractères, essayez de désactiver cette option.

##### Description différée des caractères lors du mouvement du curseur {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Activé, Désactivé|
|Défaut |Désactivé|

Lorsque ce paramètre est coché, NVDA dira la description du caractère lorsque vous vous déplacerez par caractère.

Par exemple, lors de la revue d'une ligne par caractères, lorsque la lettre "b" est lue, NVDA dira "Bravo" après un délai d'une seconde.
Cela peut être utile s'il est difficile de distinguer la prononciation des symboles ou pour les utilisateurs malentendants.

La description différée du caractère sera annulée si un autre texte est prononcé pendant ce temps, ou si vous appuyez sur la touche `contrôle`.

##### Modes disponibles dans la commande Faire défiler les modes de parole {#SpeechModesDisabling}

Les cases à cocher dans cette liste vous permettent de choisir quels [modes de parole](#SpeechModes) sont inclus lors du passage de l'un à l'autre en utilisant `NVDA+s`.
Les modes non cochés sont exclus.
Par défaut, tous les modes sont inclus.

Par exemple, si vous n'avez pas besoin d'utiliser les modes "bips" et "désactivée", vous devez décocher ces deux modes et laisser cochés les modes "activée" et "à la demande".
A noter qu'il est nécessaire de cocher au moins deux modes.

#### Choix du synthétiseur {#SelectSynthesizer}

<!-- KC:setting -->

##### Ouvrir le dialogue sélection du synthétiseur {#OpenSelectSynthesizer}

Raccourci clavier : `NVDA+contrôle+s`

Le dialogue Synthétiseur, qui s'ouvre en activant le bouton Changer dans la catégorie Parole du dialogue Paramètres, permet de choisir le synthétiseur de parole qui sera utilisé par NVDA.
Une fois que vous aurez choisi votre synthétiseur, appuyez sur "OK" et NVDA chargera le synthétiseur choisi.
S'il y a une erreur au chargement du synthétiseur, NVDA vous en informera par un message, puis continuera à utiliser le synthétiseur précédent.

##### Synthétiseur {#SelectSynthesizerSynthesizer}

Cette option vous permet de choisir le synthétiseur de parole qui sera utilisé par NVDA.

Pour une liste des synthétiseurs de parole pris en charge par NVDA, reportez-vous à la section [Synthétiseurs de parole pris en charge](#SupportedSpeechSynths).

L'élément particulier "Pas de parole" apparaîtra toujours dans cette liste.
Cela peut être utile pour quelqu'un qui veut utiliser NVDA seulement avec le braille, ou peut-être pour un développeur voyant qui ne veut utiliser que la visionneuse de parole.

#### Boucle des paramètres synthétiseur {#SynthSettingsRing}

Si vous voulez changer rapidement les paramètres vocaux sans passer par la catégorie Voix du dialogue Paramètres, il y a quelques touches de commandes qui vous permettent de le faire de n'importe où quand NVDA est en fonction.
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Description|
|---|---|---|---|
|Aller au paramètre synthétiseur suivant |NVDA+contrôle+flèche droite |NVDA+contrôle+maj+flèche droite |Va au paramètre synthétiseur applicable suivant, retourne au premier après le dernier|
|Aller au paramètre synthétiseur précédent |NVDA+contrôle+flèche gauche |NVDA+contrôle+maj+flèche gauche |Va au paramètre synthétiseur applicable précédent, retourne au dernier après le premier|
|Augmenter le paramètre synthétiseur courant |NVDA+contrôle+flèche haut |NVDA+contrôle+maj+flèche haut |Augmente le paramètre synthétiseur sur lequel vous vous trouvez. Ex : augmente le débit, choisit la voix suivante, augmente le volume|
|Augmenter le paramètre courant dans la boucle des paramètres du synthétiseur d'un interval plus important |`NVDA+contrôle+pagePrec` |`NVDA+maj+contrôle+pagePrec` |Augmente d'un pas plus important la valeur du paramètre vocal courant sur lequel vous vous trouvez. Ex. lorsque vous êtes sur le paramètre du choix de la voix, avancer de 20 voix ; lorsque vous êtes sur un paramètres avec potentiomètre (débit, hauteur, etc.), la valeur sera incrémentée de 20%|
|Diminuer le paramètre synthétiseur courant |NVDA+contrôle+flèche bas |NVDA+contrôle+maj+flèche bas |diminue le paramètre synthétiseur sur lequel vous vous trouvez. Ex : diminue le débit, choisit la voix précédente, diminue le volume|
|Diminuer le paramètre courant dans la boucle des paramètres du synthétiseur d'un interval plus important |`NVDA+contrôle+pageSuiv` |`NVDA+maj+contrôle+pageSuiv` |Diminue d'un pas plus important la valeur du paramètre vocal courant sur lequel vous vous trouvez. Ex. lorsque vous êtes sur le paramètre du choix de la voix, reculer de 20 voix ; lorsque vous êtes sur un paramètres avec potentiomètre (débit, hauteur, etc.), la valeur sera décrémentée de 20%|

<!-- KC:endInclude -->

#### Braille {#BrailleSettings}

La catégorie Braille du dialogue Paramètres contient des options vous permettant de modifier différents aspect de la saisie et de l'affichage braille.
Cette catégorie contient les options suivantes :

##### Changer de Terminal Braille {#BrailleSettingsChange}

Dans la catégorie Braille du dialogue Paramètres, le bouton Changer... active le dialogue [Choix de l'Afficheur Braille](#SelectBrailleDisplay) qui vous permet de choisir l'afficheur braille actif.
Ce dialogue s'ouvre par-dessus le dialogue Paramètres.
Sauvegarder ouannuler les paramètres dans le dialogue de choix de l'afficheur braille vous ramènera au dialogue Paramètres.

##### Table d'affichage {#BrailleSettingsOutputTable}

L'option suivante est la liste déroulante des tables d'affichage.
Dans cette liste, vous trouverez des tables braille pour différentes langues, braille intégral, informatique, abrégé et autres.
La table choisie sera utilisée pour traduire le texte en braille qui sera présenté sur votre afficheur braille.
Vous pouvez vous déplacer de table en table en utilisant les flèches.

##### Table de saisie {#BrailleSettingsInputTable}

En complément de l'option précédente, l'option que vous trouverez ensuite est la liste déroulante des tables de saisie.
La table choisie sera utilisée pour traduire en texte le braille saisi à l'aide du clavier Perkins de votre afficheur braille.
Vous pouvez vous déplacer de table en table en utilisant les flèches.

Notez que cette option n'est utile que si votre afficheur braille dispose d'un clavier Perkins et que le pilote de celui-ci supporte cette fonctionnalité.
Si la saisie n'est pas supportée par un afficheur qui dispose d'un clavier Perkins, cela sera noté dans la section [Afficheurs braille Supportés](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Mode braille {#BrailleMode}

Raccourci clavier : `NVDA+alt+t`

Cette option vous permet de choisir entre les modes braille disponibles.

Actuellement, deux modes braille sont pris en charge : "suivre les curseurs" et "afficher la parol".

Lorsque suivre les curseurs est sélectionné, l'afficheur braille suivra soit le focus / le curseur système, soit l'objet navigateur / curseur de revue en fonction de ce que le braille doit suivre.

Lorsque l'affichage de la parole est sélectionné, l'afficheur braille affichera ce que NVDA annonce, ou aurait annoncé si le mode de parole était réglé sur "parole activée".

##### Afficher le mot sous le curseur en braille informatique {#BrailleSettingsExpandToComputerBraille}

Cette option permet d'afficher le mot sous le curseur en intégral.

##### Montrer le Curseur {#BrailleSettingsShowCursor}

Cette option permet d'activer ou de désactiver l'affichage du curseur braille.
Elle s'applique au curseur système et au curseur de revue, mais pas à l'indicateur de sélection.

##### Clignotement du Curseur {#BrailleSettingsBlinkCursor}

Cette option permet au curseur braille de clignoter.
Si le clignotement est désactivé, le curseur braille sera constamment en position haute.
L'indicateur de sélection n'est pas affecté par cette option, c'est toujours les points 7 et 8 sans clignotement.

##### Vitesse de clignotement du curseur (ms) {#BrailleSettingsBlinkRate}

Cette option est un champ numérique qui vous permet de modifier la vitesse de clignotement du curseur en millisecondes.

##### Forme du Curseur pour le Focus {#BrailleSettingsCursorShapeForFocus}

Cette option vous permet de choisir la forme (combinaison de points) du curseur braille quand le braille suit le focus.
L'indicateur de sélection n'est pas affecté par cette option, c'est toujours les points 7 et 8 sans clignotement.

##### Forme du Curseur pour la Revue {#BrailleSettingsCursorShapeForReview}

Cette option vous permet de choisir la forme (combinaison de points) du curseur braille quand le braille suit la revue.
L'indicateur de sélection n'est pas affecté par cette option, c'est toujours les points 7 et 8 sans clignotement.

##### Affichage des messages {#BrailleSettingsShowMessages}

C'est une liste déroulante qui vous permet de choisir si NVDA doit afficher les messages en braille et quand ils doivent disparaître automatiquement.

Pour basculer l'affichage des messages de n'importe où, veuillez attribuer un geste personnalisé à l'aide de la [boîte de dialogue Gestes de commandes](#InputGestures).

##### Durée d'affichage des messages (sec) {#BrailleSettingsMessageTimeout}

Cette option est un champ numérique qui contrôle la durée en secondes d'affichage des messages système sur le terminal braille.
Le message de NVDA est immédiatement supprimé à l'appui d'une touche de routage curseur sur l'afficheur braille, mais réapparaît à l'appui d'une touche correspondante qui déclenche le message.
Cette option n'apparaît que si "Affichage des message" est réglé sur "Définir une durée maximale".

<!-- KC:setting -->

##### braille suit {#BrailleTether}

Raccourci clavier : NVDA+contrôle+t

Cette option vous permet de choisir si le braille suivra le curseur du focus système, le curseur de l'objet navigateur ou les deux.
Quand "automatiquement" est sélectionné, NVDA suivra le curseur système et le focus par défaut.
Dans ce cas, quand la position de l'objet de navigation ou du curseur de revue est modifiée par une action explicite de l'utilisateur, NVDA suivra temporairement la revue, jusqu'à ce que le focus ou le curseur système change.
Si vous voulez qu'il ne suive que le focus et le curseur, vous devez configurer le braille pour qu'il suive le focus.
Dans ce cas, le braille ne suivra pas le navigateur NVDA durant la navigation par objet ou le curseur de revue durant la revue.
Si vous voulez que le braille suive la navigation par objet et la revue de texte, vous devez configurer le braille pour qu'il suive la revue.
Dans ce cas, le braille ne suivra pas le focus système et le curseur système.

##### Déplacer le curseur système lors du routage du curseur de revue {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Jamais), Jamais, Seulement quand le braille suit automatiquement, Toujours|
|Défaut |Jamais|

Ce paramètre détermine si le curseur système doit également être déplacé lors d'un appui sur une touche de routage du curseur.
Cette option est définie sur Jamais par défaut, ce qui signifie que le routage ne déplacera jamais le curseur système lors du routage du curseur de revue.

Lorsque cette option est définie sur Toujours et que [Le braille suit](#BrailleTether) est défini sur "automatiquement" ou "la revue", un appui sur une touche de routage du curseur déplacera également le curseur système ou le focus lorsqu'il est pris en charge.
Lorsque le mode de revue actuel est [Revue de l'écran](#ScreenReview), il n'y a pas de curseur physique.
Dans ce cas, NVDA essaie de deplacer le focus à l'objet sous le texte vers lequel vous routez le curseur de revue.
Il en va de même pour le mode de [Revue par objet](#ObjectReview).

Vous pouvez également définir cette option pour ne déplacer le curseur que lorsque "Le braille suit" est défini sur "automatiquement".
Dans ce cas, un appui sur une touche de routage du curseur ne déplacera le curseur système ou le focus que lorsque NVDA est automatiquement attaché au curseur de revue, alors qu'aucun mouvement ne se produira lorsqu'il sera manuellement attaché au curseur de revue.

Cette option est uniquement active si "[Le braille suit](#BrailleTether)" est défini sur "automatiquement" ou sur "la revue".

Pour parcourir les modes de déplacement du curseur système lors du routage du curseur de revue depuis n'importe où, veuillez attribuer un geste personnalisé à l'aide de la [boîte de dialogue Gestes de commandes](#InputGestures).

##### Lecture par paragraphe {#BrailleSettingsReadByParagraph}

Si cette option est activée, le braille sera affiché par paragraphe au lieu d'être affiché par ligne.
De la même manière, les commandes de ligne précédente et ligne suivante navigueront par paragraphe.
Cela signifie que vous n'aurez pas besoin de faire défiler l'afficheur à la fin de chaque ligne même si plus de texte peut entrer sur l'afficheur.
Cela permet une lecture plus fluide des textes volumineux.
Par défaut, cette option est désactivée.

##### Ne pas couper les mots quand c'est possible {#BrailleSettingsWordWrap}

Si cette option est activée, un mot trop long pour entrer à la fin de l'afficheur braille ne sera pas coupé.
À la place, il y aura des espaces à la fin de l'affichage.
En faisant défiler l'affichage, vous pourrez lire le mot entier.
Ceci est parfois appelé retour automatique à la ligne.
Notez que si le mot est trop long pour entrer sur l'afficheur, il devra quand-même être coupé.

Si cette option est désactivée, le plus possible du mot sera affiché sur la ligne, mais le reste sera coupé.
En faisant défiler l'affichage, vous pourrez lire le reste du mot.

Activer cette option peut rendre la lecture plus fluide mais vous obligera à faire défiler plus souvent.

##### Afficher le contexte du focus {#BrailleSettingsFocusContextPresentation}

Cette option vous permet de choisir quelles informations contextuelles NVDA affiche en braille quand un objet prend le focus.
Les informations contextuelles font référence à la hiérarchie d'objets contenant le focus.
Par exemple, quand vous focalisez un élément de liste, celui-ci fait partie d'une liste.
Cette liste pourrait être contenue dans un dialogue, etc.
Veuillez consulter la section [navigation par objets](#ObjectNavigation) pour plus d'informations sur la hiérarchie qui s'applique aux objets dans NVDA.

Quand l'option est sur "Seulement lors d'un changement de contexte", NVDA essaie d'afficher autant d'informations contextuelles que possible sur le terminal braille, mais seulement pour les parties du contexte qui ont changé.
Dans l'exemple ci-dessus, cela signifie que quand le focus est sur la liste, NVDA affiche l'élément de liste sur le terminal braille.
De plus, s'il y a assez de place libre sur le terminal braille, NVDA essaie de montrer que l'élément de liste fait partie d'une liste.
Si vous commencer à vous déplacer dans la liste avec les flèches, on suppose que vous savez que vous êtes toujours dans la liste
Ainsi, pour les autres éléments de la liste que vous focalisez, NVDA affiche seulement l'élément de liste focalisé sur le terminal.
Si vous voulez lire à nouveau le contexte (ex : si vous êtes dans une liste et que la liste fait partie d'un dialogue), vous devrez activer le défilement arrière de votre terminal braille.

Quand l'option est sur "Toujours", NVDA essaie d'afficher autant d'informations contextuelles que possible sur le terminal braille, même si vous avez déjà vu les mêmes informations précédemment.
L'avantage est que NVDA essaie de mettre autant d'informations que possible sur le terminal.
Cependant, l'inconvénient est que le focus ne démarre pas toujours à la même position sur l'afficheur braille.
Cela peut rendre difficile le parcours d'une longue liste d'éléments, car vous devrez en permanence déplacer vos doigts pour trouver le début de chaque élément.
C'était le comportement par défaut jusqu'à NVDA 2017.2.

Quand l'option est sur "Seulement lors du défilement arrière", NVDA ne montre jamais les informations contextuelles sur le terminal.
Ainsi, dans l'exemple ci-dessus, NVDA affiche l'élément de liste que vous avez focalisé.
Cependant, si vous voulez lire le contexte (ex : que vous êtes dans une liste et que la liste fait partie d'un dialogue), vous devrez activer le défilement arrière de votre terminal.

Pour modifier l'option "Afficher le contexte du focus" de n'importe où, veuillez assigner un geste de commande personnalisé en utilisant [le dialogue Gestes de Commandes](#InputGestures).

##### Interrompre la parole pendant le défilement {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Activé), Activé, Désactivé|
|Défaut |Activé|

Ce paramètre détermine si la parole doit être interrompue lorsque l'afficheur braille défile vers l'arrière/vers l'avant.
Les commandes de ligne précédente/suivante interrompent toujours la parole.

La parole en cours peut être une distraction lors de la lecture du braille.
Pour cette raison, l'option est activée par défaut, interrompant la parole lors du défilement du braille.

La désactivation de cette option permet d'entendre la parole tout en lisant simultanément le braille.

##### Afficher la sélection {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Activé), Activé, Désactivé|
|Défaut |Activé|

Ce réglage détermine si l'indicateur de sélection (points 7 et 8) s'affiche sur l'afficheur braille.
L'option est activée par défaut, donc l'indicateur de sélection est affiché.
L'indicateur de sélection peut être une distraction lors de la lecture.
La désactivation de cette option peut améliorer la lisibilité.

Pour basculer l'affichage de la sélection de n'importe où, veuillez attribuer un geste personnalisé à l'aide de la [boîte de dialogue Gestes de commandes](#InputGestures).

#### Choisir l'afficheur braille {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Ouvrir le dialogue de sélection de l'afficheur braille {#OpenSelectBrailleDisplay}

Raccourci clavier : `NVDA+contrôle+a`

Le dialogue Choisir l'Afficheur Braille, qui peut être ouvert en activant le bouton Changer... dans la catégorie Braille du dialogue Paramètres, vous permet de choisir l'afficheur Braille qui sera utilisé par NVDA.
Quand vous aurez choisi votre afficheur braille, vous pourrez presser le bouton OK et NVDA chargera l'afficheur sélectionné.
S'il y a une erreur au chargement du pilote de l'afficheur, NVDA vous avertira par un message et continuera à utiliser l'afficheur précédent si défini.

##### Terminal braille {#SelectBrailleDisplayDisplay}

Cette liste déroulante vous présente plusieurs options en fonction des pilotes d'afficheurs brailles présents sur votre système.
Déplacez-vous entre les options en utilisant les flèches.

L'option automatique permet à NVDA de rechercher beaucoup de terminaux braille en arrière-plan.
Quand cette fonctionnalité est activée et que vous connectez un terminal braille supporté via USB ou Bluetooth, NVDA se connectera automatiquement à ce terminal.

Pas de braille signifie que vous n'utilisez pas le braille.

Reportez-vous à la section [Terminaux braille pris en charge](#SupportedBrailleDisplays) pour les informations concernant les terminaux braille et ceux qui supportent la détection automatique en arrière-plan.

##### Afficheurs à détecter automatiquement {#SelectBrailleDisplayAutoDetect}

Lorsque l'afficheur braille est réglé sur "Automatique", les cases à cocher de ce contrôle de liste vous permettent d'activer et de désactiver les pilotes d'affichage qui seront impliqués dans le processus de détection automatique.
Cela vous permet d'exclure les pilotes d'afficheur braille que vous n'utilisez pas régulièrement.
Par exemple, si vous possédez uniquement un terminal qui nécessite le pilote Baum pour fonctionner, vous pouvez laisser le pilote Baum activé tandis que les autres pilotes peuvent être désactivés.

Par défaut, tous les pilotes prenant en charge la détection automatique sont activés.
Tout pilote ajouté, par exemple dans une future version de NVDA ou dans une extension, sera également activé par défaut.

Veuillez consulter la documentation de votre plage braille dans la section [Afficheurs braille supportés](#SupportedBrailleDisplays) pour vérifier si le pilote prend en charge la détection automatique des afficheurs.

##### Port {#SelectBrailleDisplayPort}

Cette option, si disponible, vous permet de choisir quel port ou type de connexion sera utilisé pour communiquer avec l'afficheur braille sélectionné.
C'est une liste déroulante contenant les choix possibles pour votre afficheur braille.

Par défaut, NVDA emploie la détection automatique, ce qui veut dire que la connexion avec le périphérique braille sera établie automatiquement en recherchant les périphériques USB et Bluetooth connectés à votre ordinateur.
De plus, pour certains afficheurs braille, vous pourrez choisir explicitement le port à utiliser.
Les options communes sont "automatique" (qui spécifie à NVDA d'employer la procédure par défaut), "USB", "Bluetooth" et port série si votre afficheur braille supporte ce type de communication.

Cette option ne sera pas disponible si votre afficheur braille supporte seulement la détection automatique du port.

Vous devrez consulter la documentation de votre afficheur braille dans la section [Afficheurs braille supportés](#SupportedBrailleDisplays) pour plus de détails sur les types de communications supportés et les ports disponibles.

Note : Si vous connectez plusieurs Afficheurs Braille utilisant le même pilote en même temps à votre machine  (Ex. connexion de deux afficheurs Seika),
il est actuellement impossible de dire à NVDA quel afficheur utiliser.
Par conséquent, il est recommandé de ne connecter qu'un seul afficheur braille d'un type/fabricant donné à votre machine à la fois.

#### Audio {#AudioSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres audio {#OpenAudioSettings}

Raccourci clavier : `NVDA+contrôle+u`

La catégorie Audio du dialogue des Paramètres de NVDA contient des options qui vous permettent de modifier plusieurs aspects de la sortie audio.

##### Sortie audio {#SelectSynthesizerOutputDevice}

Cette option vous permet de choisir le périphérique audio par lequel NVDA doit indiquer au synthétiseur sélectionné de parler.

<!-- KC:setting -->

##### Mode d'Atténuation Audio {#SelectSynthesizerDuckingMode}

Raccourci clavier : `NVDA+maj+d`

Cette option vous permet de choisir si NVDA doit baisser le volume des autres applications quand il parle, ou tout le temps quand il est en cours d'exécution.

* Ne jamais atténuer : NVDA ne baissera jamais le volume des autres applications.
* Atténuer les autres sources quand NVDA parle : NVDA ne baissera le son des autres applications que quand il parle ou émet un son. Ceci peut ne pas fonctionner avec tous les synthétiseurs.
* Toujours atténuer : NVDA réduira le son des autres applications tout le long de son exécution.

Cette option n'est disponible que si NVDA a été installé.
Il n'est pas possible de supporter l'atténuation audio pour les versions portables et temporaires de NVDA.

##### Le volume des sons NVDA suit le volume de la voix {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Désactivé, Activé|
|Défaut |Désactivé|

Lorsque cette option est activée, le volume des sons et des bips de NVDA suivra le réglage du volume de la voix que vous utilisez.
Si vous diminuez le volume de la voix, le volume des sons diminuera.
De même, si vous augmentez le volume de la voix, le volume des sons augmentera.
Cette option n'est pas disponible si vous avez démarré NVDA avec [WASAPI désactivé pour la sortie audio](#WASAPI) dans les Paramètres avancés.

##### Volume des sons NVDA {#SoundVolume}

Ce potentiomètre vous permet de régler le volume des sons et des bips de NVDA.
Ce paramètre ne prend effet que lorsque "Le volume des sons NVDA suit le volume de la voix" est désactivé.
Cette option n'est pas disponible si vous avez démarré NVDA avec [WASAPI désactivé pour la sortie audio](#WASAPI) dans les Paramètres avancés.

##### Séparation du son {#SelectSoundSplitMode}

La fonction de séparation du son permet aux utilisateurs d'utiliser leurs périphériques de sortie stéréo, tels que des écouteurs et des haut-parleurs.
La séparation du son permet d'avoir la parole de NVDA sur un canal (par exemple gauche) et de faire en sorte que toutes les autres applications diffusent leur son sur l'autre canal (par exemple droit).
Par défaut, la séparation du son est désactivée.
Un geste de commande permet de parcourir les différents modes de séparation du son :
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Faire défiler les modes de séparation du son |`NVDA+alt+s` |Passer d'un mode de séparation du son à l'autre.|

<!-- KC:endInclude -->

Par défaut, cette commande alternera entre les modes suivants :

* Séparation du son désactivée : NVDA n'applique aucun traitement de séparation du son.
* NVDA à gauche et applications à droite : NVDA parlera dans le canal de gauche, tandis que les autres applications diffuseront leur son dans le canal de droite.
* NVDA à gauche et applications dans les deux canaux : NVDA parlera dans le canal de gauche, tandis que les autres applications diffuseront leur son dans les deux canaux, gauche et droit.

Il existe des modes de séparation du son plus avancés disponibles dans la liste déroulante des paramètres NVDA.
Parmi ces modes, le mode "NVDA dans les deux canaux et applications dans les deux canaux" force tous les sons à être dirigés dans les deux canaux.
Ce mode peut différer du mode "Séparation du son désactivé" dans le cas où un autre traitement audio interférerait avec les volumes des canaux.

Veuillez noter que le séparateur de son ne fonctionne pas comme un mélangeur audio.
Par exemple, si une application joue une piste audio stéréo alors que la séparation du son est définie sur "NVDA à gauche et applications à droite", alors vous n'entendrez que le canal droit de la piste audio, tandis que le canal gauche de la piste sera mis en sourdine.

Cette option n'est pas disponible si vous avez démarré NVDA avec [WASAPI désactivé pour la sortie audio](#WASAPI) dans les Paramètres avancés.

Veuillez noter que si NVDA plante, il ne sera pas en mesure de restaurer le volume sonore des applications et il se pourrait que ces applications continuent à diffuser leur son sur un seul canal après le crash de NVDA.
Pour corriger ce problème, veuillez redémarrer NVDA et sélectionner le mode "NVDA dans les deux canaux et applications dans les deux canaux".

##### Personnalisation des modes de séparation du son {#CustomizeSoundSplitModes}

Cette liste de cases à cocher permet de sélectionner quels modes de séparation du son sont inclus lors du passage de l'un à l'autre en utilisant `NVDA+alt+s`.
Les modes non cochés sont exclus.
Par défaut, seuls trois modes sont inclus.

* Séparation du son désactivée : NVDA et les applications diffusent des sons dans les canaux gauche et droit.
* NVDA à gauche et applications à droite.
* NVDA à gauche et applications dans les deux canaux.

Veuillez noter qu'il est nécessaire de cocher au moins un mode.
Cette option n'est pas disponible si vous avez démarré NVDA avec [WASAPI désactivé pour la sortie audio](#WASAPI) dans les Paramètres avancés.

##### Durée de maintien en éveil du périphérique audio après la parole {#AudioAwakeTime}

Cette zone d'édition spécifie combien de temps NVDA maintient le périphérique audio en éveil après la fin de la parole.
Cela permet à NVDA d'éviter certains problèmes de parole comme des parties de mots coupées.
Cela peut se produire lorsque des appareils audio (en particulier les appareils Bluetooth et sans fil) passent en mode veille.
Cela peut également être utile dans d'autres cas d'utilisation, par exemple lors de l'exécution de NVDA dans une machine virtuelle (par exemple Citrix Virtual Desktop) ou sur certains ordinateurs portables.

Des valeurs faibles peuvent provoquer une coupure de l'audio plus souvent, car un appareil peut passer en mode veille trop tôt, provoquant ainsi une coupure du début de la parole suivante.
Une valeur trop élevée peut entraîner une décharge plus rapide de la batterie du périphérique de sortie audio, car il reste active plus longtemps alors qu'aucun son n'est envoyé.

Vous pouvez mettre cette durée à zéro afin de désactiver cette fonctionnalité.

#### Vision {#VisionSettings}

La catégorie Vision du dialogue des paramètres NVDA vous permet d'activer, désactiver et configurer les [aides visuelles](#Vision).

Notez que les options disponibles dans cette catégorie pourraient être étendues par des [extensions NVDA](#AddonsManager).
Par défaut, cette catégorie de paramètres contient les options suivantes :

##### Mise en Évidence Visuelle {#VisionSettingsFocusHighlight}

Les cases à cocher du groupe Mise en Évidence Visuelle contrôlent le comportement de la fonctionnalité interne de [Mise en Évidence Visuelle](#VisionFocusHighlight)de NVDA.

* Activer la mise en évidence: Active/désactive la mise en évidence visuelle.
* Mettre en évidence le focus système : définit si le [focus système](#SystemFocus) sera mis en évidence.
* Mettre en évidence l'objet navigateur : définit si [l'objet navigateur](#ObjectNavigation) sera mis en évidence.
* Mettre en évidence le curseur du mode navigation : Définit si le [Curseur virtuel du mode navigation](#BrowseMode) sera mis en évidence.

Notez que cocher ou décocher la case "Activer la Mise en évidence" changera également l'état des trois autres cases à cocher  en conséquence.
Ainsi, si "Activer la Mise en évidence" n'est pas cochée et que vous la cochez, les trois autres cases seront cochées automatiquement.
Si vous voulez mettre en évidence seulement le focus et laisser les cases objet navigateur et mode navigation non cochées, l'état de la case "Activer la mise en évidence" sera semicoché.

##### Le Rideau d'Écran {#VisionSettingsScreenCurtain}

Vous pouvez activer le [Rideau d'Écran](#VisionScreenCurtain) en cochant la case "Rendre l'écran noir (effet immédiat)".
Un avertissement indiquant que l'écran deviendra noir après activation sera alors affiché
Avant de continuer (en sélectionnant "Oui"), vérifiez que vous avez activé la parole ou le braille et que vous serez capable de contrôler votre ordinateur sans utiliser l'écran.
Sélectionnez "Non" si vous ne souhaitez plus activer le Rideau d'Écran.
Si vous êtes sûr, vous pouvez choisir le bouton Oui pour activer le Rideau d'Écran.
Si vous ne voulez plus voir cet avertissement à chaque fois, vous pouvez changer ce comportement dans le dialogue qui affiche le message.
Vous pouvez toujours restaurer l'avertissement en cochant la case "Toujours afficher un avertissement au chargement du Rideau d'Écran" à côté de la case "Rendre l'écran noir".

Par défaut, des sons sont émis quand le Rideau d'Écran est activé ou désactivé.
Si vous souhaitez changer ce comportement, vous pouvez décocher la case " Émettre un son lors du basculement du rideau d'écran ".

##### Paramètres des aides visuelles tierses {#VisionSettingsThirdPartyVisualAids}

Des services d'aide visuelle additionnels peuvent être fournis dans des [Extensions NVDA](#AddonsManager).
Si ces services ont des paramètres ajustables, ils seront affichés dans cette catégorie de paramètres dans des groupes séparés.
Pour les paramètres supportés par un service, veuillez vous référer à la documentation pour ce service.

#### Clavier {#KeyboardSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres Clavier {#OpenKeyboardSettings}

Raccourci clavier : `NVDA+contrôle+k`

La catégorie Clavier du dialogue Paramètres de NVDA contient des options qui définissent le comportement de NVDA quand vous utilisez ou tapez sur votre clavier.
Cette catégorie de paramètres contient les options suivantes :

##### Configuration du clavier {#KeyboardSettingsLayout}

Cette liste déroulante vous permet de choisir la configuration de clavier utilisée par NVDA. Actuellement, les deux configurations fournies avec NVDA sont : Desktop (ordinateur de bureau) et Laptop (ordinateur portable).

##### Choisir les Touches NVDA {#KeyboardSettingsModifiers}

Les cases à cocher de cette liste contrôlent quelles touches peuvent être utilisées comme [touches NVDA](#TheNVDAModifierKey). Vous pouvez choisir parmi les touches suivantes :

* La touche Verrouillage Majuscule
* La touche insertion du pavé numérique
* La touche insertion étendue (elle se trouve généralement au-dessus des flèches, près de début et fin)

Si aucune touche n'est choisie pour être la touche NVDA, il peut être impossible d'accéder à de nombreuses commandes de NVDA, vous devez donc cocher au moins une des touches.

<!-- KC:setting -->

##### Écho clavier par caractère {#KeyboardSettingsSpeakTypedCharacters}

Raccourci clavier : NVDA+2

Quand cette case est cochée, NVDA prononcera chaque caractère tapé au clavier.

<!-- KC:setting -->

##### Écho clavier par mot {#KeyboardSettingsSpeakTypedWords}

Raccourci clavier : NVDA+3

Quand cette case est cochée, NVDA prononcera chaque mot tapé au clavier.

##### Interruption de la parole à la frappe d'un caractère {#KeyboardSettingsSpeechInteruptForCharacters}

Si cette option est activée, la parole sera interrompue à chaque fois qu'un caractère est saisi. Cette option est activée par défaut.

##### Interruption de la parole à l'appui de la touche Entrée {#KeyboardSettingsSpeechInteruptForEnter}

Si cette option est activée, la parole sera interrompue à chaque fois que la touche "Entrée" est appuyée. Cette option est activée par défaut.

##### Permettre le survol en mode dire tout {#KeyboardSettingsSkimReading}

Si cette option est activée, certaines commandes de navigation (telles que les touches de navigation rapide en mode navigation ou l'exploration par ligne ou par paragraphe) n'arrêtent pas dire tout, qui reprend plutôt la lecture à la nouvelle position.

##### Émettre un bip à la frappe d'un caractère minuscule quand le verrouillage majuscule est activé {#KeyboardSettingsBeepLowercase}

Quand cette case est cochée, on entend un bip d'avertissement si on entre une lettre en combinaison avec la touche Majuscule alors que le Verrouillage Majuscule est activé.
Généralement, la frappe des lettres en majuscule quand les Majuscules sont verrouillées n'est pas intentionnelle et est généralement due au fait qu'on a oublié que la touche Majuscule est activée.
Cela peut donc être utile d'en être averti.

<!-- KC:setting -->

##### Dire les touches de commandes {#KeyboardSettingsSpeakCommandKeys}

Raccourci clavier : NVDA+4

Quand cette case est cochée, NVDA annonce, lors de leur frappe, toutes les touches ne correspondant pas à des caractères. Ceci inclut les combinaisons de touches telles que "contrôle" plus une autre lettre.

##### Jouer un son pour les fautes d'orthographe durant la frappe {#KeyboardSettingsAlertForSpellingErrors}

Quand cette option est activée, un court son de vibreur sera émis quand un mot que vous frappez contient une faute d'orthographe.
Cette option n'est disponible que si l'annonce des fautes d'orthographe est activée dans [Mise en Forme des Documents](#DocumentFormattingSettings) qui se trouve dans le dialogue Paramètres de NVDA.

##### Exécuter les touches d'autres applications {#KeyboardSettingsHandleKeys}

Cette option permet à l'utilisateur de choisir si les combinaisons de touches générées par des applications telles que les claviers à l'écran et les logiciels de reconnaissance vocale doivent être traitées par NVDA.
Cette option est activée par défaut, mais certains utilisateurs souhaiteraient la désactiver, comme ceux tapant en vietnamien avec le logiciel de dactylographie UniKey, car cela causerait la saisie de caractères incorrects.

#### Souris {#MouseSettings}

<!-- KC:setting -->

##### Ouvrire les paramètres de souris {#OpenMouseSettings}

Raccourci clavier : `NVDA+contrôle+m`

La catégorie Souris du dialogue Paramètres de NVDA permet de définir le mode de suivi de la souris par NVDA, de sonoriser les coordonnées de la souris par des bips et de définir d'autres options d'utilisation de la souris.
Elle contient les options suivantes :

##### Annoncer les changements de forme de la souris {#MouseSettingsShape}

Quand cette case est cochée, NVDA annonce la forme du pointeur souris chaque fois qu'elle change.
Sous Windows, le pointeur de souris change de forme pour transmettre certaines informations comme indiquer que quelque chose devient modifiable, ou que quelque chose est en train de se charger, etc.

<!-- KC:setting -->

##### Activer le suivi de la souris {#MouseSettingsTracking}

Raccourci clavier : NVDA+m

Quand cette case est cochée, NVDA annonce le texte présent sous le pointeur souris, lorsqu'on la déplace sur l'écran. Cela vous permet de trouver un objet sur l'écran en déplaçant la souris au lieu de recourir à la navigation par objet.

##### Résolution d'unités de texte {#MouseSettingsTextUnit}

Si NVDA est configuré pour annoncer le texte sous la souris quand vous la déplacez, cette option vous permet de choisir précisément la quantité de texte qui sera lue.
Les options sont caractère, mot, ligne ou paragraphe.

Pour activer la résolution d'unités de texte de n'importe où, veuillez assigner un geste de commande personnalisé en utilisant le dialogue [Gestes de Commandes](#InputGestures).

##### Annoncer l'objet quand la souris y entre {#MouseSettingsRole}

Quand cette case est cochée, NVDA annonce des informations sur les objets quand la souris y entre.
Cela comprend le rôle (type) de l'objet ainsi que les états (coché/appuyé), les coordonnées des cellules dans les tableaux, etc.
Veuillez Noter que l'annonce de certains détails d'objet peut dépendre de la façon dont d'autres paramètres sont définis, tels que les paramètres dans les catégories [Présentation des objets](#ObjectPresentationSettings) ou [Mise en Forme des Documents](#DocumentFormattingSettings).

##### Sonoriser les coordonnées quand la souris se déplace {#MouseSettingsAudio}

Quand cette case est cochée, NVDA émet des bips quand la souris se déplace, pour que l'utilisateur puisse se figurer la position de la souris sur l'écran.
Plus la souris est haut sur l'écran, plus la fréquence des bips est élevée.
Plus la souris est à gauche ou à droite sur l'écran, plus le son sera émis à gauche ou à droite, dans la mesure où l'utilisateur possède des haut-parleurs ou un casque stéréophoniques.

##### La brillance modifie le volume des coordonnées audio {#MouseSettingsBrightness}

Si la case "Sonoriser les coordonnées quand la souris se déplace" est cochée, le volume des bips variera en fonction de la brillance de la zone sous le pointeur de la souris.
Cette case est décochée par défaut.

##### Ignorer les entrées souris d'autres applications {#MouseSettingsHandleMouseControl}

Cette option permet à l'utilisateur d'ignorer les événements relatifs à la souris (incluant le déplacement et l'appui sur les boutons) générés par d'autres applications telles que TeamViewer et autres logiciels de contrôle à distance.
Cette option est décochée par défaut.
Si vous cochez cette option et que l'option "suivi de la souris" est activée, NVDA n'annoncera pas ce qui est sous la souris si la souris est déplacée par une autre application.

#### Interaction tactile {#TouchInteraction}

Cette catégorie, disponible seulement sur un ordinateur possédant des capacités tactiles, vous permet de configurer la manière dont NVDA interagit avec l'écran tactile.
Elle contient les options suivantes :

##### Activer le support d'interaction tactile {#TouchSupportEnable}

Cette case à cocher active le support d'interaction tactile de NVDA.
Quand il est activé, vous pouvez utiliser vos doigts pour naviguer et interagir avec les éléments sur l'écran en utilisant un écran tactile.
Quand il est désactivé, le support d'écran tatile est désactivé tant que NVDA est en cours d'exécution.
Ce paramètre peut aussi être activé/désactivé en utilisant NVDA+contrôle+alt+t.

##### Mode de frappe tactile {#TouchTypingMode}

Cette case à cocher vous permet d'indiquer la méthode que vous désirez utiliser pour saisir du texte avec le clavier tactile.
Quand elle est cochée, quand vous repérez une touche sur le clavier tactile, vous pouvez retirer votre doigt et la touche sélectionnée sera pressée.
Quand elle est décochée, vous devez double-taper sur la touche du clavier tactile pour la presser.

#### Curseur de revue {#ReviewCursorSettings}

La catégorie Curseur de Revue du dialogue Paramètres de NVDA sert à configurer le comportement du curseur de revue de NVDA.
Elle contient les options suivantes :

<!-- KC:setting -->

##### Suivre le focus système {#ReviewCursorFollowFocus}

Raccourci clavier : NVDA+7

Quand cette option est activée, le curseur de revue est toujours placé dans le même objet que le focus système quand il change.

<!-- KC:setting -->

##### Suivre le curseur système {#ReviewCursorFollowCaret}

Raccourci clavier : NVDA+6

Quand l'option est activée, le curseur de revue suit les mouvements du curseur système.

##### Suivre le curseur souris {#ReviewCursorFollowMouse}

Quand l'option est activée, le curseur de revue suit les mouvements de la souris.

##### Mode de revue simple {#ReviewCursorSimple}

Quand l'option est activée, NVDA filtre la hiérarchie des objets que l'on peut atteindre, excluant les objets sans intérêt pour l'utilisateur ; Ex : les objets invisibles et les objets utilisés seulement à des fins de présentation.

Pour activer ou désactiver le mode de revue simple depuis n'importe où, veuillez lui assigner un geste de commande personnalisé en utilisant le [dialogue Gestes de Commandes](#InputGestures).

#### Présentation des objets {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres de présentation des objets {#OpenObjectPresentationSettings}

Raccourci clavier : `NVDA+contrôle+o`

La catégorie Présentation des Objets du dialogue Paramètres de NVDA sert à définir la quantité d'informations annoncées par NVDA pour les contrôles tels que leur description, leur position etc.
Ces options ne s'appliquent généralement pas au mode navigation.
Elles s'appliquent généralement aux annonces de focus et à la navigation par objets de NVDA, mais pas à la lecture de contenu textuel, par ex. mode navigation.

##### Annoncer les suggestions {#ObjectPresentationReportToolTips}

Quand cette case est cochée, NVDA annonce les suggestions à leur apparition.
De nombreuses fenêtres et commandes font apparaître un court message (ou suggestion) lorsqu'on y déplace la souris ou le focus.

##### Annoncer les notifications {#ObjectPresentationReportNotifications}

Quand cette case est cochée, NVDA annonce les bulles d'aide et les notifications d'invitation à leur apparition.

* Les bulles d'aide sont semblables aux suggestions mais généralement de plus grande taille, et sont associées à des évènements système tels que le débranchement d'un câble réseau, ou bien des alertes relatives à la sécurité.
* Les notifications d'invitation ont été introduites dans Windows 10 et apparaissent dans le centre de notification  dans la barre d'état système, informant sur divers événements (ex : une mise à jour a été téléchargée, un ouveau courriel est arrivé dans votre boîte de réception, etc.).

##### Annoncer les raccourcis clavier des objets {#ObjectPresentationShortcutKeys}

Quand cette case est cochée, NVDA inclut, à l'annonce d'un objet ou d'une commande, le raccourci clavier qui lui est associé.
Par exemple, le menu "Fichier" d'une barre de menu peut avoir pour raccourci clavier Alt+f.

##### Annoncer le rang de l'objet dans une liste {#ObjectPresentationPositionInfo}

Cette option vous permet de choisir si vous voulez connaître le rang de l'objet dans une liste (ex : 1 sur 4) annoncé quand vous allez sur un objet au moyen du focus ou de la navigation par objet.

##### Deviner le rang de l'objet quand l'information n'est pas disponible {#ObjectPresentationGuessPositionInfo}

Si l'annonce du rang de l'objet dans une liste est activée, cette option autorise NVDA à deviner le rang de l'objet si cette information n'est pas disponible pour un objet particulier.

Quand l'option est activée, NVDA annonce le rang pour un plus grand nombre de contrôles tels que les menus et les barres d'outils. Cependant, cette information peut parfois être inexacte.

##### Annonce de la description des objets {#ObjectPresentationReportDescriptions}

Décochez cette case si vous pensez que vous n'avez pas besoin d'entendre leur description annoncée avec les objets.

<!-- KC:setting -->

##### Suivi des barres de progression {#ObjectPresentationProgressBarOutput}

Raccourci clavier : NVDA+u

Cette option vous présente une liste déroulante qui contrôle la manière dont NVDA vous annonce l'évolution des barres de progression.

Elle propose les options suivantes :

* Désactivé : L'évolution des barres de progression ne sera pas annoncée.
* Vocal : Cette option dit à NVDA d'annoncer l'évolution des barres de progression en pourcentage. Chaque fois que la barre changera, NVDA dira la nouvelle valeur.
* Par des bips : Cette option dit à NVDA d'émettre un bip à chaque évolution de la barre de progression. Plus le bip est aigu, plus on approche de la fin de la barre.
* Vocal avec des bips : Cette option dit à NVDA de parler et d'émettre des bips lors de la mise à jour de la barre de progression.

##### Suivre les barres de progression en arrière-plan {#ObjectPresentationReportBackgroundProgressBars}

Quand cette case est cochée, NVDA annonce les barres de progression même si elles ne sont pas physiquement sur la fenêtre en avant-plan.
Si vous minimisez ou quittez une fenêtre qui contient une barre de progression, NVDA continuera à la surveiller, vous permettant de faire autre chose pendant ce temps.

<!-- KC:setting -->

##### Annoncer les changements de contenu dynamiques {#ObjectPresentationReportDynamicContent}

Raccourci clavier : NVDA+5

Active ou désactive l'annonce d'un nouveau contenu en particulier dans les applications telles que les terminaux ou l'historique des programmes de tchat.

##### Jouer un son quand une autosuggestion apparaît {#ObjectPresentationSuggestionSounds}

Active/désactive l'annonce de l'apparition des autosuggestions, si activé, NVDA jouera un son pour l'indiquer.
Les autosuggestions sont des listes de saisies suggérées basées sur le texte entré dans certains champs de saisie et documents.
Par exemple, quand vous entrez du texte dans la boîte de recherche du menu démarrer de Windows Vista et au-delà, Windows affiche une liste de suggestions basée sur ce que vous avez entré.
Pour certains champs d'édition comme le champ de recherche dans diverses applications Windows 10, NVDA peut vous signaler qu'une liste de suggestions est apparue quand vous tapez du texte.
La liste de suggestions se ferme quand vous quittez le champ d'édition, et pour certains champs, NVDA peut vous en avertir quand ça arrive.

#### Composition de saisie {#InputCompositionSettings}

La catégorie Composition de la Saisie permet de contrôler comment NVDA annonce la saisie des caractères asiatiques, avec IME ou les services de texte et langue d'entrée.
Notez que, comme les méthodes de saisie varient considérablement selon les fonctions disponibles et la façon dont elles transmettent l'information, il sera probablement nécessaire de configurer ces options différemment pour chaque méthode de saisie, pour obtenir la meilleure expérience de saisie possible.

##### Annonce automatique de toutes les suggestions disponibles {#InputCompositionReportAllCandidates}

Cette option, activée par défaut, permet de choisir si oui ou non toutes les suggestions visibles doivent être automatiquement rapportées quand une liste de suggestions apparaît ou quand sa page change.
Activer cette option sur les méthodes d'entrée pictographiques telles que chinois Nouveau ChangJie ou Boshiami est utile car vous pouvez entendre automatiquement tous les symboles et leurs numéros, et vous pouvez en choisir un tout de suite.
Toutefois, pour les méthodes de saisie phonétique comme le nouveau chinois phonétique, il peut être plus utile de désactiver cette option puisque tous les symboles ont les mêmes sons et vous devrez utiliser les touches fléchées pour naviguer dans les éléments de la liste individuellement pour obtenir plus d'informations de la description de caractères pour chaque suggestion.

##### Annoncer la suggestion sélectionnée {#InputCompositionAnnounceSelectedCandidate}

Cette option, activée par défaut, vous permet de choisir si NVDA doit ou non annoncer la suggestion sélectionnée lorsqu'une liste de suggestions apparaît ou quand la sélection est changée.
Pour les méthodes où la suggestion peut être changée en utilisant les flèches (comme chinois nouveau phonétique) cela est nécessaire, cependant pour certaines méthodes il est préférable de désactiver cette option.
Notez que même si cette option est désactivée, le curseur de revue se placera toujours sur la suggestion sélectionnée, vous permettant toujours d'utiliser la navigation par objet ou le curseur de revue pour sélectionner la suggestion.

##### Toujours inclure une description courte du caractère pour les suggestions {#InputCompositionCandidateIncludesShortCharacterDescription}

Cette option, activée par défaut, permet de choisir si oui ou non NVDA doit fournir une description courte de chaque caractère d'une suggestion, quand elle est sélectionnée ou lors de la lecture de la liste quand elle apparaît.
Notez que pour les langues comme le chinois, l'annonce des descriptions de caractères supplémentaires pour la suggestion sélectionnée n'est pas affectée par cette option.
Cette option est utile pour les méthodes d'entrées coréennes et japonaises.

##### Annonce les changements dans la chaîne en cours de lecture {#InputCompositionReadingStringChanges}

Certains modes de saisie tels que le chinois ChangJie phonétique et Nouveau ChangJie peuvent avoir une chaîne de lecture (parfois connu sous le nom de chaîne de précomposition).
Avec cette option, vous pouvez choisir si oui ou non NVDA doit annoncer les nouveaux caractères saisis dans la chaîne de lecture en cours.
Cette option est activée par défaut.
Notez que certaines anciennes méthodes comme le chinois ChangJie n'utilisent pas la chaîne en cours de lecture pour les caractères de précomposition, utilisez directement la chaîne de composition. Voyez l'option suivante pour configurer l'annonce de la chaîne de composition.

##### Annoncer les changements dans la chaîne de composition {#InputCompositionCompositionStringChanges}

Après que les données de lecture ou de précomposition ont été combinées en un symbole pictographique valide, la plupart des méthodes d'entrée placent ce symbole dans une chaîne de composition pour stocker temporairement avec les autres symboles combinés avant de les insérer dans le document.
Cette option permet de choisir si oui ou non NVDA doit annoncer tous les symboles quand ils apparaissent dans la chaîne de composition.
Cette option est activée par défaut.

#### Mode navigation {#BrowseModeSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres du mode navigation {#OpenBrowseModeSettings}

Raccourci clavier : `NVDA+contrôle+b`

La catégorie Mode Navigation du dialogue Paramètres de NVDA sert à configurer le comportement de NVDA quand vous naviguez dans des documents complexes tels que des pages web.
Elle contient les options suivantes :

##### Nombre maximum de caractères par ligne {#BrowseModeSettingsMaxLength}

Ce champ définit, en nombre de caractères, la longueur maximum d'une ligne en mode navigation.

##### Nombre maximum de lignes par page {#BrowseModeSettingsPageLines}

Ce champ définit le nombre de lignes dont on se déplace par appui sur "Page Précédente" ou "Page Suivante" en mode navigation.

<!-- KC:setting -->

##### Utiliser la disposition telle qu'à l'écran {#BrowseModeSettingsScreenLayout}

Raccourci clavier : NVDA+v

Cette option vous permet de spécifier si le mode navigation doit placer le contenu cliquable (liens, boutons et champs) sur sa propre ligne, ou s'il doit le conserver dans le flux du texte tel qu'il est affiché visuellement.
Notez que cette option ne concerne pas les applications Microsoft Office telles qu'Outlook et Word, qui utilisent toujours la disposition telle qu'à l'écran.
Lorsque la disposition telle qu'à l'écran est activée, les éléments de la page restent tels qu'ils sont affichés visuellement.
Par exemple, une ligne visuelle de plusieurs liens sera présentée vocalement et en braille comme plusieurs liens sur la même ligne.
S'il est désactivé, les éléments de la page seront placés sur leurs propres lignes.
Ceci peut être plus facile à comprendre lors de la navigation ligne par ligne dans la page et peut faciliter l'interaction avec les éléments pour certains utilisateurs.

##### Activer le mode navigation au chargement de la page {#BrowseModeSettingsEnableOnPageLoad}

Cette case à cocher permet de choisir si le mode navigation doit être activé automatiquement au chargement d'une page.
Quand cette option est désactivée, le mode navigation peut quand-même être activé manuellement sur les pages ou documents où il est supporté.
Veuillez consulter la section [Mode navigation](#BrowseMode) pour avoir une liste des applications supportées par le mode navigation.
Notez que cette option ne s'applique pas aux situations où le mode navigation est toujours optionnel, par exemple sous Microsoft Word.
Cette option est activée par défaut.

##### Dire tout automatiquement au chargement des pages {#BrowseModeSettingsAutoSayAll}

Cette case à cocher active ou désactive la lecture automatique des pages après leur chargement en mode navigation.
Cette option est activée par défaut.

##### Annoncer les tables de disposition {#BrowseModeSettingsIncludeLayoutTables}

Cette option affecte la façon dont NVDA gère les tableaux utilisées uniquement à des fins de mise en page.
Lorsqu'elle est activée, NVDA les traitera comme des tableaux normaux en les annonçant en fonction des [Paramètres de Mise en forme des documents](#DocumentFormattingSettings) et en les localisant par les commandes de navigation rapides.
Lorsqu'elle est désactivée, ces tableaux ne seront ni annoncés ni trouvés par la navigation rapide.
Cependant, le contenu des tableaux sera toujours inclus sous forme de texte normal.
Cette option est désactivée par défaut.

Pour activer/désactiver l'inclusion des tables de disposition de n'importe où, veuillez assigner un geste personnalisé en utilisant [le dialogue Gestes de commandes](#InputGestures).

##### Configurer l'annonce de champs tels que liens et titres {#BrowseModeLinksAndHeadings}

Veuillez consulter les options dans [Mise en forme des Documents](#DocumentFormattingSettings) du dialogue [Paramètres de NVDA](#NVDASettings) pour configurer les champs qui sont annoncés durant la navigation tels que les liens, les titres et les tableaux.

##### Mode formulaire automatique au changement de focus {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Cette option permet au mode formulaire d'être invoqué au changement de focus.
Par exemple, dans une page web, si vous tabulez et arrivez sur un formulaire : si cette option est cochée, le mode formulaire sera automatiquement activé.

##### Mode formulaire automatique au déplacement du curseur {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Cette option, quand elle est cochée, permet à NVDA d'activer ou désactiver le mode formulaire quand on se déplace avec les flèches.
Par exemple, si vous naviguez dans une page web avec les flèches et que vous arrivez sur une zone d'édition, NVDA passera automatiquement en mode formulaire.
Si vous sortez de la zone d'édition, le mode formulaire sera automatiquement désactivé.

##### Indication audio du mode formulaire ou navigation {#BrowseModeSettingsPassThroughAudioIndication}

Si cette option est activée, NVDA émettra des sons particuliers au passage du mode formulaire au mode navigation plutôt que d'annoncer le changement verbalement.

##### Empêcher les gestes ne correspondant pas à des commandes d'atteindre le document {#BrowseModeSettingsTrapNonCommandGestures}

Activée par défaut, cette option vous permet de choisir si des gestes (tels que l'appui sur des touches) qui ne déclenchent pas une commande NVDA et ne sont pas considérés comme une commande en général, devraient être interceptés pour ne pas interagir avec le document actuellement en focus.
Par exemple, si l'option est activée, si la lettre j est pressée, elle sera interceptée pour ne pas atteindre le document, même si ce n'est ni une touche de navigation rapide ni une commande dans l'application elle-même.
Dans ce cas NVDA demandera à Windows de jouer un son par défaut quand une touche interceptée est pressée.

<!-- KC:setting -->

##### Amener automatiquement le focus système aux éléments focalisables {#BrowseModeSettingsAutoFocusFocusableElements}

Raccourci clavier : NVDA+8

Désactivée par défaut, cette option vous permet de choisir si le focus système doit être automatiquement positionné aux éléments pouvant prendre le focus système (liens, champs de saisie, etc.) quand on parcourt le contenu avec le curseur de mode navigation.
Laisser cette option désactivée ne focalisera pas automatiquement les éléments focalisables quand ils seront sélectionnés avec le curseur du mode navigation.
Cela pourrait apporter une expérience de navigation plus rapide et une meilleure réactivité en mode navigation.
Le focus sera alors mis à jour lors d'une interaction avec un élément particulier (ex : l'appui d'un bouton, le cochage d'une case à cocher).
Activer cette option peut améliorer le support de quelques sites web au détriment de la performance et de la stabilité.

#### Mise en forme des documents (NVDA+contrôle+d) {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Ouvrir les paramètres de mise en forme des documents {#OpenDocumentFormattingSettings}

Raccourci clavier : `NVDA+contrôle+d`

La plupart des options de cette catégorie servent à définir quelles informations de mise en forme vous souhaitez entendre automatiquement lorsque vous parcourez un document.
Par exemple, si on coche la case "Annoncer le nom de la police", à chaque fois que les flèches amènent sur un texte avec une police différente, le nom de la police est annoncé.

Les options de mise en forme des document sont organisées par groupes ;
On peut configurer les annonces suivantes :

* Police,
  * Nom de la police
  * Taille de la police,
  * Attributs de la police,
  * Exposants et indices
  * Emphase
  * Texte surligné (marqué)
  * Style
  * Couleurs
* Informations sur le document
  * Commentaires
  * Signets
  * Modifications de l'éditeur
  * Fautes d'orthographe
* Pages et espacement
  * Numéros de page
  * Numéros de ligne
  * Annonce du retrait de ligne [(Désactivé, Parole, Sons, Parole et Sons)](#DocumentFormattingSettingsLineIndentation)
  * Ignorer les lignes vides pour l'annonce du retrait de ligne
  * Retrait des paragraphes (ex. retrait négatif, retrait de première ligne)
  * interligne (simple, double etc.)
  * Alignement
* Informations sur les tableaux
  * Tableaux
  * En-têtes des lignes et colonnes (désactivé, lignes, colonnes, lignes et colonnes)
  * Coordonnées des cellules
  * Bordure des cellules (désactivé, Styles, Couleurs et Styles)
* Éléments
  * Titres
  * Liens
  * Graphiques
  * Listes
  * Citations
  * Groupes
  * Régions
  * Articles
  * Cadres
  * Figures et légendes
  * Cliquable

Pour modifier ces paramètres de n'importe où, veuillez assigner un geste personnalisé en utilisant le [dialogue Gestes de Commandes](#InputGestures).

##### Annonce des changements de mise en forme après le curseur {#DocumentFormattingDetectFormatAfterCursor}

Si on l'active, ce paramètre dit à NVDA de détecter tous les changements de mise en forme sur une ligne et de les signaler pendant la lecture. Attention, cela peut dégrader les performances de NVDA.

Par défaut, NVDA détecte la mise en forme sous le curseur système ou le curseur de revue, et, dans certains cas, sur toute la ligne à condition que cela ne dégrade pas les performances.

Activez cette option quand vous révisez un document dans une application telle que Wordpad et que la mise en forme est importante.

##### Annonce des retraits de lignes {#DocumentFormattingSettingsLineIndentation}

Cette option vous permet de configurer la manière dont les retraits en début de ligne sont annoncés.
La liste déroulante "Annoncer les retraits de ligne par" a quatre options :

* Désactivé : NVDA ne traitera pas les retraits de lignes.
* Parole : Si parole est sélectionnée, quand le niveau de retrait change, NVDA dit quelque chose comme "douze espaces" ou "quatre tabulations.".
* Sons : Si sons est sélectionné, quand le niveau de retrait change, des sons indiquent la quantité de changement dans le retrait.
La hauteur du son montera pour chaque espace, et pour une tabulation, la hauteur montera de l'équivalent de 4 espaces.
* Parole et sons : Cette option indique les retraits en utilisant les deux méthodes ci-dessus.

Si vous cochez la case "Ignorer les lignes vides pour l'annonce de retrait de ligne", les modifications d'indentation ne seront pas signalées pour les lignes vides.
Cela peut être utile lors de la lecture d'un document dans lequel des lignes vides sont utilisées pour séparer des blocs de texte en retrait, comme dans le code source de programmation.

#### Navigation dans les documents {#DocumentNavigation}

Cette catégorie vous permet d'ajuster divers aspects de la navigation dans les documents.

##### Style des paragraphes {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Géré par l' application), géré par l' application, Saut de ligne unique, Saut de ligne multiple|
|Défaut |Géré par l'application|

Cette liste déroulante vous permet de sélectionner le style de paragraphe à utiliser lors de la navigation par paragraphes avec `contrôle+flècheHaut` et `contrôle+flècheBas`.
Les styles de paragraphe disponibles sont :

* Géré par l'application : NVDA laissera l'application déterminer le paragraphe précédent ou suivant, et NVDA lira le nouveau paragraphe lors de la navigation.
Ce style fonctionne mieux lorsque l'application prend en charge la navigation dans les paragraphes de manière native et est la valeur par défaut.
* Saut de ligne simple : NVDA tentera de déterminer le paragraphe précédent ou suivant en utilisant un saut de ligne simple comme indicateur de paragraphe.
Ce style fonctionne mieux lors de la lecture de documents dans une application qui ne prend pas en charge nativement la navigation dans les paragraphes, et dont les paragraphes du document sont marqués par une simple pression sur la touche `entreé`.
* Saut de ligne multiple : NVDA tentera de déterminer le paragraphe précédent ou suivant en utilisant au moins une ligne vierge (deux appuis sur la touche `entreé`) comme indicateur de paragraphe.
Ce style fonctionne mieux lorsque vous travaillez avec des documents qui utilisent des paragraphes de bloc.
Notez que ce style de paragraphe ne peut pas être utilisé dans Microsoft Word ou Microsoft Outlook, sauf si vous utilisez l'UIA pour accéder aux contrôles de Microsoft Word.

Vous pouvez basculer entre les styles de paragraphe disponibles de n'importe où en attribuant une touche dans la [boîte de dialogue Gestes de commandes](#InputGestures).

#### Reconnaissance Optique de Caractères de Windows {#Win10OcrSettings}

Les paramètres de cette catégorie vous permettent de configurer la [Reconnaissance de Caractères de Windows](#Win10Ocr).
Elle contient les options suivantes :

##### Langue de Reconnaissance {#Win10OcrSettingsRecognitionLanguage}

Cette liste déroulante vous permet de choisir la langue à utiliser pour la reconnaissance de texte.
Pour faire défiler les langues disponibles à partir de n'importe quel endroit, veuillez assigner un geste de commande personnalisé en utilisant [le dialogue Gestes de Commandes](#InputGestures).

##### Actualiser périodiquement le contenu reconnu {#Win10OcrSettingsAutoRefresh}

Lorsque cette case est cochée, NVDA actualisera automatiquement le contenu reconnu lorsqu'un résultat de reconnaissance aura le focus.
Cela peut être très utile lorsque vous souhaitez surveiller un contenu en constante évolution, par exemple lorsque vous regardez une vidéo avec sous-titres.
Le rafraîchissement a lieu toutes les secondes et demie.
Cette option est désactivée par défaut.

#### Paramètres avancés {#AdvancedSettings}

Avertissement ! Les paramètres dans cette catégorie sont pour les utilisateurs avancés et peuvent provoquer un mauvais fonctionnement de NVDA si mal configurés.
Ne modifiez ces paramètres que si vous êtes sûr de ce que vous faites ou si un développeur NVDA vous a demandé de le faire.

##### Modifier les paramètres avancés {#AdvancedSettingsMakingChanges}

Pour pouvoir modifier les paramètres avancés, les contrôles doivent être activés en confirmant, via la case à cocher, que vous comprenez les risques qu'il y a à modifier ces paramètres

##### Rétablir les paramètres par défaut {#AdvancedSettingsRestoringDefaults}

Le bouton rétablit les valeurs par défaut des paramètres, même si la case de confirmation n'est pas cochée.
Après avoir modifié les paramètres vous pouvez souhaiter revenir aux valeurs par défaut.
Cela peut aussi être le cas si vous n'êtes pas sûr que les paramètres ont été modifiés.

##### Activer le chargement de code personnalisé depuis le Répertoire Bloc-notes du Développeur {#AdvancedSettingsEnableScratchpad}

Quand vous développez des extensions pour NVDA, il est utile de pouvoir tester le code en cours d'écriture.
Cette option, lorsqu'elle est activée, permet à NVDA de charger des modules applicatifs personnalisés, des modules globaux, des pilotes d'afficheurs braille, des pilotes de synthétiseur et des fournisseurs d'amélioration visuelle, à partir d'un répertoire spécial bloc-notes du développeur dans votre répertoire de configuration utilisateur NVDA.
Comme leurs équivalents dans les extensions, ces modules sont chargés au démarrage de NVDA ou, dans le cas des modules applicatifs et globaux, lors du [rechargement des modules](#ReloadPlugins).
Cette option est désactivée par défaut, garantissant qu'aucun code non testé n'est exécuté par NVDA sans que l'utilisateur en ait explicitement connaissance.
Si vous voulez distribuer du code spécifique à d'autres personnes, vous devriez l'empaqueter sous forme d'extension pour NVDA.

##### Ouvrir le Répertoire Bloc-notes du Développeur {#AdvancedSettingsOpenScratchpadDir}

Ce bouton ouvre le répertoire où vous pouvez placer le code personnalisé que vous êtes en train de développer.
Ce bouton n'est disponible que si NVDA est configuré pour permettre le chargement de code personnalisé depuis le répertoire Bloc-notes du développeur.

##### Enregistrement des événements et modifications de propriété UI Automation {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Automatique, Sélectif, Global|
|Défaut |Automatique|

Cette option change la façon dont NVDA enregistre les événements déclenchés par l'API d'accessibilité UI Automation de Microsoft.
La liste déroulante Enregistrement des événements et modifications de propriété UI Automation a trois options :

* Automatique : "sélectif" sous Windows 11 Sun Valley 2 (version 22H2) et ultérieur, "global" sinon.
* Sélectif : NVDA limitera l'enregistrement des événements au focus système pour la plupart des événements
Si vous rencontrez des problèmes de performances dans une ou plusieurs applications, nous vous recommandons d'essayer cette fonctionnalité pour voir si les performances s'améliorent.
Cependant, sur les anciennes versions de Windows, NVDA peut avoir des difficultés à suivre le focus dans certains contrôles (tels que le gestionnaire de tâches et le panneau emoji).
* Global : NVDA enregistre de nombreux événements UIA qui sont traités et rejetés dans NVDA lui-même.
Bien que le suivi du focus soit plus fiable dans un plus grand nombre de situations, les performances sont considérablement dégradées, en particulier dans des applications telles que Microsoft Visual Studio.

##### Utiliser UI automation pour accéder aux contrôles des documents Microsoft Word {#MSWordUIA}

Configure si NVDA doit ou non utiliser l'API d'accessibilité UI Automation pour accéder aux documents Microsoft Word, plutôt que l'ancien modèle d'objet Microsoft Word.
Cela s'applique aux documents dans Microsoft Word lui-même, ainsi qu'aux messages dans Microsoft Outlook.
Ce paramètre contient les valeurs suivantes :

* Défaut (Lorsque c'est adapté)
* Seulement si nécessaire : quand le modèle d'objet Microsoft Word n'est pas disponible du tout
* Lorsque c'est adapté : Microsoft Word version 16.0.15000 ou supérieure, ou lorsque le modèle d'objet Microsoft Word n'est pas disponible
* Toujours : partout où UI automation est disponible dans Microsoft Word (quel que soit l'avancement de son développement)

##### Utilisez UI Automation pour accéder aux contrôles de feuille de calcul Microsoft Excel quand disponible {#UseUiaForExcel}

Lorsque cette option est activée, NVDA essaiera d'utiliser l'API d'accessibilité de Microsoft UI Automation pour récupérer les informations depuis les contrôles de la feuille de calcul Microsoft Excel.
Il s'agit d'une fonctionnalité expérimentale et certaines fonctionnalités de Microsoft Excel peuvent ne pas être disponibles dans ce mode.
Par exemple, la liste des éléments de NVDA pour lister les formules et les commentaires, et la navigation rapide en mode navigation pour sauter aux champs de formulaire sur une feuille de calcul ne sont pas disponibles.
Cependant, pour la navigation/l'édition de base d'une feuille de calcul, cette option peut améliorer considérablement les performances.
Nous ne recommandons toujours pas que la majorité des utilisateurs l'activent par défaut, mais nous invitons les utilisateurs de Microsoft Excel version 16.0.13522.10000 ou supérieure à tester cette fonctionnalité et à nous faire part de leurs commentaires.
L'implémentation de UI Automation dans Microsoft Excel est en constante évolution et les versions de Microsoft Office antérieures à 16.0.13522.10000 peuvent ne pas exposer suffisamment d'informations pour que cette option soit d'une quelconque utilité.

##### Utiliser le traitement des événements amélioré {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Activé), Désactivé, Activé|
|Défaut |Activé|

Lorsque cette option est activée, NVDA devrait rester réactif lorsqu'il est submergé de nombreux événements UI Automation, par ex. de grandes quantités de texte dans un terminal.
Après avoir modifié cette option, vous devrez redémarrer NVDA pour que la modification prenne effet.

##### Prise en charge de la Console Windows {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Automatique, UIA si disponible, Héritée|
|Défaut |Automatique|

Cette option sélectionne la façon dont NVDA interagit avec la console Windows utilisée par l'invite de commande, PowerShell et le sous-système Windows pour Linux.
Cela n'affecte pas le terminal Windows moderne.
Dans Windows 10 version 1709, Microsoft [a ajouté la prise en charge de son API UI Automation à la console](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), apportant des performances et une stabilité considérablement améliorées pour les lecteurs d'écran qui la prennent en charge.
Dans les situations où l'automatisation de l'interface utilisateur n'est pas disponible ou connue pour entraîner une expérience utilisateur inférieure, la prise en charge de la console héritée de NVDA est disponible comme solution de secours.
La liste déroulante de prise en charge de la console Windows comporte trois options :

* Automatique : utilise UI Automation dans la version de la console Windows incluse avec Windows 11 version 22H2 et versions ultérieures.
Cette option est recommandée et définie par défaut.
* UIA si disponible : utilise l'automatisation de l'interface utilisateur dans les consoles si disponible, même pour les versions avec des implémentations incomplètes ou boguées.
Bien que cette fonctionnalité limitée puisse être utile (et même suffisante pour votre utilisation), l'utilisation de cette option est entièrement à vos risques et périls et aucune assistance ne sera fournie.
* Héritée : l'automatisation de l'interface utilisateur dans la console Windows sera complètement désactivée.
L'héritage de secours sera toujours utilisé même dans les situations où UI Automation offrirait une expérience utilisateur supérieure.
Par conséquent, le choix de cette option n'est pas recommandé, sauf si vous savez ce que vous faites.

##### Utiliser UIA avec Microsoft Edge et autres navigateurs basés sur Chromium quand c'est possible {#ChromiumUIA}

Cette option permet de définir quand UIA sera utilisé si disponible dans les navigateurs basés sur Chromium tels que Microsoft Edge.
Le support d'UIA pour les navigateurs basés sur Chromium est au début de son développement et peut ne pas apporter le même niveau d'accessibilité que IA2.
La liste déroulante contient les options suivantes :

* Défaut (Seulement quand nécessaire) : C'est actuellement la valeur par défaut de NVDA. Cette valeur par défaut peut changer à l'avenir en fonction de l'amélioration de la technologie.
* Seulement quand nécessaire : Quand NVDA est incapable d'injecter dans le processus du navigateur de quoi utiliser IA2 et que UIA est disponible, NVDA utilisera UIA.
* Oui : Si le navigateur rend UIA disponible, NVDA l'utilisera.
* Non : Ne pas utiliser UIA, même si NVDA ne peut pas injecter dans le processus. Ceci peut être utile pour les développeurs corrigeant des problèmes liés à IA2 et voulant s'assurer que NVDA ne revient pas à UIA.

##### Annotations {#Annotations}

Ce groupe d'options est utilisé pour activer des fonctionnalités qui ajoutent une prise en charge expérimentale des annotations ARIA.
Certaines de ces fonctionnalités peuvent être incomplètes.

<!-- KC:beginInclude -->
Pour "Signaler le résumé de tous les détails d'annotation au niveau du curseur système", appuyez sur NVDA+d.
<!-- KC:endInclude -->

Les options suivantes existent :

* "Annoncer 'contient des détails' pour les annotations structurées" : active l'annonce si le texte ou le contrôle contient plus de détails.
* "Toujours annoncer aria-description" :
  Lorsque la source de `accDescription` est aria-description, la description est annoncée.
  Ceci est utile pour les annotations sur le web.
  Note :
  * Il existe de nombreuses sources pour `accDescription` plusieurs ont une sémantique mixte ou peu fiable.
    Historiquement, les technologies d'assistance n'ont pas été en mesure de différencier les sources de `accDescription` généralement, elle n'a pas été annoncée en raison de la sémantique mixte.
  * Cette option est en développement très précoce, elle repose sur des fonctionnalités de navigateur pas encore largement disponibles.
  * Elle devrait fonctionner avec Chromium 92.0.4479.0+

##### Signaler les régions Actives {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Activé), Désactivé, Activé|
|Défaut |Activé|

Cette option définit si NVDA signale les changements dans certains contenus Web dynamiques en Braille.
Désactiver cette option équivaut au comportement de NVDA dans les versions 2023.1 et antérieures, qui ne signalaient ces changements de contenu que par la parole.

##### Énoncer les mots de passe dans tous les terminaux améliorés {#AdvancedSettingsWinConsoleSpeakPasswords}

Ce paramètre définit si les caractères sont prononcés en [écho clavier par caractère](#KeyboardSettingsSpeakTypedCharacters) ou [écho clavier par mot](#KeyboardSettingsSpeakTypedWords) dans les situations où l'écran ne se met pas à jour (comme la saisie du mot de passe) dans certains programmes de terminal, tels que la console Windows avec l'automatisation de l'interface utilisateur support activé et Mintty.
Pour des raisons de sécurité, ce paramètre devrait être laissé désactivé.
Cependant, vous souhaiterez peut-être l'activer si vous rencontrez des problèmes de performances ou une instabilité avec les annoncess de caractères et/ou de mots saisis dans les consoles, ou si vous travaillez dans des environnements de confiance et préférez l'annonce du mot de passe.

##### Utiliser la prise en charge améliorée de la saisie de caractères dans l'ancienne console Windows lorsqu'elle est disponible {#AdvancedSettingsKeyboardSupportInLegacy}

Cette option active une méthode alternative pour détecter les caractères saisis dans les anciennes consoles Windows.
Bien qu'elle améliore les performances et empêche certains affichages de console d'être épelés, elle peut être incompatible avec certains programmes de terminaux.
Cette fonctionnalité est disponible et activée par défaut sous Windows 10 versions 1607 et ultérieures quand UI Automation n'est pas disponible ou désactivée.
Avertissement : quand cette option est activée, les caractères tapés qui n'apparaissent pas à l'écran comme les mots de passe, ne seront pas supprimés.
Dans les environnement non sûrs, vous pouvez désactiver temporairement [Écho clavier par caractère](#KeyboardSettingsSpeakTypedCharacters) et [Écho clavier par mot](#KeyboardSettingsSpeakTypedWords) quand vous entrez un mot de passe.

##### Algorithme de comparaison du texte {#DiffAlgo}

Ce paramètre définit comment NVDA détermine le nouveau texte à annoncer dans les terminaux.
La liste déroulante Algorithme de comparaison du texte a trois options :

* Automatique : Cette option fait que NVDA préfère Diff Match Patch dans la plupart des situations, mais se rabat sur Difflib dans les applications problématiques, telles que les anciennes versions de la console Windows et de Mintty.
* Diff Match Patch : Cette option permet à NVDA de calculer les modifications apportées au texte du terminal par caractère, même dans les situations où cela n'est pas recommandé.
Cela peut améliorer les performances quand de grandes quantités de texte sont écrites à la console et permet l'annonce plus précises des changements intervenant en milieu de ligne.
Cependant, dans certaines applications, la lecture d'un nouveau texte peut être saccadée ou incohérente.
* Difflib : cette option permet à NVDA de calculer les modifications apportées au texte du terminal par ligne, même dans les situations où cela n'est pas recommandé.
Ce comportement est identique à celui de NVDA en version 2020.4 et antérieures.
Ce paramètre peut stabiliser la lecture du texte entrant dans certaines applications.
Cependant, dans les terminaux, lors de l'insertion ou de la suppression d'un caractère au milieu d'une ligne, le texte après le curseur sera lu.

##### Annoncez un nouveau texte dans le terminal Windows via {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Comparaison du texte), Comparaison du texte, Notifications UIA|
|Défaut |Comparaison du texte|

Cette option sélectionne la façon dont NVDA détermine quel texte est "nouveau" (et donc ce qu'il faut prononcer lorsque "signaler les changements de contenu dynamique" est activé) dans Windows Terminal et le contrôle WPF Windows Terminal utilisé dans Visual Studio 2022.
Elle n'affecte pas la console Windows (`conhost.exe`).
La liste déroulante annoncer le nouveau texte dans le terminal Windows comporte trois options :

* Par défaut : cette option est actuellement équivalente à "différence", mais il est prévu qu'elle change une fois que la prise en charge des notifications UIA sera développée davantage.
* Différence : cette option utilise l'algorithme de comparaison sélectionné pour calculer les changements à chaque fois que le terminal affiche un nouveau texte.
Ceci est identique au comportement de NVDA dans les versions 2022.4 et antérieures.
* Notifications UIA : Cette option reporte la responsabilité de déterminer quel texte parler au terminal Windows lui-même, ce qui signifie que NVDA n'a plus à déterminer quel texte actuellement à l'écran est "nouveau".
Cela devrait nettement améliorer les performances et la stabilité de Windows Terminal, mais cette fonctionnalité n'est pas encore complète.
En particulier, les caractères saisis qui ne s'affichent pas à l'écran, tels que les mots de passe, sont signalés lorsque cette option est sélectionnée.
De plus, les étendues contiguës d'affichage de plus de 1 000 caractères peuvent ne pas être rapportées avec précision.

##### Tenter d'interrompre la parole pour les événements de focus expirés {#CancelExpiredFocusSpeech}

Cette option active un comportement qui tente d'interrompre la parole pour les événements de focus expirés.
En particulier se déplacer rapidement parmi les messages dans Gmail sous Chrome peut amener NVDA à annoncer des informations périmées.
Cette fonctionnalité est activée par défaut à partir de NVDA 2021.1.

##### Délai d'attente de mouvement du curseur (en ms) {#AdvancedSettingsCaretMoveTimeout}

Cette option vous permet de configurer le nombre de millisecondes durant lequel NVDA attendra le déplacement du curseur (point d'insertion) dans les contrôles de texte éditable.
Si vous trouvez que NVDA semble mal suivre le curseur ex : il semble être toujours un caractère en retard ou il répète les lignes, alors vous pouvez essayer d'accroître cette valeur.

##### Annoncer la transparence pour les couleurs {#ReportTransparentColors}

Cette option permet d'annoncer lorsque les couleurs sont transparentes, utile pour les développeurs d'extensions qui collectent des informations pour améliorer l'expérience utilisateur avec une application tierce.
Certaines applications GDI mettent en surbrillance le texte avec une couleur d'arrière-plan, NVDA (via le modèle d'affichage) tente de signaler cette couleur.
Dans certaines situations, l'arrière-plan du texte peut être entièrement transparent, le texte étant superposé sur un autre élément de l'interface graphique.
Pour plusieurs API GUI historiquement populaires, le texte peut être rendu avec un arrière-plan transparent, mais visuellement, la couleur d'arrière-plan est précise.

##### Utiliser WASAPI pour la sortie audio {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Défaut (Activé), Désactivé, Activé|
|Défaut |Activé|

Cette option active la sortie audio via l'API Windows Audio Session (WASAPI).
WASAPI est une architecture audio plus moderne qui peut améliorer la réactivité, les performances et la stabilité de la sortie audio NVDA, y compris la parole et les sons.
Après avoir modifié cette option, vous devrez redémarrer NVDA pour que la modification prenne effet.
La désactivation de WASAPI désactivera les options suivantes :

* [Le volume des sons NVDA suit le volume de la voix](#SoundVolumeFollowsVoice)
* [Volume des sons NVDA](#SoundVolume)

##### Catégories de journalisation de débogage {#AdvancedSettingsDebugLoggingCategories}

Les cases à cocher dans cette liste vous permettent d'activer des catégories spécifiques de messages de débogage dans le journal de NVDA.
La journalisation de ces messages peut dégrader la performance et produire de gros fichiers de journal.
N'activez l'une d'entre elle que si un développeur de NVDA vous l'a spécifiquement demandé ex : pour déboguer un pilote de terminal braille ne fonctionnant pas correctement.

##### Jouer un son pour les erreurs journalisées {#PlayErrorSound}

Cette option vous permet de spécifier si NVDA joue un son d'erreur au cas où une erreur est enregistrée.
En sélectionnant Uniquement dans les versions de test (par défaut), NVDA émet des sons d'erreur uniquement si la version actuelle de NVDA est une version de test (alpha, bêta ou exécutée à partir de la source).
En sélectionnant Oui les sons d'erreur sont activés quelle que soit votre version actuelle de NVDA.

##### Expression régulière pour la navigation par paragraphes de texte {#TextParagraphRegexEdit}

Ce champ permet aux utilisateurs de personnaliser l'expression régulière pour détecter les paragraphes de texte en mode navigation.
La [commande de navigation par paragraphe de texte](#TextNavigationCommand) recherche les paragraphes correspondant à cette expression régulière.

### Autres paramètres {#MiscSettings}

En plus du dialogue [Paramètres](#NVDASettings), le sous-menu Préférences du menu NVDA contient plusieurs autres éléments décrits ci-dessous.

#### Dictionnaires de prononciation {#SpeechDictionaries}

Le menu "Dictionnaires de prononciation" du menu "Préférences" contient des dialogues qui vous permettent de gérer la manière dont NVDA prononce certains mots ou phrases.
Il y a actuellement trois types de dictionnaires.
Ce sont :

* Défaut : les règles de ce dictionnaire affectent la parole dans tout NVDA.
* Voix : les règles de ce dictionnaire n'affectent que la voix en cours d'utilisation.
* Temporaire : les règles de ce dictionnaire affectent tout NVDA mais seulement pour la session en cours.

Vous devez assigner des gestes personnalisés en utilisant le [dialogue Gestes de Commandes](#InputGestures) si vous voulez ouvrir l'un de ces dialogues de dictionnaire depuis n'importe où.

Tous les dialogues des dictionnaires contiennent une liste de règles qui seront utilisées pour produire la parole.
Le dialogue contient aussi des boutons "Ajouter", "Éditer", "Supprimer" et "Tout supprimer".

Pour ajouter une nouvelle règle au dictionnaire, cliquez sur le bouton "Ajout", remplissez les champs dans le dialogue puis cliquez sur "OK".
Vous verrez ainsi votre nouvelle règle dans la liste des règles.
Cependant, pour être sûr que votre règle est vraiment sauvegardée, n'oubliez pas de cliquer sur le bouton "OK" pour quitter le dialogue de dictionnaire une fois que vous aurez fait toutes vos modifications.

Les règles des dictionnaires de NVDA vous permettent de remplacer une chaîne de caractères par une autre.
Par exemple, vous pourrez vouloir que NVDA prononce le mot "grenouille" chaque fois qu'il rencontre le mot "oiseau".
Dans le dialogue d'ajout de règles, la manière la plus simple de faire cela est d'entrer le mot "oiseau" dans la zone "modèle" et le mot "grenouille" dans la zone de remplacement.
Vous pouvez aussi ajouter un commentaire décrivant la règle dans la zone commentaire, quelque chose comme "Remplacer oiseau par grenouille".

Cependant, les dictionnaires de NVDA font bien mieux que le simple remplacement de mot.
Le dialogue "Ajout de règles" contient une case à cocher permettant de choisir si vous voulez que la règle respecte la casse pour que NVDA tienne compte des majuscules et minuscules.
Par défaut, NVDA ne tient pas compte de la casse.

Pour finir, un ensemble de boutons radio vous permet de dire à NVDA si votre modèle devrait s'appliquer partout, seulement dans le cas d'un mot entier ou s'il devrait être traité comme une "expression régulière".
Définir le modèle comme un mot entier signifie que le remplacement ne sera fait que si le modèle n'est pas rencontré dans un mot plus grand.
Un caractère non alphanumérique ou un souligné ou pas de caractère doit être présent immédiatement avant et après le modèle.
Ainsi, en utilisant l'exemple précédent de remplacement du mot "oiseau" par le mot "grenouille", si vous le définissez comme un remplacement de mot entier, cela ne marcherait pas pour "oiseaux" ou "damoiseau".

Une expression régulière est un modèle contenant des symboles particuliers vous permettant de trouver une correspondance sur plus d'un caractère à la fois, ou seulement sur les lettres ou les chiffres etc.
Les expressions régulières ne sont pas expliquées dans ce manuel.
Pour un tutoriel d'introduction, veuillez consulter le [Guide des expressions régulières de Python](https://docs.python.org/3.11/howto/regex.html).

#### Prononciation des ponctuations et symboles {#SymbolPronunciation}

Ce dialogue vous permet de modifier la façon dont les ponctuations et autres symboles sont prononcés ainsi que le niveau de symbole auquel ils sont annoncés.

La langue pour laquelle la prononciation des symboles est en cours d'édition sera indiquée dans le titre du dialogue.
Notez que ce dialogue tient compte de l'option "Se baser sur la langue de la voix pour le traitement des caractères et symboles" qui se trouve dans la catégorie [Parole](#SpeechSettings) du dialogue [Paramètres de NVDA](#NVDASettings). Il utilise la langue de la voix plutôt que le paramètre global langue de NVDA quand cette option est activée.

Pour modifier un symbole, sélectionnez-le d'abord dans la liste de symboles.
Vous pouvez filtrer les symboles en entrant le symbole ou une partie du remplacement du symbole dans le champ d'édition Filtrer par.

* Le champ "Remplacement" vous permet de modifier le texte qui doit être prononcé à la place de ce symbole.
* En utilisant le champ "Niveau", vous pouvez ajuster le niveau minimum auquel ce symbole doit être annoncé (aucun, quelques-uns, la plupart ou tous).
Vous pouvez également définir le niveau sur caractère ; dans ce cas, le symbole ne sera pas prononcé quel que soit le niveau de symbole utilisé, avec les deux exceptions suivantes :
  * Quand vous naviguez caractère par caractère.
  * Quand NVDA épelle un texte contenant ce symbole.
* Le champ "Envoyer le symbole réel au synthétiseur" spécifie quand le symbole lui-même (au lieu de son remplacement) devrait être envoyé au synthétiseur.
Ceci est utile si le symbole force le synthétiseur à marquer une pause ou modifie l'inflexion de la voix.
Par exemple, une virgule force le synthétiseur à marquer une pause.
Il y a trois options :
  * jamais : Ne jamais envoyer le symbole réel au synthétiseur.
  * toujours : Toujours envoyer le symbole réel au synthétiseur.
  * seulement au-dessous du niveau du symbole : N'envoyer le symbole réel que si le niveau de symboles configuré est inférieur au niveau assigné à ce symbole.
  Par exemple, vous pourriez utiliser cela pour qu'un symbole ait son remplacement annoncés à hauts niveaux sans marquer de pause, tout en étant indiqué par une pause aux niveaux inférieurs.

Vous pouvez ajouter de nouveaux symboles en pressant le bouton Ajouter.
Dans le dialogue qui apparaît, saisissez le symbole et pressez le bouton OK.
Puis, changez les champs pour le nouveau symbole comme vous le feriez pour les autres symboles.

Vous pouvez supprimer un symbole précédemment ajouté en pressant le bouton Supprimer.

Quand vous avez fini, cliquez sur le bouton "OK" pour sauvegarder vos modifications, ou le bouton "Annuler" pour les supprimer.

Dans le cas de symboles complexes, le champ Remplacement peut inclure quelques références aux groupes du texte source. Par exemple, pour un modèle correspondant à une date complète, \1, \2 et \3 devraient apparaître dans le champ, pour être remplacés par les parties correspondantes de la date.
Ainsi, dans le champ Remplacement, les barres obliques normales doivent être doublées, ex : "a\\b" doit être tapé pour obtenir le remplacement de "a\b".

#### Gestes de commandes {#InputGestures}

Dans ce dialogue, vous pouvez configurer les gestes de commandes (raccourcis clavier, boutons d'un afficheur braille etc.) pour les commandes NVDA.

Seules les commandes qui sont applicables immédiatement avant l'ouverture du dialogue sont affichées.
Par exemple, si vous souhaitez personnaliser des commandes liées au mode navigation, vous devez ouvrir le dialogue des gestes de commandes lorsque vous êtes en mode navigation.

L'arborescence de ce dialogue répertorie toutes les commandes NVDA applicables regroupées par catégories.
Vous pouvez les filtrer en entrant un ou plusieurs mots du nom de la commande dans la zone d'édition Filtrer par dans n'importe quel ordre.
Tous les gestes associés à une commande sont énumérés au niveau suivant la commande.

Pour ajouter un geste à une commande, sélectionnez la commande et appuyez sur le bouton "Ajouter".
Ensuite, effectuez le geste de commande que vous souhaitez associer, par exemple appuyez sur une touche du clavier ou un bouton sur l'afficheur braille.
Parfois, un geste peut être interprété de plusieurs façons.
Par exemple, si vous avez appuyé sur une touche du clavier, vous voudrez peut-être qu'elle soit spécifique à la configuration actuelle du clavier (par exemple, ordinateur de bureau ou ordinateur portable) ou vous voudrez peut-être l'appliquer pour toutes les configurations.
Dans ce cas, un menu apparaît, vous permettant de sélectionner l'option désirée.

Pour supprimer un geste d'une commande, sélectionnez le geste et appuyez sur le bouton "Supprimer".

La catégorie Touches émulées du clavier système contient des commandes NVDA qui émulent des touches sur le clavier du système.
Ces touches émulées du clavier système peuvent être utilisées pour contrôler une touche du système directement depuis votre terminal braille.
Pour ajouter un geste d'émulation, sélectionnez la catégorie Touches émulées du clavier système et pressez le bouton Ajouter.
Puis, pressez sur le clavier la touche que vous voulez émuler.
Après ça, la touche sera disponible dans la catégorie Touche émulées du clavier système et vous pourrez lui assigner un geste de commande comme décrit plus haut.

Note :

* Les touches émulées doivent avoir un geste assigné pour persister lors de la sauvegarde ou de la fermeture du dialogue.
* Un geste de commande avec modificateur peut ne pas pouvoir êttre assigné à un geste émulé sans modificateur
Par exemple, définir le `a` comme touche émulée et configurer un geste de commande `ctrl+m`, peut avoir comme résultat que l'application reçoit `ctrl+a`.

Lorsque vous avez terminé vos modifications, appuyez sur le bouton "OK" pour les sauvegarder ou sur le bouton "Annuler" pour les ignorer.

### Sauvegarder et recharger la configuration {#SavingAndReloading}

Par défaut NVDA sauvegarde automatiquement vos paramètres.
Notez cependant que ce comportement peut être modifié dans le dialogue "Paramètres généraux" du menu "Préférences".
Pour sauvegarder manuellement les paramètres à n'importe quel moment, utilisez l'élément "Sauvegarder la configuration" dans le menu NVDA.

Si vous faites une erreur dans vos paramètres et avez besoin de revenir aux valeurs précédentes, utilisez l'élément "Revenir à la configuration sauvegardée" dans le menu NVDA.
Vous pouvez également réinitialiser votre configuration aux valeurs d'usine en utilisant l'élément "Réinitialiser la configuration aux valeurs par défaut" également disponible dans le menu de NVDA.

Les touches de commandes suivantes sont également utiles :
<!-- KC:beginInclude -->

| Nom |Ordinateur de bureau |Ordinateur portable |Description|
|---|---|---|---|
|Sauvegarder la configuration |NVDA+contrôle+c |NVDA+contrôle+c |Sauvegarde votre configuration pour qu'elle ne soit pas perdue en quittant NVDA|
|Réinitialiser la configuration |NVDA+contrôle+r |NVDA+contrôle+r |Appuyez une fois pour réinitialiser à la configuration qui existait lors de votre dernière sauvegarde. Appuyez trois fois pour revenir à la configuration par défaut de NVDA.|

<!-- KC:endInclude -->

### Profils de configuration {#ConfigurationProfiles}

Parfois, vous souhaiteriez avoir des paramètres différents pour des situations différentes.
Par exemple, vous pourriez avoir l'annonce de retrait activée pendant que vous éditez ou l'annonce des attributs de la police activée pendant que vous corrigez.
NVDA vous permet de faire cela en utilisant des profils de configuration.

Un profil de configuration contient uniquement les paramètres qui sont modifiés alors que le profil est en cours d'édition.
La plupart des paramètres peuvent être modifiés dans les profils de configuration à l'exception de ceux de la catégorie Général du dialogue [Paramètres](#NVDASettings), qui s'appliquent à l'ensemble de NVDA.

Les profils de configuration peuvent être activés manuellement soit à partir d'un dialogue soit en utilisant un geste de commande personnalisé.
Ils peuvent également être activés automatiquement grâce à des déclencheurs tels que le passage à une application particulière.

#### Gestion basique {#ProfilesBasicManagement}

Vous pouvez gérer les profils de configuration en sélectionnant "Profils de configuration" dans le menu NVDA.
Vous pouvez aussi le faire en utilisant un raccourci clavier :
<!-- KC:beginInclude -->

* NVDA+contrôle+p : Afficher le dialogue "Profils de configuration".

<!-- KC:endInclude -->

Le premier élément dans ce dialogue est la liste des profils à partir de laquelle vous pouvez sélectionner un des profils disponibles.
Lorsque vous ouvrez le dialogue, le profil en cours d'édition est sélectionné.
Des informations complémentaires sont également indiquées pour les profils actifs, indiquant s'ils sont activés manuellement, déclenchés et/ou en cours d'édition.

Pour renommer ou supprimer un profil, appuyez sur le bouton "Renommer" ou "Supprimer", respectivement.

Appuyez sur le bouton "Fermer" pour fermer le dialogue.

#### Création d'un profil {#ProfilesCreating}

Pour créer un profil, appuyez sur le bouton "Nouveau".

Dans le dialogue "Nouveau profil", vous pouvez entrer un nom pour le profil.
Vous pouvez également choisir comment ce profil doit être utilisé.
Si vous ne souhaitez utiliser ce profil que manuellement, sélectionnez activation manuelle, qui est la valeur par défaut.
Sinon, sélectionnez un déclencheur qui doit activer automatiquement ce profil.
Pour plus de commodité, si vous n'avez pas saisi un nom pour le profil, sélectionner un déclencheur le fera pour vous.
Reportez-vous [ci-dessous](#ConfigProfileTriggers) pour plus d'informations.

Appuyer sur "OK" crée le profil et ferme le dialogue de configuration de sorte que vous pouvez le modifier.

#### Activation manuelle {#ConfigProfileManual}

Vous pouvez activer manuellement un profil en sélectionnant un profil et en cliquant sur le bouton "Activation manuelle".
Une fois activé, d'autres profils peuvent toujours être activés par des déclencheurs, mais les paramètres dans le profil activé manuellement remplacent ceux des profils activés par ces déclencheurs.
Par exemple, si un profil est déclenché pour l'application actuelle et que l'annonce des liens est activée dans ce profil mais désactivée dans le profil activé manuellement, les liens ne seront pas annoncés.
Toutefois, si vous avez changé la voix dans le profil déclenché mais que vous ne l'avez jamais changée dans le profil activé manuellement, la voix du profil déclenché sera utilisée.
Tous les paramètres que vous modifiez, seront sauvegardés dans le profil activé manuellement.
Pour désactiver un profil activé manuellement, sélectionnez-le dans le dialogue "Profils de configuration" et appuyez sur le bouton "Désactiver manuellement".

#### Déclencheurs {#ConfigProfileTriggers}

En appuyant sur le bouton "Déclencheurs" dans le dialogue "Profils de configuration", vous pouvez modifier les profils qui doivent être activés automatiquement par divers déclencheurs.

La liste des déclencheurs affiche les déclencheurs disponibles, qui sont comme suit :

* Application en cours : déclenché lors de l'activation de l'application en cours.
* Dire tout: déclenché lors de la lecture avec la commande "Dire Tout".

Pour modifier le profil qui doit être automatiquement activé par un déclencheur, sélectionnez le déclencheur, puis sélectionnez le profil désiré dans la liste des profils.
Vous pouvez sélectionner "Configuration normale" si vous ne voulez pas utiliser de profil.

Cliquez sur le bouton "Fermer" pour revenir au dialogue "Profils de configuration".

#### Éditer un profil {#ConfigProfileEditing}

Si vous avez activé manuellement un profil, les paramètres modifiés seront sauvegardés dans ce profil.
Autrement, tous les paramètres modifiés seront sauvegardés dans le profil le plus récemment déclenché.
Par exemple, si vous avez associé un profil avec l'application "Bloc-notes" et que vous basculez vers le "Bloc-notes", tous les paramètres modifiés seront sauvegardés dans ce profil.
Enfin, s'il n'y a ni profil activé manuellement, ni profil déclenché, tous les paramètres que vous modifierez seront sauvegardés dans votre configuration normale.

Pour éditer le profil utilisé dans "Dire Tout", vous devez [activer manuellement](#ConfigProfileManual) ce profil.

#### Désactiver temporairement tous les déclencheurs {#ConfigProfileDisablingTriggers}

Parfois, il peut être utile de désactiver temporairement les déclencheurs.
Par exemple, vous voudrez peut-être modifier un profil activé manuellement ou votre configuration normale sans profils déclenchés interférents.
Vous pouvez le faire en cochant la case "Désactiver temporairement tous les déclencheurs" dans le dialogue "Profils de configuration".

Pour activer ou désactiver les déclencheurs de n'importe où, veuillez assigner un geste de commande en utilisant le dialogue [Gestes de Commandes](#InputGestures).

#### Activer un profil en utilisant les gestes de commandes {#ConfigProfileGestures}

Pour chaque profil que vous ajoutez, vous pouvez assigner un ou plusieurs gestes de commandes pour l'activer.
Par défaut, les profils de configuration n'ont pas de geste de commande assigné.
Vous pouvez ajouter des gestes pour activer un profil en utilisant le dialogue [Gestes de Commandes](#InputGestures).
Chaque profil a sa propre entrée dans la catégorie profils de configuration.
Quand vous renommez un profil, tous les gestes que vous avez ajoutés restent disponibles.
La suppression d'un profil entraîne la suppression de tous les gestes qui lui sont associés.

### Emplacement des fichiers de configuration {#LocationOfConfigurationFiles}

Les versions portables de NVDA enregistrent tous les paramètres et extensions dans un répertoire nommé "userConfig" situé dans le répertoire de votre copie portable de NVDA.

Les versions installées de NVDA enregistrent tous les paramètres et extensions dans un répertoire spécial de NVDA situé dans votre profil utilisateur Windows.
Cela signifie que chaque utilisateur du système peut avoir ses propres paramètres NVDA.
Pour ouvrir votre répertoire de paramètres de n'importe où vous pouvez utiliser [le dialogue Geste de commandes](#InputGestures) pour ajouter un geste personnalisé.
De plus, pour une version installée de NVDA, depuis le menu démarrer vous pouvez aller dans programmes -> NVDA -> explorer le répertoire de configuration utilisateur de NVDA.

Les paramètres qu'utilise NVDA quand il s'exécute sur l'écran de connexion ou l'écran UAC sont enregistrés dans le répertoire "systemConfig" situé dans le répertoire NVDA.
En général, cette configuration n'a pas à être modifiée.
Pour modifier cette configuration, configurez NVDA à votre convenance, sauvegardez la configuration puis cliquez sur le bouton "Utiliser les paramètres NVDA actuellement sauvegardés pour l'écran de connexion à Windows (nécessite des privilèges administrateur)" dans la catégorie Général du dialogue [Paramètres](#NVDASettings).

## Extensions et Add-on Store {#AddonsManager}

Les extensions sont des paquets logiciels qui fournissent des fonctionnalités nouvelles ou modifiées pour NVDA.
Elles sont développées par la communauté NVDA et des organisations externes telles que des fournisseurs commerciaux.
Les extensions peuvent effectuer l'une des opérations suivantes :

* Ajoutez ou améliorez la prise en charge de certaines applications.
* Fournir un support pour des afficheurs braille supplémentaires ou des synthétiseurs vocaux.
* Ajouter ou modifier des fonctionnalités dans NVDA.

L'Add-on Store de NVDA vous permet de parcourir et de gérer les paquets  d'extensions.
Toutes les extensions disponibles dans l'Add-on Store peuvent être téléchargées gratuitement.
Cependant, certaines d'entre elles peuvent exiger que les utilisateurs paient une licence ou un logiciel supplémentaire avant de pouvoir les utiliser.
Les synthétiseurs vocaux commerciaux sont un exemple de ce type d'extension.
Si vous installez une extension avec des composants payants et que vous changez d'avis quant à son utilisation, l'extension peut être facilement supprimée.

L'Add-on Store est accessible depuis le sous-menu Outils du menu NVDA.
Pour accéder à l'Add-on Store de n'importe où, attribuez un geste personnalisé à l'aide de la [boîte de dialogue Gestes de commandes](#InputGestures).

### Parcourir les extensions {#AddonStoreBrowsing}

Lorsqu'il est ouvert, l'Add-on Store affiche une liste d'extensions.
Si vous n'avez pas encore installé d'extension, l'Add-on Store s'ouvrira sur une liste d'extensions disponibles à installer.
Si vous avez installé des extensions, la liste affichera les extensions actuellement installées.

Sélectionner une extension, en vous déplaçant dessus avec les touches fléchées haut et bas, affichera les détails de l'extension.
Les extensions ont des actions associées auxquelles vous pouvez accéder via un [menu d'actions](#AddonStoreActions), telles que l'installation, l'aide, la désactivation et la suppression.
Les actions disponibles changeront selon que l'extension est installée ou non, et si elle est activée ou désactivée.

#### Vues de la liste des extensions {#AddonStoreFilterStatus}

Il existe différentes vues pour les extensions installées, pouvant être mis à jour, disponibles et incompatibles.
Pour changer la vue des extensions, changez l'onglet actif de la liste des extensions en utilisant `ctrl+tab`.
Vous pouvez également `tabuler` dans la liste des vues et vous déplacer à travers elles avec les touches `flècheGauche` et `flècheDroite`.

#### Filtrage des extensions activées ou désactivées {#AddonStoreFilterEnabled}

Normalement, une extension installée est "activée", ce qui signifie qu'elle est en cours d'exécution et disponible dans NVDA.
Cependant, certaines de vos extensions installées peuvent être définies sur l'état "désactivé".
Cela signifie qu'elles ne seront pas utilisées et que leurs fonctions ne seront pas disponibles pendant votre session NVDA en cours.
Vous avez peut-être désactivé une extension parce qu'elle était en conflit avec une autre extension ou avec une certaine application.
NVDA peut également désactiver certaines extensions, si elles s'avèrent incompatibles lors d'une mise à jour de NVDA ; mais vous serez averti si cela se produit.
Les extensions peuvent également être désactivées si vous n'en avez tout simplement pas besoin pendant une période prolongée, mais que vous ne souhaitez pas les désinstaller car vous pensez en avoir besoin à nouveau à l'avenir.

Les listes d'extensions installées et incompatibles peuvent être filtrées par leur état activé ou désactivé.
La valeur par défaut affiche les extensions activées et désactivées.

#### Inclure les extensions incompatibles {#AddonStoreFilterIncompatible}

Les extensions disponibles et pouvant être mises à jour peuvent être filtrées pour inclure les [extensions incompatibles](#incompatibleAddonsManager) qui sont disponibles pour l'installation.

#### Filtrer les extensions par canal {#AddonStoreFilterChannel}

Les extensions peuvent être distribuées via quatre canaux :

* Stable : le développeur a publié ceci en tant qu'extension testée avec une version publiée de NVDA.
* Bêta : Cette extension peut nécessiter des tests supplémentaires, mais elle est publiée pour les commentaires des utilisateurs.
Suggéré pour les premiers utilisateurs.
* Dev : ce canal est suggéré pour être utilisé par les développeurs d'extensions pour tester les modifications d'API non publiées.
Les testeurs alpha de NVDA peuvent avoir besoin d'utiliser une version "Dev" de leurs extensions.
* Externe : extensions installées à partir de sources externes, en dehors de l'Add-on Store.

Pour lister les extensions uniquement pour des canaux spécifiques, modifiez la sélection du filtre "Canal".

#### Recherche d'extensions {#AddonStoreFilterSearch}

Pour rechercher des extensions, utilisez la zone de texte "Rechercher".
Vous pouvez y accéder en appuyant sur `maj+tab` dans la liste des extensions.
Tapez un ou deux mots-clés pour le type d'extension que vous recherchez, puis `tabulation` pour aller à la liste des extensions.
Les extensions seront répertoriées si le texte de recherche peut être trouvé dans l'ID, le nom, l'éditeur l'auteur ou la description de l'extension.

### Actions sur les extensions {#AddonStoreActions}

Les extensions ont des actions associées, telles que installer, aide, désactiver et supprimer.
Pour une extension de la liste des extensions, ces actions sont accessibles via un menu qu'on ouvre en appuyant sur la touche `applications`, `entrée`, un clic droit ou un double-clic sur l'extension.
Ce menu est également accessible par un bouton Actions dans les détails de l'extension sélectionnée.

#### Installation d'extensions {#AddonStoreInstalling}

Ce n'est pas parce qu'une extension est disponible dans l'Add-on Store de NVDA qu'elle a été approuvée ou vérifiée par NV Access ou qui que ce soit d'autre.
Il est très important de n'installer que des extensions provenant de sources de confiance.
La fonctionnalité des extensions est illimitée dans NVDA.
Cela peut inclure l'accès à vos données personnelles ou même à l'ensemble du système.

Vous pouvez installer et mettre à jour des extensions en [parcourant les extensions disponibles](#AddonStoreBrowsing).
Sélectionnez une extension dans l'onglet "Extensions disponibles" ou "Mises à jour".
Utilisez ensuite l'action de mise à jour, d'installation ou de remplacement pour démarrer l'installation.

Vous pouvez également installer plusieurs extensions à la fois.
Cela se fait en sélectionnant plusieurs extensions dans l'onglet des extensions disponibles, puis en activant le menu contextuel sur la sélection et en choisissant l'action "Installer les extensions sélectionnées".

Pour installer une extension que vous avez obtenue en dehors de l'Add-on Store, appuyez sur le bouton "Installer à partir d'une source externe".
Cela vous permettra de rechercher un paquet d'extension (fichier `.nvda-addon`) quelque part sur votre ordinateur ou sur un réseau.
Une fois que vous avez ouvert le paquet d'extension le processus d'installation commencera.

Si NVDA est installé et en cours d'exécution sur votre système, vous pouvez également ouvrir un fichier d'extension directement depuis le navigateur ou le système de fichiers pour commencer le processus d'installation.

Lorsqu'une extension est installée depuis une source externe, NVDA vous demandera de confirmer l'installation.
Une fois l'extension installée, NVDA doit être redémarré pour que l'extension démarre, bien que vous puissiez reporter le redémarrage de NVDA si vous avez d'autres extensions à installer ou à mettre à jour.

#### Suppression des extensions {#AddonStoreRemoving}

Pour supprimer une extension, sélectionnez-la  dans la liste et utilisez l'action Supprimer.
NVDA vous demandera de confirmer la suppression.
Comme pour l'installation, NVDA doit être redémarré pour que l'extension soit complètement supprimée.
En attendant, un statut "En attente de suppression" sera affiché pour cette extension dans la liste.
Comme pour l'installation, vous pouvez également supprimer plusieurs extensions à la fois.

#### Désactivation et activation des extensions {#AddonStoreDisablingEnabling}

Pour désactiver une extension, utilisez l'action "désactiver".
Pour activer une extension précédemment désactivée, utilisez l'action "activer".
Vous pouvez désactiver une extension si l'état de l'extension indique qu'elle est "activée" ou l'activer si l'extension est "désactivée".
Pour chaque utilisation de l'action activer/désactiver, le statut de l'extension change pour indiquer ce qui se passera au redémarrage de NVDA.
Si l'extension était auparavant "désactivée", l'état affichera "activé après le redémarrage".
Si l'extension était précédemment "activée", l'état affichera "désactivé après le redémarrage".
Tout comme lorsque vous installez ou supprimez des extensions, vous devez redémarrer NVDA pour que les modifications prennent effet.
Vous pouvez également activer ou désactiver plusieurs extensions à la fois en sélectionnant plusieurs extensions dans l'onglet des extensions disponibles, puis en activant le menu contextuel sur la sélection et en choisissant l'action appropriée.

#### Examiner les extension et lire les avis {#AddonStoreReviews}

Vous souhaiterez peut-être lire les avis d'autres utilisateurs qui ont déjà utilisé une extension par exemple avant de l'installer ou pendant que vous apprenez à l'utiliser.
En outre, il est utile pour les autres utilisateurs que vous déposiez des commentaires sur les extensions que vous avez testées.
Pour lire les avis sur une extension, sélectionnez-la et utilisez l'action "Avis de la communauté".
Cela renvoie vers une page Web de discussion GitHub, où vous pourrez lire et rédiger des avis sur l'extension.
Veuillez noter que cela ne remplace pas une communication directe avec les développeurs d'extension.
Le but de cette fonctionnalité est plutôt de partager des commentaires pour aider les utilisateurs à décider si une extension peut leur être utile.

### Extensions incompatibles {#incompatibleAddonsManager}

Certaines extensions anciennes peuvent ne plus être compatibles avec la version de NVDA que vous possédez.
Si vous utilisez une ancienne version de NVDA, certaines nouvelles extensions peuvent ne pas être compatibles non plus.
Toute tentative d'installation d'une extension incompatible entraînera une erreur expliquant pourquoi l'extension est considérée comme incompatible.

Pour les extensions plus anciennes, vous pouvez ignorer l'incompatibilité à vos risques et périls.
Les extensions incompatibles peuvent ne pas fonctionner avec votre version de NVDA et peuvent provoquer un comportement instable ou inattendu, y compris des plantages.
Vous pouvez ignorer la compatibilité lors de l'activation ou de l'installation d'une extension.
Si l'extension incompatible cause des problèmes ultérieurement, vous pouvez la désactiver ou la supprimer.

Si vous rencontrez des problèmes pour exécuter NVDA et que vous avez récemment mis à jour ou installé une extension, en particulier s'il s'agit d'une extension incompatible, vous pouvez essayer d'exécuter temporairement NVDA avec toutes les extensions désactivées.
Pour redémarrer NVDA avec toutes les extensions désactivées, choisissez l'option appropriée lorsque vous quittez NVDA.
Vous pouvez également utiliser l'[option de ligne de commande](#CommandLineOptions) `--disable-addons`.

Vous pouvez parcourir les extensions incompatibles disponibles à l'aide des [onglets d'extensions disponibles et mises à jour](#AddonStoreFilterStatus).
Vous pouvez parcourir les extensions incompatibles installées à l'aide de l'[onglet extensions incompatibles](#AddonStoreFilterStatus).

## Outils Additionnels {#ExtraTools}
### Visionneuse du Journal {#LogViewer}

La visionneuse du journal, située dans "Outils" du menu NVDA, vous permet de consulter les événements enregistrés depuis le démarrage de la dernière session de NVDA.

En plus de lire le contenu, vous pouvez également sauvegarder une copie du journal ou réactualiser la visionneuse de manière à charger les nouveaux événements générés après que la visionneuse ait été ouverte.
Ces actions sont disponibles dans le menu Journal de la visionneuse.

Le fichier qui s'affiche lorsque vous ouvrez la visionneuse de journaux est enregistré sur votre ordinateur à l'emplacement du fichier `%temp%\nvda.log`.
Un nouveau fichier de journal est créé à chaque démarrage de NVDA.
A ce moment, le fichier de journal de la session NVDA précédente est déplacé vers `%temp%\nvda-old.log`.

Vous pouvez également copier un fragment du fichier de journal courant dans le presse-papiers sans ouvrir la visionneuse de journaux.
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Ouvrir la visionneuse de journaux |`NVDA+f1` |Ouvre la visionneuse de journaux et affiche des informations pour le développeur sur l'objet navigateur courant.|
|Copier un fragment du journal dans le presse-papiers |`NVDA+contrôle+maj+f1` |Au premier appui, le point de départ pour le contenu du journal qui doit être capturé est défini. Au deuxième appui, le contenu du journal depuis le point de départ est copié dans votre presse-papiers.|

<!-- KC:endInclude -->

### Visionneuse de Parole {#SpeechViewer}

Pour les développeurs voyants ou les personnes présentant NVDA à un public voyant, une fenêtre flottante est disponible, affichant tout ce que dit NVDA.

Pour activer la visionneuse de parole, cochez l'élément de menu "Visionneuse de parole" situé dans "Outils" dans le menu NVDA.
Décochez l'élément de menu pour la désactiver.

La fenêtre de la visionneuse de parole contient une case à cocher nommée "Montrer la visionneuse de parole au démarrage".
Si elle est cochée, la visionneuse de parole s'ouvrira au démarrage de NVDA.
La fenêtre de la visionneuse de parole essaiera toujours de s'ouvrir à la même dimension et à la même position que lors de sa fermeture.

Pendant que la visionneuse de parole est active, elle se met constamment à jour, vous permettant de voir les dernières paroles prononcées par NVDA.
Cependant, si vous déplacez la souris ou mettez le focus sur la visionneuse, NVDA arrêtera momentanément de mettre à jour le texte, vous pourrez ainsi sélectionner ou copier le contenu.

Pour activer la visionneuse de parole de n'importe où, Veuillez assigner un geste personnalisé en utilisant le [dialogue Gestes de Commandes](#InputGestures).

### Visionneuse Braille {#BrailleViewer}

Pour les voyants développeurs de logiciel ou les personnes présentant NVDA à un public voyant, une fenêtre flottante permettant de voir la sortie braille ainsi que le texte correspondant à chaque caractère braille est disponible.
La visionneuse Braille peut être utilisée en même temps qu'un afficheur braille physique, elle s'adaptera au nombre de cellules sur l'afficheur physique.
Quand la visionneuse Braille est activée, elle se met à jour constamment pour vous montrer ce qui serait affiché sur un afficheur braille physique.

Pour activer la visionneuse Braille, cochez l'élément de menu "Visionneuse Braille" dans Outils dans le menu de NVDA.
Décochez l'élément de menu pour la désactiver.

Les afficheurs braille physiques ont généralement des boutons pour faire défiler le texte en avant ou en arrière, pour permettre le défilement avec la visionneuse Braille utilisez le [dialogues de Gestes de Commandes](#InputGestures) pour assigner des raccourcis clavier pour "faire défiler l'afficheur braille en arrière" et "faire défiler l'afficheur braille en avant"

La fenêtre de la visionneuse Braille contient une case à cocher étiquetée "Montrer la visionneuse Braille au démarrage".
Si elle est cochée, la visionneuse Braille s'affichera au démarrage de NVDA.
La visionneuse Braille essaiera toujours de se rouvrir avec les mêmes dimensions et à la même position que lors de sa fermeture.

La fenêtre de la visionneuse braille contient une case à cocher étiquetée "Survol pour le routage vers une cellule", non cochée par défaut.
Si elle est cochée, le survol d'une cellule braille par la souris permettra d'activer la commande "aller à la cellule braille" pour cette cellule.
Ceci est parfois utilisé pour déplacer le curseur ou activer l'action pour un contrôle.
Ceci peut être utile pour tester si NVDA est capable de retrouver correctement une position à l'écran depuis une cellule braille.
Pour empêcher des routages cellules non intentionnels, la commande s'exécute après un délai.
La souris doit survoler jusqu'à ce que la cellule devienne verte.
La cellule commencera avec une couleur jaune clair, virera à l'orange, puis deviendra brusquement verte.

Pour activer/désactiver la visionneuse braille de n'importe où, Veuillez assigner un geste de commande personnalisé en utilisant le [dialogue Gestes de commandes](#InputGestures).

### Console Python {#PythonConsole}

La console Python de NVDA, disponible sous Outils dans le menu NVDA, est un outil de développement utile pour le débogage, l'inspection générale des internes de NVDA ou l'inspection de la hiérarchie d'accessibilité d'une application.
Pour plus d'informations, veuillez consulter le [Guide de développement NVDA](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Add-on Store {#AddonStoreMenuItem}

Cela ouvrira l'[Add-on Store de NVDA](#AddonsManager).
Pour plus d'informations, lisez la section détaillée : [Extensions et Add-on Store](#AddonsManager).

### Créer une copie portable {#CreatePortableCopy}

Ceci ouvrira un dialogue vous permettant de créer une copie portable de NVDA à partir de la version installée.
Au contraire, lors de l'exécution d'une copie portable de NVDA, dans le sous-menu Outils l'élément s'intitulera "installer NVDA sur ce PC" au lieu de "créer une copie portable".

Le dialogue de création d'une copie portable ou d'installation de NVDA sur ce PC vous demandera de choisir un dossier où créer la copie portable ou installer NVDA.

Dans ce dialogue vous pourrez activer ou désactiver ce qui suit :

* Copier la configuration utilisateur actuelle (Ceci inclut les fichiers contenus dans %appdata%\roaming\NVDA ou dans la configuration utilisateur de votre copie portable et inclut également les extensions ou autres modules)
* Démarrer la nouvelle copie portable après création ou démarrer NVDA après installation (démarre automatiquement NVDA après création de la copie portable ou après installation)

### Exécuter l'outil de correction d'enregistrements COM... {#RunCOMRegistrationFixingTool}

Installer et désinstaller des programmes sur un ordinateur peut, dans certains cas, causer le désenregistrement des fichiers DLL COM.
Comme les interfaces COM tels que IAccessible dépendent de l'enregistrement correct des DLL COM, des problèmes peuvent apparaître en cas d'absence d'enregistrement de celles-ci.

Cela peut survenir par exemple après installation et désinstallation d'Adobe Reader, Math Player et autres programmes.

Les enregistrements manquants peuvent causer des problèmes dans les navigateurs, les applications de bureau, barre des tâches et autres interfaces.

Spécifiquement, Les problèmes suivants peuvent être réglés par l'exécution de cet outil :

* NVDA annonce "inconnu" en navigation avec des navigateurs tels que Firefox, Thunderbird etc.
* NVDA échoue à basculer entre mode formulaire et mode navigation.
* NVDA est très lent dans les navigateurs en mode navigation.
* Et possiblement d'autres problèmes.

### Recharger les modules {#ReloadPlugins}

Cet élément, quand on l'active, recharge les modules applicatifs et globaux sans avoir à redémarrer NVDA, ce qui peut être utile pour les développeurs.
Les modules applicatifs (appModules) gèrent la manière dont NVDA interagit avec des applications spécifiques.
Les modules globaux (globalPlugins) gèrent la manière dont NVDA interagit avec toutes les applications.

Les raccourcis clavier NVDA suivants peuvent également être utiles :
<!-- KC:beginInclude -->

| Nom |Touche |Description|
|---|---|---|
|Recharger les modules |`NVDA+contrôle+f3` |Recharger les modules globaux et applicatifs|
|Annoncer le module applicatif chargé et l'exécutable |`NVDA+contrôle+f1` |Annoncer le nom du module applicatif, s'il y en a un, et le nom de l'exécutable associé à l'application qui a le focus clavier.|

<!-- KC:endInclude -->

## Synthétiseurs de Parole Pris en Charge {#SupportedSpeechSynths}

Cette section contient des informations concernant les synthétiseurs de parole pris en charge par NVDA.
Pour une liste encore plus importante de synthétiseurs gratuits ou du commerce que vous pouvez acheter et télécharger pour utilisation avec NVDA, veuillez consulter la [page des voix supplémentaires](https://github.com/nvaccess/nvda/wiki/ExtraVoices) (en anglais).

### eSpeak NG {#eSpeakNG}

Le synthétiseur [eSpeak nG](https://github.com/espeak-ng/espeak-ng) est intégré dans NVDA et ne dépend d'aucun pilote ou programme additionnel pour être installé.
Sous Windows 8.1, NVDA utilise eSpeak NG par défaut ([Windows OneCore](#OneCore) est utilisé sous Windows 10 et versions ultérieures par défaut).
Comme ce synthétiseur est intégré dans NVDA, il est le plus indiqué quand vous voulez exécuter NVDA depuis une clé USB sur un autre système.

Chaque voix fournie avec eSpeak NG correspond à une langue différente.
eSpeak NG prend en charge plus de 43 langues.

Vous disposez également d'un grand choix de variantes, permettant de modifier considérablement le son de la voix.

### Microsoft Speech API Version 4 (SAPI 4) {#SAPI4}

SAPI 4 est un ancien standard Microsoft pour les synthétiseurs de parole logiciels.
NVDA le supporte encore pour les utilisateurs qui ont déjà des synthétiseurs SAPI 4 installés.
Cependant, Microsoft ne le supporte plus et les composants nécessaires ne sont plus disponibles chez Microsoft.

Quand vous utilisez ce synthétiseur avec NVDA, la liste des voix disponibles (accessibles via la catégorie [Parole](#SpeechSettings)du dialogue [Paramètres](#NVDASettings), ou [la boucle des paramètres synthétiseur](#SynthSettingsRing)) contient toutes les voix de tous les synthétiseurs SAPI 4 installés sur votre système.

### Microsoft Speech API Version 5 (SAPI 5) {#SAPI5}

SAPI 5 est un standard Microsoft pour les synthétiseurs de parole logiciels.
Beaucoup de synthétiseurs de parole compatibles avec ce standard peuvent être achetés ou téléchargés gratuitement auprès de différentes sociétés ou sites web, mais il est probable que votre système possède déjà une voix SAPI 5 préinstallée.
Quand vous utilisez ce synthétiseur avec NVDA, la liste des voix disponibles (accessibles via la catégorie [Parole](#SpeechSettings)du dialogue [Paramètres](#NVDASettings), ou [la boucle des paramètres synthétiseur](#SynthSettingsRing)) contient toutes les voix de tous les synthétiseurs SAPI 5 installés sur votre système.

### La Plate-forme Microsoft Speech {#MicrosoftSpeechPlatform}

La plate-forme Microsoft Speech fournit des voix pour beaucoup de langues, normalement utilisées dans le développement de serveurs vocaux.
Ces voix peuvent également être utilisées avec NVDA.

Pour utiliser ces voix, vous devrez installer deux composants :

* [Microsoft Speech Platform - Runtime (Version 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (Version 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Cette page contient beaucoup de fichiers aussi bien pour la reconnaissance de parole que pour la synthèse vocale.
 Choisissez les fichiers contenant la synthèse vocale pour la langue désirée.
 Par exemple, le fichier MSSpeech_TTS_fr-FR_Hortense.msi est une voix francophone française.

### Voix Windows OneCore {#OneCore}

Windows 10 et les versions ultérieures incluent de nouvelles voix appelées "OneCore" ou voix "mobile".
Des voix sont fournies pour beaucoup de langues, et elles sont plus réactives que les voix Microsoft disponibles en utilisant Microsoft Speech API version 5.
Sous Windows 10 et versions ultérieures, NVDA utilise les voix Windows OneCore par défaut ([eSpeak NG](#eSpeakNG) est utilisé dans les autres versions).

Pour ajouter de nouvelles voix Windows OneCore, rendez-vous à  "Voix", dans les paramètres système de Windows.
Utilisez l'option "Ajouter des voix" et recherchez la langue désirée.
Beaucoup de langues incluent de multiples variantes.
"Royaume Uni" et "Australie" sont deux des variantes pour l'Anglais.
"France", "Canada" et "Suisse" sont des variantes disponibles pour le Français.
Recherchez la langue de base (telle que Anglais ou Français), puis trouvez la variante dans la liste.
Sélectionnez toutes les langues désirées et utilisez le bouton "Ajouter" pour les ajouter.
Une fois les langues ajoutées, redémarrez NVDA.

Veuillez consulter [Langues et voix prises en charge](https://support.microsoft.com/fr-fr/windows/annexe-a-langues-et-voix-prises-en-charge-4486e345-7730-53da-fcfe-55cc64300f01) pour une liste de voix disponibles.

## Terminaux Braille Pris en Charge {#SupportedBrailleDisplays}

Cette section contient des informations sur les terminaux braille pris en charge par NVDA.

### Terminaux supportant la détection automatique en arrière-plan {#AutomaticDetection}

NVDA a la possibilité de détecter beaucoup de terminaux braille automatiquement en arrière-plan, via USB ou Bluetooth.
Ce comportement est activé en sélectionnant l'option Automatique comme terminal braille préféré dans le [dialogue Paramètres Braille](#BrailleSettings).
Cette option est sélectionnée par défaut.

Les terminaux suivants supportent cette fonctionnalité de détection automatique.

* Terminaux Handy Tech
* Terminaux braille Baum/Humanware/APH/Orbit
* Séries HumanWare Brailliant BI/B
* HumanWare BrailleNote
* SuperBraille
* Séries Optelec ALVA 6
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Series
* Terminaux Eurobraille Esys/Esytime/Iris
* Afficheurs Nattiq nBraille
* Seika Notetaker: MiniSeika (16, 24 cellules), V6, et V6Pro (40 cellules)
* Afficheurs Tivomatic Caiku Albatross 46/80
* N'importe quel afficheur supportant le protocole standard HID Braille

### Les Terminaux Focus et PAC Mate de chez Freedom Scientific {#FreedomScientificFocus}

Tous les terminaux Focus et PAC Mate de chez [Freedom Scientific](https://www.freedomscientific.com/) sont pris en charge quand ils sont connectés en USB ou Bluetooth.
Vous devrez installer les pilotes de terminaux braille de Freedom Scientific sur votre système.
Si vous ne les avez pas déjà, vous pourrez les obtenir sur la [page du pilote d'affichage braille Focus Blue](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Bien que cette page ne mentionne que le terminal Focus 40 Blue, le pilote supporte tous les terminaux de Freedom Scientific.

Par défaut, NVDA peut automatiquement détecter et se connecter à ces afficheurs via USB ou Bluetooth.
Cependant, lorsque vous configurez l'afficheur, vous pouvez sélectionner explicitement "USB" ou "Bluetooth" pour restreindre le type de connexion qui sera utilisée.
Cela peut être utile si vous voulez connecter l'afficheur Focus à NVDA via le Bluetooth tout en le chargeant en utilisant l'USB.
La détection automatique de terminaux braille de NVDA reconnaîtra également cet afficheur en USB ou Bluetooth.

Voici les assignations de touches pour ces terminaux avec NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage braille |topRouting1 (première cellule de l'afficheur)|
|Défilement avant de l'affichage braille |topRouting20/40/80 (dernière cellule de l'afficheur)|
|Défilement arrière de l'affichage braille |barAvancerDeGauche|
|Défilement avant de l'affichage braille |barAvancerDeDroite|
|Basculer le suivi du braille |boutonGDFGauche+boutonGDFDroite|
|Choix de la fonction de la roulette magique gauche |Appui sur la roulette magique gauche|
|Retour arrière en utilisant la roulette magique gauche |roulette magique gauche vers le haut|
|Avancer en utilisant la roulette magique gauche |roulette magique gauche vers le bas|
|Choix de la fonction de la roulette magique droite |Appui sur la roulette magique droite|
|Retour arrière en utilisant la roulette magique droite |roulette magique droite vers le haut|
|Avancer en utilisant la roulette magique droite |roulette magique droite vers le bas|
|Aller à la cellule braille |routage|
|touche maj+tab |barreEspacebraille+point1+point2|
|touche tab |barreEspacebraille+point4+point5|
|touche flèche haut |barreEspacebraille+point1|
|touche flèche bas |barreEspacebraille+point4|
|touche contrôle+flèche gauche |barreEspacebraille+point2|
|touche contrôle+flèche droite |barreEspacebraille+point5|
|flèche gauche |barreEspacebraille+point3|
|flèche droite |barreEspacebraille+point6|
|touche origine |barreEspacebraille+point1+point3|
|touche fin |barreEspacebraille+point4+point6|
|touche contrôle+début |barreEspacebraille+point1+point2+point3|
|touche contrôle+fin |barreEspacebraille+point4+point5+point6|
|touche alt |barreEspacebraille+point1+point3+point4|
|touche alt+tab |barreEspacebraille+point2+point3+point4+point5|
|touche alt+maj+tab |BarreEspacebeBraille+point1+poin2+point5+point6|
|touche windows+tab |barreEspaceBraille+point2+point3+point4|
|touche échap |barreEspacebraille+point1+point5|
|touche Windows |barreEspacebraille+point2+point4+point5+point6|
|touche espace |barreEspacebraille|
|Bascule touche contrôle |barreEspaceBraille+point3+point8|
|Bascule touche alt |barreEspaceBraille+point6+point8|
|Bascule touche Windows |barreEspaceBraille+point4+point8|
|Bascule touche NVDA |barreEspaceBraille+point5+point8|
|Bascule touche majuscule |barreEspaceBraille+point7+point8|
|Bascule touches contrôle et majuscule |barreEspaceBraille+point3+point7+point8|
|Bascule touche alt et majuscule |barreEspaceBraille+point6+point7+point8|
|Bascule touches Windows et majuscule |barreEspaceBraille+point4+point7+point8|
|Bascule touches NVDA et majuscule |barreEspaceBraille+point5+point7+point8|
|Bascule touches contrôle et alt |barreEspaceBraille+point3+point6+point8|
|bascule contrôle, alt et majuscule keys |barreEspaceBraille+point3+point6+point7+point8|
|touche Windows+d (minimiser toutes les applications) |barreEspacebraille+point1+point2+point3+point4+point5+point6|
|Rapporter la ligne courante |barreEspacebraille+point1+point4|
|menu NVDA |barreEspacebraille+point1+point3+point4+point5|

Pour les nouveaux modèles de Focus qui ont des touches de bascule (focus 40, Focus 80 et Focus Blue) :

| Nom |Touche|
|---|---|
|Déplacer l'affichage braille vers la ligne précédente |barreBasculeGaucheeHaut, barreBasculeDroiteHaut|
|Déplacer l'affichage braille vers la ligne suivante |barreBasculeGaucheBas, barreBasculeDroiteBas|

Pour le Focus 80 seulement :

| Nom |Touche|
|---|---|
|Défiler le braille vers l'arrière |barreBumperHaut, barreBumperHaut|
|Défiler vers l'avant |barreBumperBas, barreBumperBas|

<!-- KC:endInclude -->

### Séries Optelec ALVA 6/Convertisseur de Protocole {#OptelecALVA}

Les terminaux BC640 et BC680 de chez [Optelec](https://www.optelec.com/) sont pris en charge quand ils sont connectés en USB ou Bluetooth.
Par ailleurs, vous pouvez connecter un terminal Optelec plus ancien, tel qu'un Braille Voyager, en utilisant un convertisseur de protocole fourni par Optelec.
Vous n'avez besoin d'aucun pilote particulier pour utiliser ces terminaux.
Il suffit de brancher le terminal et de configurer NVDA pour l'utiliser.

Note : NVDA pourrait être incapable d'utiliser un terminal ALVA BC6 via Bluetooth s'il est appairé en utilisant l'utilitaire ALVA Bluetooth.
Si vous avez appairé votre terminal en utilisant cet utilitaire et que NVDA est incapable de le détecter, nous vous recommandons d'appairer votre terminal ALVA de façon standard en utilisant les paramètres Bluetooth de Windows.

Note : Bien que certains de ces terminaux aient un clavier braille, ils prennent en charge la conversion braille vers texte par eux-mêmes par défaut.
Cela signifie que le système de saisie du braille de NVDA n'est pas utilisé dans la situation par défaut (le paramètre table de saisie braille n'a pas d'effet).
Pour les terminaux ALVA avec un microprogramme récent, il est possible de désactiver cette simulation de clavier HID en utilisant un geste de commande.

Voici les assignations de touches pour ces terminaux avec NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage braille |t1, etouch1|
|Amener l'affichage braille à la ligne précédente |t2|
|Aller au focus courant |t3|
|Amener l'affichage braille à la ligne suivante |t4|
|Défilement avant de l'affichage braille |t5, etouch3|
|Aller à la cellule braille |routage|
|Annoncer la mise en forme du texte sous la cellule braille |routage secondaire|
|Activer/désactiver la simulation de clavier HID |t1+spEnter|
|Aller à la première ligne en mode revue |t1+t2|
|Aller à la dernière ligne en mode revue |t4+t5|
|Bascule du suivi braille |t1+t3|
|Annonce du titre |etouch2|
|Annonce de la barre d'état |etouch4|
|Touche maj+tab |sp1|
|Touche alt |sp2, alt|
|Touche échap |sp3|
|Touche tab |sp4|
|Flèche haut |spUp|
|Flèche bas |spDown|
|Flèche gauche |spLeft|
|Flèche droite |spRight|
|Entrée |spEnter, enter|
|date et heure |sp2+sp3|
|Menu NVDA |sp1+sp3|
|Touche Windows+d (Minimiser toutes les applications) |sp1+sp4|
|Touche Windows+b (focus sur la zone de notification) |sp3+sp4|
|Touche Windows |sp1+sp2, windows|
|Touche alt+tab |sp2+sp4|
|Touche contrôle+début |t3+spUp|
|Touche contrôle+fin |t3+spDown|
|Touche début |t3+spLeft|
|Touche fin |t3+spRight|
|touche contrôle |contrôle|

<!-- KC:endInclude -->

### Les Terminaux Handy Tech {#HandyTech}

NVDA prend en charge la plupart des terminaux de chez [Handy Tech](https://www.handytech.de/) quand ils sont connectés en USB, par port série ou en Bluetooth.
Pour les terminaux USB les plus anciens, vous devrez installer le pilote USB Handy Tech sur votre système.

Les terminaux suivants ne sont pas nativement supportés, mais peuvent être utilisé via [le pilote universel Handy Tech](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) et l'extension NVDA :

* Braillino
* Bookworm
* Les afficheurs modulaires avec le microprogramme version 1.13 ou inférieure. Veuillez noter que le microprogramme de ces afficheurs peut être mis à jour.

Voici les assignations de touches pour ces terminaux avec NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage braille |left, up, b3|
|Défilement avant de l'affichage braille |right, down, b6|
|Amener l'affichage braille à la ligne précédente |b4|
|Amener l'affichage braille à la ligne suivante |b5|
|Aller à la cellule braille |routage|
|Touche maj+tab |esc, touche triple action gauche haut+bas|
|Touche alt |b2+b4+b5|
|Touche échap |b4+b6|
|Touche tab |enter, touche triple action droite haut+bas|
|Touche entrée |esc+enter, touche triple action gauche+droite haut+bas, JoystickAction|
|Flèche haut |joystick haut|
|Flèche bas |joystick bas|
|Flèche gauche |joystick gauche|
|Flèche droite |joystick droit|
|Menu NVDA |b2+b4+b5+b6|
|Bascule braille suit |b2|
|Bascule du curseur braille |b1|
|Bascule de présentation du contexte du focus |b7|
|Bascule de la saisie braille |space+b1+b3+b4 (space+capital B)|

<!-- KC:endInclude -->

### Le Terminal MDV Lilli {#MDVLilli}

Le terminal braille Lilli distribué par [MDV](https://www.mdvbologna.it/) est supporté.
Vous n'avez besoin d'aucun pilote particulier pour utiliser ce terminal.
Il suffit de brancher le terminal et de configurer NVDA pour l'utiliser.

Ce terminal ne supporte pas la détection automatique en arrière-plan.

Voici les assignations de touches pour ce terminal avec NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage braille |LF|
|Défilement avant de l'affichage braille |RG|
|Amener l'affichage braille à la ligne précédente |UP|
|Amener l'affichage braille à la ligne suivante |DN|
|Aller à la cellule braille |route|
|Touche maj+tab |SLF|
|Touche tab |SRG|
|Touche alt+tab |SDN|
|Touche alt+maj+tab |SUP|

<!-- KC:endInclude -->

### Les Terminaux Baum/Humanware/APH/Orbit {#Baum}

Plusieurs terminaux [Baum](https://www.baum.de/cms/en/), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) et [Orbit](https://www.orbitresearch.com/) sont pris en charge quand ils sont connectés via USB, Bluetooth ou série.
Les terminaux suivants sont pris en charge :

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Il est possible que d'autres terminaux fabriqués par Baum fonctionnent, mais cela n'a pas été testé.

Si vous connectez via USB des terminaux qui n'utilisent pas le mode HID, vous devrez d'abord installer les pilotes USB fournis par le constructeur.
Le VarioUltra et le Pronto! utilisent HID.
Le Refreshabraille et l'Orbit Reader 20 peuvent utiliser HID si configurés de manière appropriée.

Le mode USB série de l'Orbit Reader 20 n'est actuellement pris en charge que sous Windows 10 et versions ultérieures.
USB HID devrait en général être utilisé à la place.

Voici les assignations de touches pour ces terminaux avec NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière affichage braille |`d2`|
|Défilement avant affichage braille |`d5`|
|Amener l'affichage sur la ligne précédente |`d1`|
|Amener l'affichage sur la ligne suivante |`d3`|
|Aller à la cellule braille |`routage`|
|touche `Maj+tab` |`espace+point1+point3`|
|touche `tab` |`espace+point4+point6`|
|touche `alt` |`espace+point1+point3+point4` (`espace+m`)|
|touche `échap` |`espace+point1+point5` (`espace+e`)|
|touche `windows` |`espace+point3+point4`|
|touche `alt+tab` |`espace+point2+point3+point4+point5` (`espace+t`)|
|Menu NVDA |`espace+point1+point3+point4+point5` (`espace+n`)|
|touche `windows+d` (minimiser toutes les applications) |`espace+point1+point4+point5` (`espace+d`)|
|Dire tout |`espace+point1+point2+point3+point4+point5+point6`|

Pour les terminaux possédant un joystick:

| Nom |Touche|
|---|---|
|Flèche haut |haut|
|Flèche bas |bas|
|Flèche gauche |gauche|
|Flèche droite |droite|
|Touche entrée |select|

<!-- KC:endInclude -->

### Hedo ProfiLine USB {#HedoProfiLine}

Le terminal Hedo ProfiLine USB de [Hedo Reha-Technik](https://www.hedo.de/) est supporté.
Vous devrez tout d'abord installer le pilote USB fourni par le constructeur.

Ce terminal ne supporte pas encore la détection automatique en arrière-plan.

Voici les assignations de touches pour ce terminal sous NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage |K1|
|Défilement avant de l'affichage |K3|
|Ligne précédente |B2|
|Ligne suivante |B5|
|Aller à la cellule braille |routage|
|Bascule braille suit |K2|
|Dire tout |B6|

<!-- KC:endInclude -->

### Hedo MobilLine USB {#HedoMobilLine}

Le terminal Hedo MobilLine USB de [Hedo Reha-Technik](https://www.hedo.de/) est supporté.
Vous devrez tout d'abord installer le pilote USB fourni par le constructeur.

Ce terminal ne supporte pas encore la détection automatique en arrière-plan.

Voici les assignations de touches pour ce terminal sous NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage |K1|
|Défilement avant de l'affichage |K3|
|Ligne précédente |B2|
|Ligne suivante |B5|
|Aller à la cellule braille |routage|
|Bascule braille suit |K2|
|Dire tout |B6|

<!-- KC:endInclude -->

### HumanWare Séries Brailliant BI/B / BrailleNote Touch {#HumanWareBrailliant}

Les terminaux des séries Brailliant BI & B de [HumanWare](https://www.humanware.com/), incluant le BI 14, BI 32, BI 20X, BI 40, BI 40X et B 80 sont supportés quand ils sont connectés via USB ou Bluetooth.
S'ils sont connectés en USB avec le protocole réglé sur HumanWare, vous devez d'abord installer le pilote USB fourni par le constructeur.
Les pilotes USB ne sont pas nécessaires si le protocole est réglé sur OpenBraille.

Les terminaux suivants sont également supportés (et ne nécessitent aucun pilote spécial pour être installés):

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Voici les assignations de touches pour Brailliant BI/B et BrailleNote touch sous NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.

#### Assignations des Touches pour tous les Modèles {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage |gauche|
|Défilement avant de l'affichage |droite|
|Ligne précédente |haut|
|Ligne suivante |bas|
|Aller à la cellule braille |routage|
|Bascule d'attachement du braille |haut+bas|
|Touche flèche haut |espace+point1|
|Touche flèche bas |espace+point4|
|Touche flèche gauche |espace+point3|
|Touche flèche droite |espace+point6|
|Touche maj+tab |espace+point1+point3|
|Touche tab |espace+point4+point6|
|Touche alt |espace+point1+point3+point4 (espace+m)|
|Touche échap |espace+point1+point5 (espace+e)|
|Touche entrée |point8|
|Touche Windows |espace+point3+point4|
|Touche alt+tab |Espace+point2+point3+point4+point5 (espace+t)|
|Menu NVDA |c1+c3+c4+c5 (commande n)|
|Touche Windows+d (minimiser toutes les applications) |c1+c4+c5 (commande d)|
|Dire tout |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Assignations de Touches pour les Brailliant BI 32, BI 40 et B 80 {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Menu NVDA |c1+c3+c4+c5 (commande n)|
|Touche windows+d (minimiser toutes les applications) |c1+c4+c5 (commande d)|
|Dire tout |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Assignations de Touches pour le Brailliant BI 14 {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|touche flèche haut |joystick vers le haut|
|touche flèche bas |joystick vers le bas|
|touche flèche gauche |joystick vers la gauche|
|touche flèche droit |joystick vers la droite|
|touche entrée |joystick action|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Series {#Hims}

NVDA supporte les afficheurs braille Braille Sense, Braille EDGE, Smart Beetle et Sync Braille de [Hims](https://www.hims-inc.com/) quand ils sont connectés via USB ou Bluetooth.
Si vous connectez votre afficheur braille par USB, vous devrez installer les [pilotes USB de HIMS](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) sur votre système.

Voici les assignations de touches pour ce terminal sous NVDA.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Aller à la cellule braille |routage|
|Défilement arrière de l'affichage braille |défilementHautDeGauche, défilementHautDeDroite, défilementDeGauche|
|Défilement avant de l'affichage braille |défilementBasDeGauche, défilementBasDeDroite, défilementDeDroite|
|Amener l'affichage à la ligne précédente |défilementHautDeGauche+défilementHautDeDroite|
|Amener l'affichage à la ligne suivante |défilementBasDeGauche+défilementBasDeDroite|
|Aller à la ligne précédente en revue |flècheHautDeDroite|
|Aller à la ligne suivante en revue |flècheBasDeDroite|
|Aller au caractère précédent en revue |flècheGaucheDeDroite|
|Aller au caractère suivant en revue |flècheDroiteDeDroite|
|Aller au focus courant |défilementHautDeGauche+défilementBasDeGauche, défilementHautDeDroite+défilementBasDeDroite, défilementDeGauche+défilementDeDroite|
|Touche contrôle |smartbeetle:f1, brailleedge:f3|
|Touche Windows |f7, smartbeetle:f2|
|Touche alt |point1+point3+point4+espace, f2, smartbeetle:f3, brailleedge:f4|
|Touche majuscule |f5|
|Touche insertion |point2+point4+espace, f6|
|Touche applications |point1+point2+point3+point4+espace, f8|
|Verrouillage majuscule |point1+point3+point6+espace|
|touche tabulation |point4+point5+espace, f3, brailleedge:f2|
|maj+alt+tab |f2+f3+f1|
|alt+tab |f2+f3|
|maj+tab |point1+point2+espace|
|Touche fin |point4+point6+espace|
|contrôle+fin |point4+point5+point6+espace|
|Touche début |point1+point3+espace, smartbeetle:f4|
|contrôle+début |point1+point2+point3+espace|
|alt+f4 |point1+point3+point5+point6+espace|
|flèche gauche |point3+espace, flècheGaucheDeGauche|
|contrôle+maj+flècheGauche |point2+point8+espace+f1|
|contrôle+flècheGauche |point2+espace|
|maj+alt+flècheGauche |point2+point7+f1|
|`alt+flècheGauche` |`point2+point7+espace`|
|flècheDroite |point6+espace, flècheDroiteDeGauche|
|contrôle+maj+flècheDroite |point5+point8+espace+f1|
|contrôle+flècheDroite |point5+espace|
|maj+alt+flècheDroite |point5+point7+f1|
|`alt+flècheDroite` |`point5+point7+espace`|
|pagePrec |point1+point2+point6+espace|
|contrôle+pagePrec |point1+point2+point6+point8+espace|
|Touche flècheHaut |point1+espace, flècheHautDeGauche|
|contrôle+maj+flècheHaut |point2+point3+point8+espace+f1|
|contrôle+flècheHaut |point2+point3+espace|
|maj+alt+flècheHaut |point2+point3+point7+f1|
|`alt+flècheHaut` |`point2+point3+point7+espace`|
|maj+flècheHaut |DéfilementBasDeGauche+espace|
|pageSuiv |point3+point4+point5+espace|
|contrôle+pageSuiv |point3+point4+point5+point8+espace|
|Touche flècheBas |point4+espace, flècheBasDeGauche|
|contrôle+maj+flècheBas |point5+point6+point8+espace+f1|
|contrôle+flècheBas |point5+point6+espace|
|maj+alt+flècheBas |point5+point6+point7+f1|
|`alt+flècheBas` |`point5+point6+point7+espace`|
|maj+flècheBas |espace+défilementBasDeDroite|
|Touche échap |point1+point5+espace, f4, brailleedge:f1|
|touche effacement |point1+point3+point5+espace, point1+point4+point5+espace|
|touche f1 |point1+point2+point5+espace|
|touche f3 |point1+point4+point8+espace|
|touche f4 |point7+f3|
|windows+b |point1+point2+f1|
|windows+d |point1+point4+point5+f1|
|contrôle+insert |smartbeetle:f1+défilementDeDroite|
|alt+insert |smartbeetle:f3+défilementDeDroite|

<!-- KC:endInclude -->

### Seika Braille Displays {#Seika}

Les afficheurs braille Seika suivants de Nippon Telesoft sont pris en charge en deux groupes avec des fonctionnalités différentes :

* [Seika Version 3, 4, et 5 (40 cellules), Seika80 (80 cellules)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 cellules), V6, et V6Pro (40 cellules)](#SeikaNotetaker)

Vous pouvez trouver plus d'informations concernant ces afficheurs sur leur [Page de téléchargement de démos et de pilotes](https://en.seika-braille.com/down/index.html).

#### Seika Version 3, 4, et 5 (40 cellules), Seika80 (80 cellules) {#SeikaBrailleDisplays}

* Ces terminaux ne supporte pas encore la détection automatique en arrière-plan.
* Sélectionnez "Terminaux Braille Seika" pour configurer manuellement
* Un pilote doit être installé avant d'utiliser les Seika v3/4/5/80.
Les pilotes sont [fournis par le fabriquant](https://en.seika-braille.com/down/index.html).

Voici les assignations de touches pour le terminal Seika Braille :
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage braille |gauche|
|Défilement avant de l'affichage braille |droite|
|Déplacer l'afficheur braille à la ligne précédente |B3|
|Déplacer l'afficheur braille à la ligne suivante |b4|
|Basculer le suivi braille |b5|
|Dire tout |b6|
|tab |b1|
|maj+tab |b2|
|alt+tab |b1+b2|
|Menu NVDA |gauche+droite|
|Aller à la cellule braille |route (amener le curseur au caractère)|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 cellules), V6, et V6Pro (40 cellules) {#SeikaNotetaker}

* La détection automatique de l'afficheur braille en arrière-plan de NVDA est prise en charge via USB et Bluetooth.
* Sélectionnez "Seika Notetaker" ou "automatique" pour configurer.
* Aucun pilote supplémentaire n'est requis lors de l'utilisation d'un afficheur braille Seika Notetaker.

Voici les assignation de touches pour le Seika Notetaker.
Veuillez consulter la documentation du terminal pour savoir où se situent ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement braille vers la gauche |gauche|
|Défilement braille vers la droite |droite|
|Dire tout |espace+RetourArrière|
|Menu NVDA |Gauche+Droite|
|Amener l'afficheur braille à la ligne précédente |LJ haut|
|Amener l'afficheur braille à la ligne suivante |LJ bas|
|Basculer le suivi braille |LJ centre|
|tab |LJ droite|
|Maj+tab |LJ gauche|
|FlècheHaut |RJ haut|
|FlècheBas |RJ bas|
|FlècheGauche |RJ gauche|
|FlècheDroite |RJ droit|
|Aller à la cellule braille |routage|
|maj+flècheHaut |Espace+RJ haut, RetourArrière+RJ haut|
|Maj+flècheBas |Espace+RJ bas, RetourArrière+RJ bas|
|maj+flèchegauche |Espace+RJ gauche, RetourArrière+RJ gauche|
|maj+flècheDroite |Espace+RJ droit, RetourArrière+RJ droit|
|touche entrée |RJ centre, point8|
|touche échap |Espace+RJ centre|
|touche windows |RetourArrière+RJ centre|
|touche espace |Espace, RetourArrière|
|touche RetourArrière |point7|
|touche pagePrec |Espace+LJ droit|
|touche pageSuiv |Espace+LJ gauche|
|touche début |espace+LJ haut|
|touche fin |espace+LJ bas|
|touche contrôle+début |retourArrière+LJ haut|
|touche contrôle+fin |retourArrière+LJ bas|

### Nouveaux Modèles de Papenmeier brailleX {#Papenmeier}

Les afficheurs braille suivant sont supportés :

* BrailleX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BrailleX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BrailleX Trio (USB et Bluetooth)
* BRAILLEX Live 20, BRAILLEX Live et BRAILLEX Live Plus (USB et Bluetooth)

Ces terminaux ne supporte pas la détection automatique en arrière-plan.
Il existe une option dans le pilote USB de l'afficheur qui peut entraîner un problème de chargement de l'afficheur.
Veuillez essayez ce qui suit:

1. Veuillez vous assurer que vous avez installé le [dernier pilote](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Ouvrez le Gestionnaire de périphériques Windows.
1. Faites défiler la liste jusqu'à "Contrôleurs USB" ou "Périphériques USB".
1. Sélectionnez "Périphérique USB Papenmeier Braillex".
1. Ouvrez les propriétés et passez à l'onglet "Avancé".
Parfois, l'onglet "Avancé" n'apparaît pas.
Si tel est le cas, déconnectez la plage braille de l'ordinateur, quittez NVDA, attendez un moment et reconnectez la plage braille.
Répétez cette opération 4 à 5 fois si nécessaire.
Si l'onglet "Avancé" ne s'affiche toujours pas, veuillez redémarrer l'ordinateur.
1. Désactivez l'option "Load VCP".

La plupart des afficheurs ont une barre d'accès facile (EAB) qui permet des opérations intuitives et rapides.
L'EAB peut être bougé dans quatre directions et chaque direction a deux crans.
Les séries C et Live sont les seules exceptions à cette règle.

La série-C et quelques autres afficheurs ont deux rangées de routines où celle du haut sert à rapporter les informations de mise en forme.
Garder enfoncée une des routines du haut puis appuyer sur l'EAB sur une Série-C annule le second cran.
Les terminaux des séries Live n'ont qu'une ligne de routines et l'EAB n'a qu'un cran par direction.
Le second cran peut être reproduit en pressant une des touches de routage et en pressant l'EAB dans la direction correspondante.
Appuyer et garder les touches haute, basse, gauche et droite (ou EAB) répète la dernière commande.

Généralement, les touches suivantes sont disponibles sur ces afficheurs braille :

| Nom |touche|
|---|---|
|l1 |touche gauche devant|
|l2 |touche gauche derrière|
|r1 |touche droite devant|
|r2 |touche droite derrière|
|haut |Monter une fois vers le haut|
|haut2 |Monter deux fois vers le haut|
|gauche |un vers la gauche|
|gauche2 |deux vers la gauche|
|droite |un vers la droite|
|droite2 |deux vers la droite|
|dn |un vers le bas|
|dn2 |deux vers le bas|

Voici les commandes assignées pour les afficheurs Papenmeier dans NVDA :
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'affichage braille |left|
|Défilement avant de l'affichage braille |right|
|Déplacer l'afficheur braille à la ligne précédente |up|
|Déplacer le braille à la ligne suivante |dn|
|Aller à la cellule braille |routage|
|Lire le caractère sous le curseur de revue |l1|
|Activer l'objet courant du navigateur |l2|
|Bascule braille suit |r2|
|Lire le titre |l1+up|
|Lire la barre d'état |l2+down|
|Aller à l'objet parent |up2|
|Aller à l'objet enfant |dn2|
|Aller à l'objet précédent |left2|
|Aller à l'objet suivant |right2|
|Annoncer l'information de mise en forme du texte sous la cellule braille |rangée de routines du haut|

<!-- KC:endInclude -->

Le modèle Trio à quatre touches additionnelles en face du clavier braille.
Elles sont (ordonnées de gauche à droite) :

* Touche thumb gauche (lt)
* Espace
* Espace
* Touche thumb droite (rt)

Pour le moment, rt n'est pas utilisée.
Les touches intérieures font toutes les deux espace.

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|touche échap |espace avec point 7|
|touche flèche haute |espace avec point 2|
|touche flèche gauche |espace avec point 1|
|touche flèche droite |espace avec point 4|
|touche flèche basse |espace avec point 5|
|touche contrôle |lt+point 2|
|touche alt |lt+point 3|
|touches contrôle+échap |espace avec les points 1 2 3 4 5 6|
|touche tab |espace avec points 3 7|

<!-- KC:endInclude -->

### Papenmeier Braille BrailleX Modèles Anciens {#PapenmeierOld}

Les afficheurs braille suivants sont supportés :

* BrailleX EL 80, EL 2D-80, EL 40 P
* BrailleX Tiny, 2D Screen

Notez que ces afficheurs ne peuvent être connectés qu'en port série.
De ce fait, ils ne supportent pas la détection automatique en arrière-plan.
Vous devez donc sélectionner le port série où l'afficheur est connecté après avoir sélectionné le pilote dans le dialogue [Choisir l'Afficheur Braille](#SelectBrailleDisplay).

Certains de ces périphériques ont une barre d'accès facile (EAB) qui permet une opération rapide et intuitive.
L'EAB peut être bougée dans quatre directions où chaque direction a généralement deux crans.
Garder appuyée la touche haut, basse, gauche, droite (ou EAB) répète l'action correspondante.
Les anciens modèles n'ont pas d'EAB ; les touches de façade sont utilisées à la place.

Globalement, les touches suivantes sont disponibles sur les afficheurs braille :

| Nom |Touche|
|---|---|
|l1 |Touche avant gauche|
|l2 |Touche arrière droite|
|r1 |Touche avant droite|
|r2 |Touche arrière droite|
|up |1 appui vers le haut|
|up2 |2 appuis vers le haut|
|left |1 appui gauche|
|left2 |2 appuis gauche|
|right |1 appui à droite|
|right2 |2 appuis à droite|
|dn |1 appui en bas|
|dn2 |2 appuis en bas|

Les commandes Papenmeier disponibles dans NVDA sont les suivantes :

<!-- KC:beginInclude -->
Périphériques avec EAB :

| Nom |Touche|
|---|---|
|Défilement affichage braille arrière |left|
|Défilement affichage braille avant |right|
|Déplacer l'affichage braille vers la ligne précédente |up|
|Déplacer l'affichage braille vers la ligne suivante |down|
|Joindre à la cellule braille |routage|
|Annoncer le caractère courant sous la revue |l1|
|Activer l'objet courant du navigateur |l2|
|Dire titre |l1up|
|Lire barre d'état |l2down|
|Aller à l'objet contenant |up2|
|Aller au premier objet contenu |dn2|
|Aller à l'objet suivant |right2|
|Aller à l'objet précédant |left2|
|Annoncer l'information de mise en forme du texte sous la cellule braille |rangée de routines du haut|

BRAILLEX Tiny :

| Nom |Touche|
|---|---|
|Annoncer le caractère sous le curseur de revue |l1|
|Activer l'objet sous le navigateur |l2|
|Défiler le braille vers l'arrière |left|
|Défiler le braille vers l'avant |right|
|Déplacer le braille à la ligne précédente |up|
|Déplacer le braille à la ligne suivante |dn|
|Basculer le suivi du braille |r2|
|Aller à l'objet contenant |r1+up|
|Aller au premier objet contenu |r1+dn|
|Aller à l'objet précédent |r1+left|
|Aller à l'objet suivant |r1+right|
|Annoncer l'information de mise en forme du texte sous la cellule braille |rangée de routines du haut|
|Annoncer le titre |l1+up|
|Annoncer la barre d'état |l2+down|

brailleX 2D Screen:

| Nom |Touche|
|---|---|
|Annoncer le caractère sous le curseur de revue |l1|
|Activer l'objet sous le navigateur |l2|
|Basculer le suivi du braille |r2|
|Annoncer l'information de mise en forme du texte sous la cellule braille |rangée de routines du haut|
|Déplacer le braille à la ligne précédente |up|
|Défiler le braille vers l'arrière |left|
|Défiler le braille vers l'avant |right|
|Déplacer le braille à la ligne suivante |dn|
|Aller à l'objet suivant |left2|
|Aller à l'objet contenant |up2|
|Aller au premier objet contenu |dn2|
|Aller à l'objet précédent |right2|

<!-- KC:endInclude -->

### BrailleNote de HumanWare {#HumanWareBrailleNote}

NVDA supporte les bloc-notes BrailleNote de [HumanWare](https://www.humanware.com) lorsque ceux-ci agissent comme afficheurs braille pour un lecteur d'écran.
Les modèles suivants sont supportés :

* BrailleNote Classic (connexion série seulement)
* BrailleNote PK (connexion Série et Bluetooth)
* BrailleNote MPower (connexion Série et Bluetooth)
* BrailleNote Apex (connexion Bluetooth et USB)

Pour le BrailleNote Touch, Veuillez vous référer à la section [Séries Brailliant BI / BrailleNote Touch](#HumanWareBrailliant).

Excepté pour le BrailleNote PK, les claviers braille (BT) et QWERTY (QT) sont supportés.
Pour le BrailleNote QT, l'émulation de clavier PC n'est pas supportée.
Vous pouvez également entrer les points braille en utilisant le clavier QT.
Veuillez consulter la section terminal braille du manuel BrailleNote pour plus de détails.

Si votre périphérique supporte plusieurs types de connexion, en connectant votre BrailleNote à NVDA, vous devrez définir le port dans les options de votre afficheur braille.
Lisez le manuel de votre BrailleNote pour plus de détails.
Dans NVDA, vous devrez peut-être également configurer le port dans le dialogue [Choisir l'Afficheur Braille](#SelectBrailleDisplay).
Si vous le connectez via USB ou Bluetooth, vous pouvez le configurer sur "Automatique", "USB" ou "Bluetooth" selon ce qui est disponible.
Si vous le connectez à un port série ou un convertisseur USB-Série ou si aucune de ces dernières options n'apparaît, vous devez choisir explicitement le port de communication à utiliser dans la liste des ports matériels.

Avant de connecter votre BrailleNote Apex en utilisant son interface client USB, vous devez installer le pilote fourni par HumanWare.

Sur le BrailleNote Apex BT, vous pouvez utiliser la roue de défilement située entre les points 1 et 4 pour diverses commandes NVDA.
La roue consiste en 4 points directionnels, un bouton central de clic, et une roue qui peut tourner dans le sens des aiguilles d'une montre ou inversement.

Voici les assignations de touches du BrailleNote pour NVDA.
Consultez la documentation de votre BrailleNote pour savoir où se situent ces touches.

<!-- KC:beginInclude -->

| Nom |touche|
|---|---|
|Défilement affichage braille arrière |Arrière|
|Défilement affichage braille avant |Avant|
|Déplacer l'affichage braille vers la ligne précédente |Précédent|
|Déplacer l'affichage braille vers la ligne suivante |Suivant|
|Joindre à la cellule braille |routage|
|menu NVDA |espace+point1+point3+point4+point5 (espace+n)|
|Basculer le suivi de l'affichage braille |Précédent+Suivant|
|Touche Flèche haute |Espace+Point 1|
|Touche Flèche basse |Espace+Point 4|
|Touche Flèche gauche |Espace+Point 3|
|Touche Flèche droite |Espace+Point 6|
|Touche page précédente |Espace+Point 1+Point 3|
|Touche Page Suivante |Espace+Point4+Point6|
|Touche Origine |Espace+Point1+Point2|
|Touche fin |Espace+Point4+Point5|
|Contrôle+Origine |Espace+Point1+Point2+Point3|
|Touche Espace |Espace|
|Contrôle+Fin |Espace+Point4+Point5+Point6|
|Entrée |Espace+Point8|
|Touche retour arrière |Espace+Point7|
|Touche Tab |Espace+Point2+Point3+Point4+Point5 (Espace+t)|
|Maj+Tab |Espace+Point1+Point2+Point5+Point6|
|Touche Windows |Espace+Point2+Point4+Point5+Point6|
|Touche alt |Espace+Point1+Point3+Point4 (Espace+m)|
|Basculer aide à la saisie |Espace+Point2+Point3+Point6 (Espace+h en bas)|

Voici les commandes assignées au BrailleNote QT quand il n'est pas en mode saisie braille :

| Nom |Touche|
|---|---|
|menu NvDA |lecture+n|
|touche flèche haut |flècheHaut|
|touche flèche bas |flècheBas|
|touche flèche gauche |flècheGauche|
|touche flèche droite |flècheDroite|
|touche pagePrec |fonction+flècheHaut|
|touche pageSuiv |fonction+flècheBas|
|touche début |fonction+flècheGauche|
|touche fin |fonction+flècheDroite|
|touche contrôle+début |lecture+t|
|touche contrôle+fin |lecture+b|
|touche entrée |entrée|
|touche retour arrière |retourArrière|
|touche tab |tab|
|touche maj+tab keys |maj+tab|
|touche windows |lecture+w|
|touche alt |lecture+m|
|bascule de l'aide à la saisie |lecture+1|

Voici les commandes assignées à la roue de défilement :

| Nom |Touche|
|---|---|
|touche flècheHaut |flècheHaut|
|touche flècheBas |flècheBas|
|touche flècheGauche |flècheGauche|
|touche flècheDroite |flècheDroite|
|touche entrée |bouton central|
|touche tab |tourner la roue dans le sens des aiguilles d'une montre|
|touche maj+tab |tourner la roue dans le sens inverse des aiguilles d'une montre|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA supporte Les afficheurs EcoBraille de [ONCE](https://www.once.es/).
Les modèles suivants sont supportés :

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

Sous NVDA, vous pouvez définir le port série auquel l'afficheur est connecté dans le dialogue [Choisir l'Afficheur Braille](#SelectBrailleDisplay).
Ces terminaux ne supporte pas la détection automatique en arrière-plan.

Voici les assignations de touche pour les afficheurs EcoBraille.
Veuillez consulter [la documentation EcoBraille](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) pour connaître la position de ces touches.

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement braille arrière |T2|
|Défilement braille avant |T4|
|Amener l'afficheur braille à la ligne précédente |T1|
|Amener l'afficheur braille à la ligne suivante |T5|
|Aller à la cellule braille |Routage|
|Activer l'objet navigateur courant |T3|
|Passer au mode de revue suivant |F1|
|Aller à l'objet contenant |F2|
|Passer au mode de revue précédent |F3|
|Aller à l'objet précédent |F4|
|Annoncer l'objet courant |F5|
|Aller à l'objet suivant |F6|
|Aller à l'objet en focus |F7|
|Aller au premier objet inclus |F8|
|Amener le focus système ou le curseur à la position courante de revue |F9|
|Annoncer la position du curseur de revue |F0|
|Bascule du mode de suivi braille |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

L'afficheur SuperBraille, principalement disponible à Taiwan, peut être connecté en USB ou en série.
Comme le SuperBraille n'a ni clavier physique ni bouton de défilement, toutes les saisies doivent être effectuées depuis un clavier d'ordinateur standard.
Pour cette raison, et pour maintenir la compatibilité avec d'autres revues d'écran à Taiwan, deux raccourcis clavier pour le défilement de l'affichage ont été définis :
<!-- KC:beginInclude -->

| Nom |touche|
|---|---|
|Défilement braille arrière |pavnumMoins|
|Défilement braille avant |pavnumPlus|

<!-- KC:endInclude -->

### Afficheurs Eurobraille {#Eurobraille}

Les afficheurs b.book, b.note, Esys, Esytime et Iris d'Eurobraille sont supportés par NVDA.
Ces appareils disposent d'un clavier braille à 10 touches.
Veuillez consulter la documentation de l'afficheur pour une description de ces touches.
Des deux touches placées comme une barre d'espace, la touche gauche correspond à la touche retour arrière et la touche droite à la touche espace.

Ces appareils sont connectés via USB et disposent d'un clavier USB autonome.
Il est possible d'activer/désactiver ce clavier en basculant "simulation de clavier HID" à l'aide d'un geste de commande.
Les fonctions du clavier braille décrites directement ci-dessous sont lorsque la "simulation du clavier HID" est désactivée.

#### Fonctions du clavier Braille {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Effacer la dernière cellule ou le dernier caractère braille saisi |`retourArrière`|
|Traduire n'importe quelle entrée en braille et appuyer sur la touche Entrée |`RetourArrière+espace`|
|Basculer la touche `NVDA` |`point3+point5+espace`|
|touche `insert` |`point1+point3+point5+espace`, `point3+point4+point5+espace`|
|touche `supprimer` |`point3+point6+espace`|
|touche `début` |`point1+point2+point3+espace`|
|touche `fin` |`point4+point5+point6+espace`|
|Touche `flècheGauche` |`point2+espace`|
|Touche `flècheDroite` |`point5+espace`|
|Touche `flècheHaute` |`point1+espace`|
|Touche `flècheBas` |`point6+espace`|
|Touche `pagePrec` |`point1+point3+espace`|
|Touche `pageSuiv` |`point4+point6+espace`|
|touche `pavnum1` |`point1+point6+retourArrière`|
|touche `pavnum2` |`point1+point2+point6+retourArrière`|
|touche `pavnum3` |`point1+point4+point6+retourArrière`|
|touche `pavnum4` |`point1+point4+point5+point6+retourArrière`|
|touche `pavnum5` |`point1+point5+point6+retourArrière`|
|touche `pavnum6` |`point1+point2+point4+point6+retourArrière`|
|touche `pavnum7` |`point1+point2+point4+point5+point6+retourArrière`|
|touche `pavnum8` |`point1+point2+point5+point6+retourArrière`|
|touche `pavnum9` |`point2+point4+point6+retourArrière`|
|Touche `pavnumInser` |`point3+point4+point5+point6+retourArrière`|
|Touche `PavnumDécimal` |`point2+retourArrière`|
|touche `PavnumDiviser` |`point3+point4+retourArrière`|
|Touche `pavnumMultiplier` |`point3+point5+retourArrière`|
|Touche `pavnumMoins` |`point3+point6+retourArrière`|
|touche `PavnumPlus` |`point2+point3+point5+retourArrière`|
|Touche `pavnumEntrée` |`point3+point4+point5+retourArrière`|
|touche `échappement` |`point1+point2+point4+point5+espace`, `l2`|
|touche `tabulation` |`point2+point5+point6+espace`, `l3`|
|touches `maj+tab` |`point2+point3+point5+espace`|
|Touche `impressionÉcran` |`point1+point3+point4+point6+espace`|
|touche `pause` |`point1+point4+espace`|
|touche `applications` |`point5+point6+retourArrière`|
|touche `f1` |`point1+retourArrière`|
|touche `f2` |`point1+point2+retourArrière`|
|touche `f3` |`point1+point4+retourArrière`|
|touche `f4` |`point1+point4+point5+retourArrière`|
|touche `f5` |`point1+point5+retourArrière`|
|touche `f6` |`point1+point2+point4+retourArrière`|
|touche `f7` |`point1+point2+point4+point5+retourArrière`|
|touche `f8` |`point1+point2+point5+retourArrière`|
|touche `f9` |`point2+point4+retourArrière`|
|touche `f10` |`point2+point4+point5+retourArrière`|
|touche `f11` |`point1+point3+retourArrière`|
|touche `f12` |`point1+point2+point3+retourArrière`|
|touche `windows` |`point1+point2+point4+point5+point6+espace`|
|Basculer la touche `windows` |`point1+point2+point3+point4+retourArrière`, `point2+point4+point5+point6+espace`|
|touche `VerMaj` |`point7+retourArrière`, `point8+retourArrière`|
|Touche `VerNum` |`point3+retourArrière`, `point6+retourArrière`|
|touche `maj` |`point7+espace`|
|Basculer la touche `maj` |`point1+point7+espace`, `point4+point7+espace`|
|touche `contrôle` |`point7+point8+espace`|
|Basculer la touche `contrôle` |`point1+point7+point8+espace`, `point4+point7+point8+espace`|
|touche `alt` |`point8+espace`|
|Basculer la touche `alt` |`point1+point8+espace`, `point4+point8+espace`|
|Basculer la simulation du clavier HID |`switch1Gauche+joystick1Bas`, `switch1Droit+joystick1Bas`|

<!-- KC:endInclude -->

#### commandes clavier b.book {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Faire défiler l'affichage braille vers l'arrière |`en arrière`|
|Faire défiler l'affichage braille vers l'avant |`en avant`|
|Déplacer vers le focus actuel |`arrière+avant`|
|Route vers cellule braille |`routage`|
|Touche `flècheGauche` |`joystick2gauche`|
|Touche `flècheDroite` |`joystick2Right`|
|Touche `flècheHaut` |`joystick2Haut`|
|Touche `flècheBas` |`joystick2Bas`|
|touche `entrée` |`joystick2Centre`|
|touche `échappement` |`c1`|
|touche `tabulation` |`c2`|
|Basculer la touche `maj` |`c3`|
|Basculer la touche `contrôle` |`c4`|
|Basculer la touche `alt` |`c5`|
|Basculer la touche `NVDA` |`c6`|
|Touche `contrôle+Début` |`c1+c2+c3`|
|Touche `contrôle+Fin` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### commandes clavier b.note {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Faire défiler l'affichage braille vers l'arrière |`clavierGaucheGauche`|
|Faire défiler l'affichage braille vers l'avant |`clavierGaucheDroit`|
|Route vers cellule braille |`routage`|
|Signaler la mise en forme du texte sous la cellule braille |`doubleRouting`|
|Passer à la ligne suivante dans la révision |`clavierGaucheBas`|
|Passer au mode de révision précédent |`ClavierGaucheGauche+ClavierGaucheHaut`|
|Passer au mode de révision suivant |`clavierGaucheDroit+clavierGaucheBas`|
|Touche `flèchegauche` |`ClavierDroitGauche`|
|Touche `flèchedroite` |`clavierDroitDroite`|
|Touche `flècheHaut` |`clavierDroitHaut`|
|Touche `flècheBas` |`clavierDroitBas`|
|Touche `contrôle+Début` |`clavierDroitGauche+clavierDroitHaut`|
|Touche `contrôle+fin` |`clavierDroitGauche+clavierDroitHaut`|

<!-- KC:endInclude -->

#### Commandes clavier Esys {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Faire défiler l'affichage braille vers l'arrière |`switch1Gauche`|
|Faire défiler l'affichage braille vers l'avant |`switch1Droite`|
|Déplacer vers le focus actuel |`switch1Centre`|
|Route vers cellule braille |`routage`|
|Signaler la mise en forme du texte sous la cellule braille |`doubleRouting`|
|Aller à la ligne précédente en révision |`joystick1Haut`|
|Passer à la ligne suivante dans la révision |`joystick1bas`|
|Passer au caractère précédent en revue |`joystick1gauche`|
|Passer au caractère suivant en revue |`joystick1Droite`|
|Touche `flècheGauche` |`joystick2gauche`|
|Touche `flècheDroite` |`joystick2Droite`|
|Touche `flècheHaut` |`joystick2Haut`|
|Touche `glècheBas` |`joystick2Bas`|
|touche `entrée` |`joystick2Centre`|

<!-- KC:endInclude -->

#### Commandes clavier Esytime {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Faire défiler l'affichage braille vers l'arrière |`l1`|
|Faire défiler l'affichage braille vers l'avant |`l8`|
|Déplacer vers le focus actuel |`l1+l8`|
|Route vers cellule braille |`routage`|
|Signaler la mise en forme du texte sous la cellule braille |`doubleRouting`|
|Aller à la ligne précédente en révision |`joystick1Haut`|
|Passer à la ligne suivante dans la révision |`joystick1bas`|
|Passer au caractère précédent en revue |`joystick1gauche`|
|Passer au caractère suivant en revue |`joystick1Droite`|
|Touche `flèchegauche` |`joystick2gauche`|
|Touche `flèchedroite` |`joystick2Droite`|
|Touche `flècheHaut` |`joystick2Haut`|
|Touche `flècheBas` |`joystick2Bas`|
|touche `entrée` |`joystick2Centre`|
|touche `échappement` |`l2`|
|touche `tabulation` |`l3`|
|Basculer la touche `Maj` |`l4`|
|Basculer la touche `contrôle` |`l5`|
|Basculer la touche `alt` |`l6`|
|Basculer la touche `NVDA` |`l7`|
|Touche `contrôle+début` |`l1+l2+l3`, `l2+l3+l4`|
|Touche `contrôle+fin` |`l6+l7+l8`, `l5+l6+l7`|
|Basculer la simulation du clavier HID |`l1+joystick1Bas`, `l8+joystick1Bas`|

<!-- KC:endInclude -->

### Afficheurs Nattiq nBraille {#NattiqTechnologies}

NVDA supporte les afficheurs de [Nattiq Technologies](https://www.nattiq.com/) quand ils sont connectés via USB.
Windows 10 et les versions ultérieures détectent les afficheurs Braille à la connexion, il peut être nécessaire d'installer des pilotes USB si vous utilisez des versions plus anciennes de Windows (antérieures à Win10).
Vous pouvez les obtenir sur le site du fabriquant.

Voici les assignations de touches pour les afficheurs Nattiq Technologies sous NVDA.
Veuillez consulter la documentation de l'afficheur pour connaître la position de ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière |haut|
|Défilement avant |bas|
|Amener l'afficheur à la ligne précédente |gauche|
|amener l'afficheur à la ligne suivante |droit|
|Aller à la cellule braille |routage|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) est un programme séparé qui permet de prendre en charge beaucoup plus de terminaux braille.
Pour l'utiliser, il vous faut installer [BRLTTY pour Windows](https://www.brltty.app/download.html).
Vous devez télécharger et installer la version la plus récente avec installateur qui s'appellera, par exemple, brltty-win-4.2-2.exe.
Quand vous configurerez le terminal et le port à utiliser, portez une attention particulière aux instructions, en particulier si vous utilisez un terminal USB et que le pilote du constructeur est déjà installé.

Pour les afficheurs disposant d'un clavier braille, BRLTTY gèrent la saisie du braille.
L'option table d'entrée n'est donc pas applicable.

BRLTTY n'est pas concerné par la détection automatique en arrière-plan.

Voici les assignations de commandes BRLTTY pour NVDA.
Veuillez consulter les [listes des assignations des touches de BRLTTY](https://brltty.app/doc/KeyBindings/) pour des informations sur la manière dont BRLTTY lie ses commandes aux touches sur les terminaux braille.
<!-- KC:beginInclude -->

| Nom |commande BRLTTY|
|---|---|
|Défilement arrière de l'affichage braille |`fwinlt` (se déplacer à gauche d'une fenêtre)|
|Défilement avant de l'affichage braille |`fwinrt` (se déplacer à droite d'une fenêtre)|
|Amener l'affichage à la ligne précédente |`lnup` (monter d'une ligne)|
|Amener l'affichage à la ligne suivante |`lndn` (descendre d'une ligne)|
|Aller à la cellule braille |`route` (amener le curseur au caractère)|
|Basculer l'aide à la saisie |`learn` (entrer/sortir du mode d'apprentissage des commandes)|
|Ouvrir le menu NVDA |`prefmenu` (ouvrir/quitter le menu des préférences)|
|Rétablir la configuration |`prefload` (restaurer les préférences à partir du disque)|
|Enregistrer la configuration |`prefsave` (enregistrer les préférences sur le disque)|
|Afficher l'heure |`hour` (afficher la date et l'heure actuelles)|
|Prononcer la ligne où se trouve le curseur de révision |`say_line` (prononcer la ligne actuelle)|
|Dire tout en utilisant le curseur de revue |`say_below` (Lire depuis la ligne actuelle jusqu'au bas de l'écran)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Les terminaux Caiku Albatross, qui étaient fabriqués par Tivomatic et disponibles en Finlande, peuvent être connectés via USB ou série.
Vous n'avez pas besoin d'installer de pilote spécifique pour utiliser ces afficheurs.
Branchez simplement l'afficheur et configurez NVDA pour l'utiliser.

Remarque : Un débit de 19 200 bauds est fortement recommandé.
Si nécessaire, réglez la valeur du débit en bauds sur 19200 dans le menu de l'afficheur braille.
Bien que le pilote prenne en charge un débit en bauds de 9600, il n'a aucun moyen de contrôler le débit en bauds utilisé par l'affichage.
Parce que 19200 est le débit en bauds par défaut de l'affichage, le pilote l'essaie d'abord.
Si les débits en bauds ne sont pas les mêmes, le pilote peut se comporter de manière inattendue.

Voici les affectations de touches pour ces afficheurs avec NVDA.
Veuillez consulter la documentation de l'afficheur pour savoir où trouver ces touches.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Aller à la première ligne en mode revue |`home1`, `home2`|
|Aller à la dernière ligne en mode revue |`end1`, `end2`|
|Amener l'objet navigateur au focus courant |`eCursor1`, `eCursor2`|
|Aller au focus courant |`cursor1`, `cursor2`|
|Amener le pointeur souris à l'objet navigateur courant |`home1+home2`|
|Amener l'objet navigateur à l'objet sous le pointeur souris et l'annoncer |`end1+end2`|
|Amener le focus à l'objet navigateur courant |`eCursor1+eCursor2`|
|Basculer le suivi braille |`cursor1+cursor2`|
|Amener l'affichage braille à la ligne précédente |`up1`, `up2`, `up3`|
|Amener l'affichage braille à la ligne suivante |`down1`, `down2`, `down3`|
|Faire défiler l'affichage braille en arrière |`left`, `lWheelLeft`, `rWheelLeft`|
|Faire défiler l'affichage braille en avant |`right`, `lWheelRight`, `rWheelRight`|
|Aller à la cellule braille |`routing`|
|Annoncer la mise en forme du texte sous la cellule braille |`secondary routing`|
|Choisir la manière dont l'information contextuelle est présentée en braille |`attribute1+attribute3`|
|Faire défiler les modes de parole |`attribute2+attribute4`|
|Passer au mode de revue précédent (ex : objet, document ou écran) |`f1`|
|Passer au mode de revue suivant (ex : objet, document ou écran) |`f2`|
|Amener l'objet navigateur à l'objet le contenant |`f3`|
|Amener l'objet navigateur au premier objet qu'il contient |`f4`|
|Amener l'objet navigateur à l'objet précédent |`f5`|
|Amener l'objet navigateur à l'objet suivant |`f6`|
|Annoncer l'objet navigateur courant |`f7`|
|Annoncer l'information de position du texte ou de l'objet sous le curseur de revue |`f8`|
|Afficher les paramètres braille |`f1+home1`, `f9+home2`|
|Lire la barre d'état et y amener l'objet navigateur |`f1+end1`, `f9+end2`|
|Basculer le curseur braille |`f1+cursor1`, `f9+cursor2`|
|Faire défiler les formes de curseur braille |`f1+eCursor1`, `f9+eCursor2`|
|Faire défiler le mode d'affichage des messages en braille |`f1+f2`, `f9+f10`|
|Faire défiler le mode d'affichage de la sélection braille |`f1+f5`, `f9+f14`|
|Faire défiler les modes  pour l'option braille "Déplacer le curseur système lors du routage du curseur de revue" |`f1+f3`, `f9+f11`|
|Exécuter l'action par défaut sur l'objet navigateur courant |`f7+f8`|
|Annoncer date/heure |`f9`|
|Annoncer le niveau de batterie et le temps restant si l'alimentation n'est pas branchée |`f10`|
|Annoncer le titre |`f11`|
|Annoncer la barre d'état |`f12`|
|Annoncer la ligne courante sous le curseur d'application |`f13`|
|Dire tout |`f14`|
|Annoncer le caractère courant sous le curseur de revue |`f15`|
|Annoncer la ligne de l'objet navigateur courant où se situe le curseur de revue |`f16`|
|Dir le mot de l'objet navigateur courant où se situe le curseur de revue |`f15+f16`|
|Amener le curseur de revue à la ligne précédente de l'objet navigateur courant et l'annoncer |`lWheelUp`, `rWheelUp`|
|Amener le curseur de revue à la ligne suivante de l'objet navigateur courant et l'annoncer |`lWheelDown`, `rWheelDown`|
|Touche `Windows+d` (minimiser toutes les applications) |`attribute1`|
|Touche `Windows+e` (Ce PC) |`attribute2`|
|Touche `Windows+b` (focus dans la barre d'état) |`attribute3`|
|Touche `Windows+i` (Paramètres Windows) |`attribute4`|

<!-- KC:endInclude -->

### Afficheurs braille au standard HID {#HIDBraille}

Il s'agit d'un pilote expérimental pour la nouvelle spécification standard HID Braille, convenue en 2018 par Microsoft, Google, Apple et plusieurs sociétés de technologie d'assistance, dont NV Access.
L'espoir est que tous les futurs modèles d'afficheurs Braille créés par n'importe quel fabricant utiliseront ce protocole standard qui supprimera le besoin de pilotes Braille spécifiques au fabricant.

La détection automatique de l'affichage braille de NVDA reconnaîtra également tout affichage prenant en charge ce protocole.

Voici les affectations de touches actuelles pour ces affichages.
<!-- KC:beginInclude -->

| Nom |Touche|
|---|---|
|Défilement arrière de l'afficheur braille |panoramique à gauche ou rocker vers le haut|
|Défilement avant de l'afficheur braille |panoramique à droite ou rocker vers le bas|
|Aller à la cellule braille |ensemble de routage 1|
|Basculer braille suit to |haut+bas|
|touche flècheHaut |joystick vers le haut, dpad ver le haut ou espace+point1|
|touche flècheBas |joystick vers le bas, dpad ver le bas ou espace+point4|
|touche flècheGauche |espace+point3, joystick vers la gauche ou dpad ver la gauche|
|touche flècheDroite |espace+point6, joystick vers la droite ou dpad ver la droite|
|Touche maj+tab |espace+point1+point3|
|Touche tab |espace+point4+point6|
|Touche alt |espace+point1+point3+point4 (espace+m)|
|Touche échap |espace+point1+poin5 (espace+e)|
|touche entrée |poin8, joystick centre ou dpad centre|
|Touche Windows |espace+point3+point4|
|Touche alt+tab |espace+point2+point3+point4+point5 (espace+t)|
|Menu NVDA |espace+point1+point3+point4+point5 (espace+n)|
|Touche windows+d (minimiser toutes les applications) |espace+point1+point4+point5 (espace+d)|
|Dire tout |espace+point1+point2+point3+point4+point5+point6|

<!-- KC:endInclude -->

## Fonctions Avancées {#AdvancedTopics}
### Mode Sécurisé {#SecureMode}

Les administrateurs système peuvent souhaiter configurer NVDA pour restreindre les accès non autorisés au système.
NVDA permet l'installation d'extensions personnalisées, qui peuvent exécuter du code arbitraire, y compris lorsque NVDA est élevé aux privilèges d'administrateur.
NVDA permet également aux utilisateurs d'exécuter du code arbitraire via la console NVDA Python.
Le mode sécurisé de NVDA empêche les utilisateurs de modifier leur configuration NVDA et limite par ailleurs l'accès non autorisé au système.

NVDA s'exécute en mode sécurisé lorsqu'il est exécuté sur les [écrans sécurisés](#SecureScreens) à moins que le [paramètre à l'échelle du système](#SystemWideParameters) `serviceDebug` soit activé.
Pour forcer NVDA à toujours démarrer en mode sécurisé, définissez le [paramètre système](#SystemWideParameters) `forceSecureMode`.
NVDA peut également être démarré en mode sécurisé avec  [l'option de ligne de commande](#CommandLineOptions) `-s`.

Le mode sécurisé désactive :

* La sauvegarde de la configuration et autres paramètres sur disque
* La sauvegarde des gestes de commande sur disque
* Les fonctionnalités de [Profil de Configuration](#ConfigurationProfiles) telles que créer, supprimer, renommer les profils etc.
* Le chargement de la configuration depuis un dossiers personnalisés à l'aide de [l'option de ligne de commande `-c`](#CommandLineOptions)
* Mettre à jour NVDA et créer des copies portables
* [L'Add-on Store](#AddonsManager)
* La [console Python NVDA](#PythonConsole)
* La [Visionneuse du journal](#LogViewer) et la journalisation
* La [Visionneuse Braille](#BrailleViewer) et la [Visionneuse de parole](#SpeechViewer)
* L'ouverture de documents externes depuis le menu NVDA, comme le guide de l'utilisateur ou le fichier des contributeurs.

Les copies installées de NVDA stockent leur configuration, y compris les extensions, dans `%APPDATA%\nvda`.
Pour empêcher les utilisateurs de NVDA de modifier directement leur configuration ou leurs extensions, l'accès des utilisateurs à ce dossier doit également être restreint.

Le mode sécurisé est inefficace pour les copies portables de NVDA.
Cette limitation s'applique également à la copie temporaire de NVDA qui s'exécute au lancement de l'installateur.
Dans un environnements sécurisés, le fait qu'un utilisateur puisse exécuter un exécutable portable présente le même risque de sécurité, quele mode sécurisé soit forcé ou non.
Il est attendu que les administrateurs système empêchent l'exécution de logiciels non autorisés sur leurs systèmes, y compris les copies portables de NVDA.

Les utilisateurs de NVDA comptent souvent sur la configuration de leur profil NVDA pour répondre à leurs besoins.
Cela peut inclure l'installation et la configuration d'extensions personnalisées, qui doivent être approuvés indépendamment de NVDA.
Le mode sécurisé gèle les modifications apportées à la configuration de NVDA, veuillez donc vous assurer que NVDA est correctement configuré avant de forcer le mode sécurisé.

### Écrans Sécurisés {#SecureScreens}

NVDA s'exécute en [mode sécurisé](#SecureMode) lorsqu'il est exécuté sur les écrans sécurisés à moins que le [paramètre à l'échelle du système](#SystemWideParameters) `serviceDebug` soit activé.

Lorsqu'il s'exécute sur un écran sécurisé, NVDA utilise un profil système pour les préférences.
Les préférences utilisateur de NVDA peuvent être copiées [pour une utilisation dans les écrans sécurisés](#GeneralSettingsCopySettings).

Les écrans sécurisés incluent :

* L'écran de connexion à Windows
* Le dialogue Contrôle d'accès utilisateur, actif lors de l'exécution d'une action en tant qu'administrateur
  * Cela inclut l'installation de programmes

### Options de Ligne de Commande {#CommandLineOptions}

Au démarrage, NVDA peut accepter une ou plusieurs options additionnelles pour modifier son comportement.
Vous pouvez passer autant d'options que nécessaire.
Ces options peuvent être passées quand on démarre depuis un raccourci (dans les propriétés du raccourci), depuis le dialogue Exécuter (Menu Démarrer -> Exécuter ou Windows+r) ou depuis une console de commande Windows.
Les options doivent être séparées du nom de l'exécutable NVDA et des autres options par des espaces.
Par exemple, une option utile est `--disable-addons`, qui dit à NVDA d'interrompre toutes les extensions en cours d'exécution.
Cela vous permet de déterminer si un problème est causé par une extension et de vous sortir de sérieux problèmes pouvant être causés par des extensions.

Par exemple, vous pouvez quitter la copie en cours de NVDA en entrant ce qui suit dans le dialogue Exécuter :

    nvda -q

Certaines options de ligne de commande ont une version courte et une version longue, tandis que d'autres n'ont qu'une version longue.
Pour celles qui ont une version courte, vous pouvez les combiner ainsi :

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |Ceci démarrera NVDA avec le son et le message de démarrage  désactivé, et la configuration spécifiée.|
|`nvda -mc CONFIGPATH --disable-addons` |Même chose, mais avec les extensions désactivées|

Certaines options de ligne de commande acceptent des paramètres additionnels ; ex : le niveau de détail du journal ou le chemin du répertoire de configuration utilisateur.
Ces paramètres doivent être placés après l'option, séparés de l'option par un espace quand il s'agit d'une option en version courte ou par un signe égal (`=`) quand il s'agit d'une option en version longue; ex :

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Dit à NVDA de démarrer avec le niveau de journalisation sur débogage|
|`nvda --log-file=c:\nvda.log` |Dit à NVDA d'écrire le fichier journal dans `c:\nvda.log`|
|`nvda --log-level=20 -f c:\nvda.log` |Dit à NVDA de démarrer avec le niveau de journalisation sur info et d'écrire son journal dans `c:\nvda.log`|

Voici les options de ligne de commande de NVDA :

| Courte |Longue |Description|
|---|---|---|
|`-h` |`--help` |affiche l'aide de la ligne de commande et s'arrête|
|`-q` |`--quit` |Quitte la copie en cours d'exécution de NVDA|
|`-k` |`--check-running` |Indique si NVDA est en cours d'exécution via le code retour; 0 si oui, 1 si non|
|`-f NOMDUFICHIERJOURNAL` |`--log-file=NOMDUFICHIERJOURNAL` |Le fichier où les messages du journal doivent être écrits. La journalisation est toujours désactivée si le mode sécurisé est activé.|
|`-l NIVEAUDEJOURNALISATION` |`--log-level=NIVEAUDEJOURNALISATION` |Le niveau minimal de messages journalisés (débogage 10, entrées/sorties 12, avertissements de débogage 15, info 20, désactivé 100). La journalisation est toujours désactivée si le mode sécurisé est activé.|
|`-c CHEMINDECONFIG` |`--config-path=CHEMINDECONFIG` |Le chemin vers lequel tous les paramètres de NVDA sont stockés. La valeur par défaut est forcée si le mode sécurisé est activé.|
|Aucun |`--lang=LANGUAGE` |Remplacer la langue NVDA configurée. Choisissez "Windows" pour la langue en cours par défaut, "en" pour Anglais, etc.|
|`-m` |`--minimal` |Pas de sons, pas d'interface, pas de message de démarrage etc.|
|`-s` |`--secure` |Démarre NVDA en [Mode Sécurisé](#SecureMode)|
|Aucune |`--disable-addons` |Les extensions n'auront pas d'effet|
|Aucune |`--no-logging` |Désactive complètement la journalisation durant l'utilisation de NVDA. Ce paramètre peut être ignoré si un niveau de journalisation (`--loglevel`, `-l`) est spécifié dans la ligne de commande ou si la journalisation de débogage est activée.|
|Aucune |`--debug-logging` |Active le niveau de journalisation débogage seulement pour cette session. Ce paramètre remplacera tout autre niveau de journalisation (`--loglevel`, `-l`) argument donné, incluant l'option pas de journalisation.|
|Aucune |`--no-sr-flag` |Ne change pas l'indicateur système global de revue d'écran|
|Aucune |`--install` |Installe NVDA (en démarrant la copie nouvellement installée)|
|Aucune |`--install-silent` |Installe NVDA silencieusement (sans démarrer la copie nouvellement installée)|
|Aucune |`--enable-start-on-logon=True|False` |Durant l'installation, active le [démarrage sur l'écran de connexion](#StartAtWindowsLogon) de NVDA|
|Aucune |`--copy-portable-config` |À l'installation, copie la configuration portable depuis le chemin indiqué (`--config-path`, `-c`) vers le compte utilisateur courant|
|Aucune |`--create-portable` |Crée une copie portable de NVDA (puis démarre la copie nouvellement créée). `--portable-path` doit être spécifié|
|Aucune |`--create-portable-silent` |Crée une copie portable de NVDA (sans démarrer la copie nouvellement créée). `--portable-path` doit être spécifié|
|Aucune |`--portable-path=PORTABLEPATH` |L'emplacement où la copie portable sera créée|

### Paramètres Système {#SystemWideParameters}

NVDA permet de définir certaines valeurs dans la base de registre du système ce qui modifie le comportement général de NVDA.
Ces valeurs sont stockées dans la base de registres sous l'une des clés suivantes :

* Systèmes 32-bits : `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* Systèmes 64-bits : `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

Les valeurs suivantes peuvent être définies dans ces clés de registre :

| Nom |Type |valeurs Possibles |Description|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (par défaut) pour désactiver, 1 pour activer |Si activé, stocke la configuration de l'utilisateur NVDA dans les données d'application locales au lieu des données d'application itinérantes|
|`serviceDebug` |DWORD |0 (par défaut) pour désactiver, 1 pour activer |S'il est activé, désactive [Secure Mode](#SecureMode) sur [secure screens](#SecureScreens). En raison de plusieurs implications majeures en matière de sécurité, l'utilisation de cette option est fortement déconseillée|
|`forceSecureMode` |DWORD |0 (par défaut) pour désactiver, 1 pour activer |Si activé, force [le mode sécurisé](#SecureMode) à être activé lors de l'exécution de NVDA.|

## Informations Complémentaires {#FurtherInformation}

Si vous avez besoin d'informations complémentaires ou d'aide concernant l'utilisation de NVDA, veuillez visiter le [site web de NVDA](NVDA_URL).
Sur ce site, vous pourrez trouver des informations complémentaires telles que des listes de discussion spécialisées et d'autres ressources communautaires pour vous aider à utiliser NVDA.
Ce site fournit également des informations concernant le développement de NVDA.
