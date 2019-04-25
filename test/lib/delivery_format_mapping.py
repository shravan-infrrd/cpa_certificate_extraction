group_live = ['Group live', 'Group-live', 'Group-Live', 'Live Presentation', 'Conferences', 'Group Lve', 'Virtual group live', 'GroupLive', 'Group/Live', 'Live', 'Live seminar']

group_internet_based = [ 'Group Internet based', 'Group Internet-Based', 'Group-Intemet Based', 'Group - Internet-Based', 'Group Internet', 'Webcast', 'Group Intemet Based', 'Group - Internet Based', 'Internet Based', 'Group [nternet- Based', 'Group Program', 'Group Study', 'Internet-Based', 'Group ‘rternet basea', 'Group-Internet', 'Webinar', 'Group - Live', 'Virtual Instructor-Led', 'GroupInternet', 'Group intemet-based','Intermet', 'Group-Internel Based', 'Group-Interet Based', 'intemet', 'internel', 'Interet', 'Group-Infernel Based', 'Infernel', 'Groupod', 'Intemet-Bas', 'Internct-Based']

qas_self_study = [ 'Internet Based Self-Study Program.', 'Interactive Self Study','QAS Self study', 'Self-Study', 'Self Study', 'QAS Self Study.', 'self', 'QAS Study']

blendend_learning = ['Blended learning']

nano_learning = ['Nano learning']


def map_with_given_list(delivery_method):
    print(f"MAPP_DELIVERY_METHOD---->{delivery_method}")
    for gl in group_live:
        if gl.lower() in delivery_method.lower():
            return 'Group live'
    for qss in qas_self_study:
        if qss.lower() in delivery_method.lower():
            return 'QAS Self study'
    for gib in group_internet_based:
        if gib.lower() in delivery_method.lower():
            return 'Group Internet based'
    for bl in blendend_learning:
        if bl.lower() in delivery_method.lower():
            return 'Blended learning'
    for nl in nano_learning:
        if nl.lower() in delivery_method.lower():
            return 'Nano learning'
    return ""
