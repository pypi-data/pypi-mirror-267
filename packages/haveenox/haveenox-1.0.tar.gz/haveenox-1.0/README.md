### New:
> `clr()` - clear console
> `repeat(content, amount)` - repeat stuff
> - - - - - - - - - - - - - 
> `haveenox.dcPost(url, content)` - post stuff to discord webhooks
> `haveenox.parse_json(json_string)` - parse json to python dict
> `haveenox.create(filetype, mode, content)` - create a file with an optional mode (default = 'r') and optional add content (default=`None`) 

I was bored this was a 2m thing

Anyways, bunch of colors you can use for now:

```
RESET 
BLACK 
RED 
GREEN 
YELLOW 
BLUE 
MAGENTA 
CYAN  
WHITE 
LIGHTBLACK  
LIGHTRED 
LIGHTGREEN 
LIGHTYELLOW 
LIGHTBLUE 
LIGHTMAGENTA 
LIGHTCYAN 
LIGHTWHITE
```

Request more colors in a pull request and ill add them. 

### How to use the package:
> 1) On your shell or cmd, run the following below:
> ```git clone https://github.com/ExoticCitron/haveenox.git```

>  `Note:` You must have [Git](https://git-scm.com/downloads) installed for this to work

> 2) Import the package directly on your main file using the example below:
> ```py
> from haveenox import *
> ```

> 3) Use the color codes from above to change colors on console.
> ```py
> from haveenox import *
>
> print(f"{LIGHTMAGENTA} Test 1")
> print(CYAN + "Test 2" + RESET)
> ```

__**FAQ:**__
> There's none lol. Open an Issue for that. 

**Disclaimer:** You are currently downloading the dev build of this package, I'll make a public package soon on [PyPi](https://pypi.org/) 
