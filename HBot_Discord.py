import discord,requests,random,json,time,webbrowser
from discord.ext import commands

client = commands.Bot(command_prefix ='H.')

#List of 4chan boards, and dict to act as a cache for already looked up board catalogs
boards = ['a','c','w','m','cgl','cm','n','jp','vp','v','vg','vr','co','g','tv','k','o','an','tg','sp','asp','sci','int','out','toy','biz','i','po','p','ck','ic','wg','mu','fa','3','gd','diy','wsg','s','hc','h','e','u','d','y','t','hr','gif','trv','fit','x','lit','adv','lgbt','mlp','b','r','r9k','pol','soc','s4s']
cache  = {cache: '' for cache in boards}

#Returns [ random image URL, random image's thread URL ]
def r4chan(board):
    #Request board catalog, and get get a list of threads on the board; then sleeping for 1.5 seconds
    threadnums = list()
    data = ''

    #If a board's catalog has already been requested, just use that stored data instead
    if (cache[board] != ''):
        data = cache[board]
    #else request the catalog, and sleep for 1.5 seconds; storing that data for future use
    else:
        data = (requests.get('http://a.4cdn.org/' + board + '/catalog.json')).json()
        cache[board] = data
        time.sleep(1.5)

    #Get a list of threads in the data
    for page in data:
        for thread in page["threads"]:
            threadnums.append(thread['no'])

    #Select a thread
    thread = random.choice(threadnums)

    #Request the thread information, and get a list of images in that thread; again sleeping for 1.5 seconds
    imgs = list()
    pd = (requests.get('http://a.4cdn.org/' + board + '/thread/' + str(thread) + '.json')).json()
    for post in pd['posts']:
        #Ignore key missing error on posts with no image
        try:
            imgs.append(str(post['tim']) + str(post['ext']))
        except:
            pass
    time.sleep(1.5)

    #Select an image
    image = random.choice(imgs)

    #Assemble and return the urls
    imageurl = 'http://i.4cdn.org/' + board + '/' + image
    thread = 'http://boards.4chan.org/' + board + '/thread/' + str(thread)
    return [ imageurl , thread ]

#Opens x amount of image URLs in web browser; printing a link to the parent threads in console for reference
def ecchi():
    url = r4chan('e')
    return url[0]

def hentai():
    url = r4chan('h')
    return url[0]

def s():
    url = r4chan('s')
    return url[0]

def rndb():
    b = ['s','hc','h','e','u','d','y','t','hr','gif','aco','r']
    url = r4chan(random.choice(b))
    return url[0]


@client.event
async def on_ready():
    print('Bot is ready...')

@client.command()
async def e(ctx):
    await ctx.send('Ecchi !\n')
    await ctx.send(ecchi())

@client.command()
async def h(ctx):
    await ctx.send('Hentai !\n')
    await ctx.send(hentai())

@client.command()
async def secret(ctx):
    await ctx.send('OUPS\n')
    await ctx.send(s())

@client.command()
async def rnd(ctx):
    await ctx.send('Random\n')
    await ctx.send(rndb())

client.run('Njg5OTMxNDg1NjkxNzcyOTUw.XnKC3Q.zZrvVlCYJgamrMtQfRk6X2WjnRE')
