# coding : utf-8
import re
from utils.rtext import RTextList,RText,RAction,RColor

bot_list = []

worlds = ['§a主世界', '§d末地', '§4地狱']


def say_lines(server, msg):
    for line in msg.splitlines():
        server.say(line)


def joined_info(msg):
    joined_player = re.match(
        r'(\w+)\[([0-9\.:]+|local)\] logged in with entity id', msg)
    if joined_player:
        if joined_player.group(2) == 'local':
            return [True, 'bot', joined_player.group(1)]
        else:
            return [True, 'player', joined_player.group(1)]
    return [False]


def get_player_pos(server, player):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    return [
        PlayerInfoAPI.getPlayerInfo(server, player, 'Dimension'),
        PlayerInfoAPI.getPlayerInfo(server, player, 'Pos')
    ]


def list_bot(server):
    new_list = []
    for bot in bot_list:
        new_list.append([bot, get_player_pos(server, bot)])
    return new_list


def msg_list_bot(server):
    if not len(bot_list):
        return '§7服务器还没有假人'
    new_list = list_bot(server)
    msg=RTextList(RText("[假人列表]",color=RColor.gray))
    for bot in new_list:
            msg+=RTextList(
                RText('\n[x] ',color=RColor.red)
                    .h('下线该假人')
                    .c(RAction.run_command,'/player '+bot[0]+' kill'),
                RText(bot[0])
                    .h(RText(' [' + worlds[bot[1][0]] + '§r] \n(' + ','.join([str(int(i)) for i in bot[1][1]]) + ') '))
            )
    return msg


def on_info(server, info):
    if info.source == 0 and not info.is_player:
        botinfo = joined_info(info.content)
        if botinfo[0] and botinfo[1] == 'bot' and botinfo[2] not in bot_list:
            server.say('§7假人[' + botinfo[2] + ']加入了游戏')
            bot_list.append(botinfo[2])
    elif info.is_player:
        cmd = info.content.split()
        if len(cmd) == 1 and cmd[0] == '!!botlist':
            server.say(msg_list_bot(server))


def on_player_left(server, player):
    if player in bot_list:
        bot_list.remove(player)
        server.say('§7假人[' + player + ']离开了游戏')


def on_load(server, old_module):
    global bot_list
    if old_module:
        bot_list = old_module.bot_list

def on_server_startup(server):
    global bot_list
    bot_list=[]
