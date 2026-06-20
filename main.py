import os
import aiohttp
import discord
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

POKEAPI_BASE = "https://pokeapi.co/api/v2"

# Type effectiveness chart (simplified)
TYPE_EMOJI = {
    "normal": "⚪", "fire": "🔥", "water": "💧", "electric": "⚡", "grass": "🌿",
    "ice": "❄️", "fighting": "👊", "poison": "☠️", "ground": "⛰️", "flying": "🪽",
    "psychic": "🔮", "bug": "🐛", "rock": "🪨", "ghost": "👻", "dragon": "🐉",
    "dark": "🌑", "steel": "⚙️", "fairy": "🧚"
}

TYPE_COLORS = {
    "normal": 0xA8A8A8, "fire": 0xF08030, "water": 0x6890F0, "electric": 0xF8D030,
    "grass": 0x78C850, "ice": 0x98D8D8, "fighting": 0xC03028, "poison": 0xA040A0,
    "ground": 0xE0C068, "flying": 0xA890F0, "psychic": 0xF85888, "bug": 0xA8B820,
    "rock": 0xB8A038, "ghost": 0x705898, "dragon": 0x7038F8, "dark": 0x705848,
    "steel": 0xB8B8D0, "fairy": 0xEE99AC
}

@bot.event
async def on_ready():
    print(f'✓ {bot.user} is online — type !pokemon <name> to get started')

@bot.command(name='pokemon', aliases=['p'])
async def pokemon_lookup(ctx, *, name: str):
    """Look up a Pokemon by name or ID."""
    await ctx.trigger_typing()
    
    async with aiohttp.ClientSession() as session:
        try:
            # Fetch basic pokemon data
            async with session.get(f"{POKEAPI_BASE}/pokemon/{name.lower()}") as resp:
                if resp.status != 200:
                    return await ctx.send(f"❌ Pokemon `{name}` not found. Check spelling?")
                data = await resp.json()
            
            # Fetch species data for description
            species_url = data['species']['url']
            async with session.get(species_url) as resp:
                species_data = await resp.json()
                flavor_text = next(
                    (entry['flavor_text'] for entry in species_data['flavor_text_entries'] 
                     if entry['language']['name'] == 'en'),
                    "No description available."
                ).replace('\n', ' ').replace('\f', ' ')
            
            # Build embed
            types = [t['type']['name'] for t in data['types']]
            main_type = types[0]
            color = TYPE_COLORS.get(main_type, 0x000000)
            
            embed = discord.Embed(
                title=f"#{data['id']} {data['name'].capitalize()}",
                description=flavor_text[:300] + ("..." if len(flavor_text) > 300 else ""),
                color=color
            )
            
            # Thumbnail
            embed.set_thumbnail(url=data['sprites']['other']['official-artwork']['front_default'] or 
                              data['sprites']['front_default'])
            
            # Types
            type_str = " | ".join([f"{TYPE_EMOJI.get(t, '')} **{t.capitalize()}**" for t in types])
            embed.add_field(name="Type", value=type_str, inline=True)
            
            # Stats
            stats_str = "\n".join([
                f"{s['stat']['name'].replace('special-', 'Sp. ').replace('-', ' ').replace('hp', 'HP').title()}: **{s['base_stat']}**"
                for s in data['stats']
            ])
            embed.add_field(name="Base Stats", value=stats_str, inline=True)
            
            # Abilities
            abilities = [a['ability']['name'].replace('-', ' ').title() for a in data['abilities']]
            embed.add_field(name="Abilities", value=", ".join(abilities), inline=False)
            
            # Physical traits
            embed.add_field(name="Height / Weight", 
                          value=f"{data['height']/10} m / {data['weight']/10} kg", 
                          inline=False)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error fetching data: {str(e)}")

@bot.command(name='type')
async def type_info(ctx, type_name: str):
    """Get info about a Pokemon type."""
    type_name = type_name.lower()
    
    if type_name not in TYPE_EMOJI:
        return await ctx.send(f"❌ Invalid type: `{type_name}`. Use one of: {', '.join(TYPE_EMOJI.keys())}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEAPI_BASE}/type/{type_name}") as resp:
            if resp.status != 200:
                return await ctx.send(f"❌ Could not fetch type data.")
            data = await resp.json()
    
    # Damage relations
    relations = data['damage_relations']
    weak = [t.capitalize() for t in relations['double_damage_from']]
    resist = [t.capitalize() for t in relations['half_damage_from']]
    immune = [t.capitalize() for t in relations['no_damage_from']]
    
    # Pokemon of this type
    pokemon_count = len(data['pokemon'])
    
    embed = discord.Embed(
        title=f"{TYPE_EMOJI[type_name]} {type_name.capitalize()} Type",
        color=TYPE_COLORS.get(type_name, 0x000000)
    )
    
    if weak:
        embed.add_field(name="Weak Against ⚠️", value=", ".join(weak), inline=True)
    if resist:
        embed.add_field(name="Resistant 🛡️", value=", ".join(resist), inline=True)
    if immune:
        embed.add_field(name="Immune 🚫", value=", ".join(immune), inline=True)
    
    embed.add_field(name="Pokemon Count", value=str(pokemon_count), inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='compare', aliases=['c'])
async def compare_stats(ctx, pokemon1: str, pokemon2: str):
    """Compare base stats of two Pokemon."""
    await ctx.trigger_typing()
    
    async with aiohttp.ClientSession() as session:
        async def fetch_stats(name):
            async with session.get(f"{POKEAPI_BASE}/pokemon/{name.lower()}") as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return {
                    'name': data['name'].capitalize(),
                    'id': data['id'],
                    'stats': {s['stat']['name']: s['base_stat'] for s in data['stats']},
                    'sprite': data['sprites']['front_default']
                }
        
        p1, p2 = await fetch_stats(pokemon1), await fetch_stats(pokemon2)
        
        if not p1:
            return await ctx.send(f"❌ Pokemon `{pokemon1}` not found.")
        if not p2:
            return await ctx.send(f"❌ Pokemon `{pokemon2}` not found.")
    
    # Build comparison
    stat_names = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    stat_labels = ['HP', 'ATK', 'DEF', 'Sp.ATK', 'Sp.DEF', 'SPD']
    
    lines = []
    for i, (stat, label) in enumerate(zip(stat_names, stat_labels)):
        v1, v2 = p1['stats'][stat], p2['stats'][stat]
        diff = "=" if v1 == v2 else ("<" if v1 < v2 else ">")
        lines.append(f"**{label}**: {v1} {diff} {v2}")
    
    desc = "\n".join(lines)
    
    # Determine winner by total stats
    total1 = sum(p1['stats'].values())
    total2 = sum(p2['stats'].values())
    winner = p1['name'] if total1 > total2 else (p2['name'] if total2 > total1 else "Tie")
    
    embed = discord.Embed(
        title=f"⚔️ {p1['name']} vs {p2['name']}",
        description=desc,
        color=0xFFCB05
    )
    embed.add_field(name="Total BST", value=f"{total1} vs {total2}", inline=False)
    embed.add_field(name="Winner", value=winner, inline=False)
    embed.set_thumbnail(url=p1['sprite'])
    embed.set_footer(text=f"#{p1['id']} vs #{p2['id']}")
    
    await ctx.send(embed=embed)

@bot.command(name='ability', aliases=['a'])
async def ability_info(ctx, *, ability_name: str):
    """Look up a Pokemon ability."""
    await ctx.trigger_typing()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEAPI_BASE}/ability/{ability_name.lower().replace(' ', '-')}") as resp:
            if resp.status != 200:
                return await ctx.send(f"❌ Ability `{ability_name}` not found.")
            data = await resp.json()
    
    effect = next(
        (e['effect'] for e in data['effect_entries'] if e['language']['name'] == 'en'),
        "No effect description available."
    )
    
    pokemon_list = [p['pokemon']['name'].capitalize() for p in data['pokemon'][:10]]
    
    embed = discord.Embed(
        title=f"Ability: {data['name'].replace('-', ' ').title()}",
        description=effect,
        color=0x3B4CCA
    )
    embed.add_field(name="Pokemon with this ability", value=", ".join(pokemon_list) + "...", inline=False)
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Commands",
            description="""```
!pokemon <name/id>  — Look up a Pokemon
!type <type>         — Type info
!compare <p1> <p2>   — Stat comparison
!ability <name>      — Ability info
```""",
            color=0xFFCB05
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: `{error.param.name}`")

if __name__ == '__main__':
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables.")
        print("1. Create a bot at https://discord.com/developers/applications")
        print("2. Copy the token")
        print("3. Add it to your Secrets as DISCORD_BOT_TOKEN")
        exit(1)
    bot.run(token)