# anilist-helper

A simple library to help you fetch data from AniList

## Description

Welcome to my first python project!
This library is aimed at people who might be interested in automatizing their anime library.

## Getting Started

### Dependencies

* Python(tested on the latest ver.)
* An AniList account
* An AniList developer app
* Javascript enabled during the set-up process (for sending the access token back to Python)

### Installing

* Clone this repo
```
git clone https://github.com/ProchyGaming/anilist-helper /path/to/desired/folder
```
* Install it using pip
```
pip install anilist-helper
```
* Install it using pip locally
```
cd /path/to/desired/folder
pip install .
```
* If you want to make modifications to the library install it in the edit mode:
```
cd /path/to/desired/folder
pip install -e .
```

### Using the library

* To import the library into your code use:
```
import anilisthelper
```
* When importing this library for the first time, you will be taken through the setup process

### Setting up the AniList developer app

* When the setup process starts, you will be automatically taken to required pages. This process is really simple.
* When asked for the Client ID, you will be taken to the account developer page.
* If not logged in, log in first.
* Then create a new client
* Choose whatever name you fancy, and for the redirect URL use http://localhost:8888/auth
* After you save the client, copy the ID and paste it into the terminal
* After entering the ID you will be taken to an auth page, where you need to allow the app to access your account.
* Afterwards you will be taken to a redirect page that is momentarily hosted using gevent. (If you have any worries, please see the token_getter.html source code.)
* After that the library is successfully set-up and ready for use.

## Help

If you encounter any issues, feel free to open a new issue. If you have any new ideas or fixes, please open a pull request, they are more than welcome!

## Version History
* [1.05](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.05)
    * [get_all_anime_for_user(): Allow list as status](https://github.com/ProchyGaming/anilist-helper/commit/ae0906ae17940de5511b044abe4de957ef28a2b9)
    * [anilist_helper(): Add support for external api key](https://github.com/ProchyGaming/anilist-helper/commit/95ed72aa2f43a385ae8a40ed27b7c42fbe3b1c5d)
    * [anilist_helper: add MAL_ID into collected data](https://github.com/ProchyGaming/anilist-helper/commit/3c05821fa6ccfb3411ab3c4287ce47255da87fde)
    * [anilist_helper: Rewrite](https://github.com/ProchyGaming/anilist-helper/commit/d19059c2ef805d5d3cff318afd0bcc119608a8b6)
    * [anilist_helper: Add is_sus flag](https://github.com/ProchyGaming/anilist-helper/commit/5b6b2bfe14f09dbf3bb06d1a8f2dea80fa1e5f16)
* [1.042](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.042)
    * [gh-actions: Add action to cache build dependencies](https://github.com/ProchyGaming/anilist-helper/commit/7e02445ec6f5acf0ef7e5fad8634e77c9301164a)
    * [anilist_helper: Remove debug lines for cache](https://github.com/ProchyGaming/anilist-helper/commit/acc5b453d8324ef181c549df3bc550d5c46b0b26)
* [1.041](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.041)
    * [anilist_helper: Fix more oversights](https://github.com/ProchyGaming/anilist-helper/commit/b0ea061c16c5c147faf651593dd412b5bb92d2bb)
* [1.04](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.04)
    * [anilist_helper: Break down the setup process](https://github.com/ProchyGaming/anilist-helper/commit/8c3fe5900f4396186b3a7315bf38e73e236e784e)
    * [Remove LICENCE file when using pip show](https://github.com/ProchyGaming/anilist-helper/commit/9b42002dab525a1893c1f31b415c504c8e34c04b)
    * Didn't forget to update the README finally lul xd
* [1.03](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.03)
    * [anilist_helper: Fix Type and Key errors](https://github.com/ProchyGaming/anilist-helper/commit/c8cd7323beea27f653c9e888a1acb47b70ced8b0)
* [1.02](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.02)
    * [anilist_helper: Fix-up typos](https://github.com/ProchyGaming/anilist-helper/commit/af08dc7c2757156dc51c3e37374c623baf76c281)
    * [anilisthelper: Drop monkey patching](https://github.com/ProchyGaming/anilist-helper/commit/80fce02c35a6343f8ab19c896e41be0c11931974)
    * [anilisthelper: Cache at the info generational level](https://github.com/ProchyGaming/anilist-helper/commit/7076e876461238ca9c4ef7ecf12c0c2fa3da8ce4)
    * [generate_anime_entry(): Set placeholder day to 28th](https://github.com/ProchyGaming/anilist-helper/commit/b1b499e79fffe11b3f0007458e337f5ccbefa787)
    * [check_status_in_cache(): Force check data for releasing anime too](https://github.com/ProchyGaming/anilist-helper/commit/990900964995ff1fa30eb753dcdccbe0df5d7377)
    * [anilist_helper: Add support for env variable](https://github.com/ProchyGaming/anilist-helper/commit/ac64f38b8563f199776d931e621af290637f476f)
    * [anilist-helper: Add config_anilist() function](https://github.com/ProchyGaming/anilist-helper/commit/5d65e7ddee604379f70ab2e3291f3fe88607f8fc)
* [1.01](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.01)
    * [Import only datetime, not the whole library](https://github.com/ProchyGaming/anilist-helper/commit/7c7d5674644a50e891cf9f69bb71546b7fbcbf5b)
    * [Add a config_path variable](https://github.com/ProchyGaming/anilist-helper/commit/1d88e70891c785714bf355e3f526c59a7e9e21d1)
    * [get_anime_info(): Return proper dict](https://github.com/ProchyGaming/anilist-helper/commit/4b93547684030ffea06b53e234ab41cde352d446)
    * [get_anime_info(): Introduce a force update flag](https://github.com/ProchyGaming/anilist-helper/commit/348359239372b8a6d7e87034ec57c52b2b75d575)
    * [Introduce a check_status_in_cache() function](https://github.com/ProchyGaming/anilist-helper/commit/e6a1eb54298dc4a5838d45d8ed2d3bcb4effdf65)
* [1.0](https://github.com/ProchyGaming/anilist-helper/releases/tag/v1.0)
    * [Initial Release](https://github.com/ProchyGaming/anilist-helper/commit/5c838f646c66de83365f6a0e897d317e89d67e4f)

## Acknowledgments

Huge thanks to AniList team for their great page and database:
* [AniList](https://anilist.co/home)
* [AniList GraphQL](https://anilist.co/graphiql)
