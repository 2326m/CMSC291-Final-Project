import discord
from discord.ext import commands
import word2number

if __name__ == '__main__':

    client = commands.Bot(command_prefix="$")

    NUM_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))


    @client.event
    async def on_reaction_add(reaction, user):
        if user == client.user or reaction.message.embeds[0].title != "Available Roles:":
            # not a relevant reaction
            return

        # regenerate list of roles
        available_roles = reaction.message.guild.roles
        index = NUM_EMOJIS.index(reaction.emoji)
        try:
            await user.add_roles(available_roles[index])
            await reaction.message.channel.send("Hey, check out the roles on this guy @" + str(user.display_name))
        except:
            await reaction.message.channel.send("Sorry, " + str(user.display_name) + ", I can't let you have the role of "
                                                + str(available_roles[index].name))

    @client.command()
    async def poll(ctx):
        if ctx.message.content == "$poll help":
            await ctx.send('To create a poll, use this format: $poll "Question" "Option 1" "Option 2" . ' +
                           'Then let users vote by reacting!')
            return

        poll_content = [line for line in [line.strip() for line in ctx.message.content.split("\"")] if line]
        try:
            question = poll_content[1]
            options = poll_content[2:]
        except:
            await ctx.send('To create a poll, use this format: "Question" "Option 1" "Option 2" ....')
            return

        if len(options) > 10:
            await ctx.send("Sheeeesh, that's too many options! Keep it to 10 or less.")
            return

        option_text = ''
        for i in range(0, len(options)):
            option_text += NUM_EMOJIS[i+1] + '  ' + options[i] + '\n\n'

        embed = discord.Embed(title="Poll: " + question,
                              description=option_text,
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed)

        for i in range(0, len(options)):
            await msg.add_reaction(NUM_EMOJIS[i])


    @client.command()
    async def roles(ctx):
        if ctx.message.content == '$roles help':
            await ctx.send('Use $roles to list all roles in the server and allow users to add a role by reacting!')
            return

        available_roles = ctx.guild.roles
        if len(available_roles) > 10:
            await ctx.send("Sheeeesh, there are too many roles in this server! Keep it to 10 or less.")
            return

        text = ''
        for i in range(0, len(available_roles)):
            text += NUM_EMOJIS[i] + ' ' + str(available_roles[i].name) + '\n \n'

        embed = discord.Embed(title="Available Roles:",
                              description=text,
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed)

        for i in range(0, len(available_roles)):
            await msg.add_reaction(NUM_EMOJIS[i])




    with open('token.txt', 'r') as file:
        token = file.readline()

    client.run(token)

