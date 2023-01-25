from DiscordCore import DiscordCore

def ReturnCall(member, guild):
    print(f'{member.name} has joined the server {guild.name}!')

discordCore = DiscordCore(on_member_join_method=ReturnCall)
discordCore.run("MTA0MTc4MzYzNzYzNDQ1MzUwNA.Gq4iQS._WzqYVB6JVGWhAzFp3deQ84jF8oulf-njXf8S8")