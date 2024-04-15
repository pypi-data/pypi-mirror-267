# libreppc 

A simple profile page creator.

![example](resources/example.png "Profile example")

## Installation

```sh
$ pip install libreppc
$ python -m libreppc --serve
```

## Getting started

You need to create `config.json`:

**config.json** structure
```json
{
    "theme" : "CSS_FILE_NAME_WITHOUT_.css",
    "avatar" : "https://avatar-url.com",
    "username" : "yourusername",
    "description" : "yourdescription",
    "base_url" : "yourpageurl",
    "blog_dir" : "blog",
    "blog_title" : "Blog",
    "links" : [
        {
            "title" : "linktitle",
            "icon" : "iconurl",
            "url" : "linkurl"
        },
    ],
    "support" : [
        {
            "title" : "Monero/XMR",
            "type" : "text",
            "target" : "yourcryptoaddress"
        },
        {
            "title" : "Patreon",
            "type" : "url",
            "target" : "https://patreon.com/"
        },
    ],
    "projects" : [
        {
            "title" : "projectname",
            "description" : "projectdescription",
            "url" : "projecturl"
        }
    ]
}
```

Then you need to build site with:

```sh
$ python -m libreppc --build
```

## Contacts

| Contact                                               | Description       |
| :---:                                                 | :---              |
| [`Matrix`](https://matrix.to/#/#librehub:matrix.org)  | Matrix server     |

## Support

You can support us [here](https://warlock.codeberg.page).


