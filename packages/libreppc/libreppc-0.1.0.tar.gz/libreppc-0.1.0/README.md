# profiler 

A simple profile page creator. 

![example](resources/profiler-example.png "Profile example")

## Installation

```sh
$ git clone https://codeberg.org/librehub/profiler
$ cd profiler
$ python main.py --serve
```

## Getting started

You need to create `config.json`:

**config.json** structure
```json
{
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

```
$ python main.py --build
```

## Contacts

| Contact                                               | Description       |
| :---:                                                 | :---              |
| [`Matrix`](https://matrix.to/#/#librehub:matrix.org)  | Matrix server     |

## Donates
**Monero/XMR:** `47KkgEb3agJJjSpeW1LpVi1M8fsCfREhnBCb1yib5KQgCxwb6j47XBQAamueByrLUceRinJqveZ82UCbrGqrsY9oNuZ97xN`

