import discord
from discord.ext import commands
import json
import os
import random

os.chdir("C:\pyroject")
bot = discord.Client()

client = commands.Bot(command_prefix="py ")
hot="💵 "
@client.event
async def on_ready():
    print("Ready")
    
@client.command()
async def saldo(ctx):
    await open_account(ctx.author)
    
    user = ctx.author
    users = await get_banco_data()

    carteira_amt = users[str(user.id)]["carteira"]
    banco_amt = users[str(user.id)]["banco"]

    em = discord.Embed(title =f"💳 Pybank de {ctx.author.name}")
    em.add_field(name = "💰 Total da Carteira", value= hot+str(carteira_amt))
    em.add_field(name = "🏦 Total do Banco", value= hot+str(banco_amt))
    await ctx.send(embed= em)

@client.command(aliases=['daily', 'assalto'])
async def amém(ctx):
    await open_account(ctx.author)
    
    users = await get_banco_data()
    
    user = ctx.author

    earnings = random.randrange(0,101)
    
    await ctx.send(f" Aleeeeluia 🙏!!  {hot } {earnings} reais caiu do céu e foi direto para a sua continha!! 🤑")
    

    users[str(user.id)]["carteira"] += earnings

    with open("mainbanco.json", "w") as f:
        json.dump(users,f)
   
@client.command(aliases=['sacar', 'retirar'])
async def saque(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("essas é uma daquelas questões aritimeticas onde devo fazer um calculo para adivinhar o valor do saque ou você acabou se esquecendo?")
        return

    bal = await update_banco(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("uns tem Alzheimer outros possuem sonambulismo, não sei qual a sua situação, mas, com certeza essa não é a quantidade do seu saldo.")
        return

    if amount<0:
        await ctx.send("oi? para que tu quer um numero negativo?")
        return

    await update_banco(ctx.author, amount)
    await update_banco(ctx.author,-1* amount,"banco")

    await ctx.send(f"você tirou {amount} dinheiro da conta, ebbaa, de pouquinho em pouquinho vai tudo embora xD")


@client.command(aliases=['depositar', 'colocar', 'dep'])
async def deposito(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("a umm... eu irei adivinhar o valor que você quer depositar a ummm.. acabei me dando conta que não tenho poderes sobrenaturais..")
        return

    bal = await update_banco(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("onde é que tá toda essa quantia?")
        return

    if amount<0:
        await ctx.send("se não vai depositar é adicionar não diminuir ;p")
        return

    await update_banco(ctx.author,-1* amount)
    await update_banco(ctx.author, amount,"banco")

    await ctx.send(f"você colocou {amount} de dinheiro na conta, vai ficar rico u.u")

            
@client.command(aliases=['doar', 'esmola', 'investimento'])
async def enviar(ctx, member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    
    if amount == None:
        await ctx.send("faltou falar o valor que você quer enviar...")
        return

    bal = await update_banco(ctx.author)
    if amount =="all":
        amount =bal[0]

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("você não é o silvo santos não ;v")
        return

    if amount<0:
        await ctx.send("querendo doar numeros negativos, tem vergonha na cara.")
        return

    await update_banco(ctx.author,-1* amount, "banco")
    await update_banco(member, amount,"banco")

    await ctx.send(f"você doou {amount} de dinheiro")

@client.command(aliases=['robson'])
async def rob(ctx,member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_banco(member)

    if bal[0]<100:
        await ctx.send("não vale a pena")
        return
    
    earnings = random.randrange(0, bal[0])

    await update_banco(ctx.author,earnings)
    await update_banco(member,-1* earnings)

    await ctx.send(f"você rodou e ganhou {earnings} de dinheiro")

@client.command(aliases=['rodar', 'apostar', 'bet'])
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    
    if amount == None:
        await ctx.send("faltou o valor da aposta no final.")
        return

    bal = await update_banco(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Só nos seus sonhos que você possui isso tudo xD")
        return

    if amount<0:
        await ctx.send("não quero money negativo não")
        return

    final =[]
    for i in range(3):
        a=random.choice(["🍒","🍉","🔔"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_banco(ctx.author, 2*amount)
        await ctx.send("você ganhou {amount} 🎰!!")
    else:
        await update_banco(ctx.author, -1*amount)
        await ctx.send("você perdeu!!")



async def open_account(user):
    users = await get_banco_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]["carteira"] = 0
        users[str(user.id)]["banco"] = 0
    with open("mainbanco.json", "w") as f:
        json.dump(users,f)
    return True 

async def get_banco_data():
    with open("mainbanco.json", "r") as f:
        users = json.load(f)

    return users  

async def update_banco(user, change = 0, mode = "carteira"):
    users = await get_banco_data()

    users[str(user.id)][mode]+= change

    with open("mainbanco.json","w") as f:
        json.dump(users,f)
    bal=[users[str(user.id)]["carteira"],users[str(user.id)]["banco"]]
    return bal

client.run("***")


