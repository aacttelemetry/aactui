#Supposedly a series of if-else is the fastest way of figuring out whether a float is within many reanges.
#There are other more elegant and Pythonic ways, but this appears to be the fastest.

'''
x_min = [-86.6524,-86.6533,-86.653783,-86.653925,-86.654456,-86.654708,-86.655003,-86.655361,-86.654947,-86.655114,-86.655119,-86.655208,-86.655319,-86.654828,-86.653503,-86.653253,-86.653033,-86.652536]
x_max = [-86.652097,-86.652428,-86.653481,-86.653592,-86.654164,-86.654472,-86.654717,-86.655164,-86.654797,-86.654892,-86.654958,-86.655008,-86.655111,-86.654567,-86.653311,-86.653031,-86.652769,-86.652236]
y_min = [34.7105,34.710464,34.710344,34.710086,34.709961,34.709961,34.709961,34.710031,34.710225,34.710444,34.710303,34.710228,34.7105,34.710536,34.710619,34.710767,34.710844,34.710883]
y_max = [34.710861,34.710686,34.710581,34.710308,34.7101,34.7101,34.7101,34.710203,34.710436,34.710531,34.710442,34.7103,34.7106,34.710719,34.710747,34.710908,34.711017,34.711103]
regions = ['Start/Finish','Obstacle 1/Task 1','Obstacle 2','Obstacle 3','Obstacle 4','Obstacle 5/Task 2','Obstacle 6','Task 3','Obstacle 7','Obstacle 8','Obstacle 9','Task 4','Obstacle 10','Obstacle 11','Task 5','Obstacle 12','Obstacle 13','Obstacle 14']
names = ['Start/Finish Area','Undulating Terrain/Solid Soil Sample Retrieval','Serpentine Chicane','Crater with Ejecta','High Butte','Large Ravine/Spectrographic Analysis','Martian Sand Dunes','Instrument Deployment','Crevasses','Side Incline','Lunar Crater','Flag Plan and Photo','Bouldering Rocks (large rocks)','Tilted Craters','Liquid Sample Retrieval','Loose Regolith','Pea Gravel','Undulating Hills']
points = ['good luck!!','2/10 points maximum','3 points maximum','2 points maximum','6 points maximum','4/10 points maximum','5 points maximum','11 points maximum','3 points maximum','3 points maximum','4 points maximum','7 points maximum','4 points maximum','2 points maximum','10 points maximum','4 points maximum','4 points maximum','2 points maximum']
sections = ['ALL','14.x/14.1','14.x','14.2','14.3','14.4/14.5','14.6','14.7','14.8','14.9','14.10','14.11','14.12','14.x','14.13','14.14','14.15','14.16']
pages = ['ALL','19-20','21','21','22','23-25','26','27','27','28','29','30','30-31','31','32','33','34','35']
'''
#for i in range(0,len(regions)):
#	print('''elif %s <= x <= %s and %s <= y <= %s:
#			return (["%s","%s","%s","%s","%s"])'''%(x_min[i],x_max[i],y_min[i],y_max[i],regions[i],names[i],points[i],sections[i],pages[i]))


def determine_region(x,y):
    if x == "NO_ENCODE":
        return(["NO_ENCODE","Couldn't parse NMEA strings","Check for green light","ALL","ALL"])
    else:
        x = float(x)
        y = float(y)
    if -86.655442 <= x <= -86.651886 and 34.709939 <= y <= 34.711136:
        if -86.6524 <= x <= -86.652097 and 34.7105 <= y <= 34.710861:
            return (["Start/Finish","Start/Finish Area","good luck!!","ALL","ALL"])
        elif -86.6533 <= x <= -86.652428 and 34.710464 <= y <= 34.710686:
            return (["Obstacle 1/Task 1","Undulating Terrain/Solid Soil Sample Retrieval","2/10 points maximum","14.x/14.1","19-20"])
        elif -86.653783 <= x <= -86.653481 and 34.710344 <= y <= 34.710581:
            return (["Obstacle 2","Serpentine Chicane","3 points maximum","14.x","21"])
        elif -86.653925 <= x <= -86.653592 and 34.710086 <= y <= 34.710308:
            return (["Obstacle 3","Crater with Ejecta","2 points maximum","14.2","21"])
        elif -86.654456 <= x <= -86.654164 and 34.709961 <= y <= 34.7101:
            return (["Obstacle 4","High Butte","6 points maximum","14.3","22"])
        elif -86.654708 <= x <= -86.654472 and 34.709961 <= y <= 34.7101:
            return (["Obstacle 5/Task 2","Large Ravine/Spectrographic Analysis","4/10 points maximum","14.4/14.5","23-25"])
        elif -86.655003 <= x <= -86.654717 and 34.709961 <= y <= 34.7101:
            return (["Obstacle 6","Martian Sand Dunes","5 points maximum","14.6","26"])
        elif -86.655361 <= x <= -86.655164 and 34.710031 <= y <= 34.710203:
            return (["Task 3","Instrument Deployment","11 points maximum","14.7","27"])
        elif -86.654947 <= x <= -86.654797 and 34.710225 <= y <= 34.710436:
            return (["Obstacle 7","Crevasses","3 points maximum","14.8","27"])
        elif -86.655114 <= x <= -86.654892 and 34.710444 <= y <= 34.710531:
            return (["Obstacle 8","Side Incline","3 points maximum","14.9","28"])
        elif -86.655119 <= x <= -86.654958 and 34.710303 <= y <= 34.710442:
            return (["Obstacle 9","Lunar Crater","4 points maximum","14.10","29"])
        elif -86.655208 <= x <= -86.655008 and 34.710228 <= y <= 34.7103:
            return (["Task 4","Flag Plant and Photo","7 points maximum","14.11","30"])
        elif -86.655319 <= x <= -86.655111 and 34.7105 <= y <= 34.7106:
            return (["Obstacle 10","Bouldering Rocks (large rocks)","4 points maximum","14.12","30-31"])
        elif -86.654828 <= x <= -86.654567 and 34.710536 <= y <= 34.710719:
            return (["Obstacle 11","Tilted Craters","2 points maximum","14.x","31"])
        elif -86.653503 <= x <= -86.653311 and 34.710619 <= y <= 34.710747:
            return (["Task 5","Liquid Sample Retrieval","10 points maximum","14.13","32"])
        elif -86.653253 <= x <= -86.653031 and 34.710767 <= y <= 34.710908:
            return (["Obstacle 12","Loose Regolith","4 points maximum","14.14","33"])
        elif -86.653033 <= x <= -86.652769 and 34.710844 <= y <= 34.711017:
            return (["Obstacle 13","Pea Gravel","4 points maximum","14.15","34"])
        elif -86.652536 <= x <= -86.652236 and 34.710883 <= y <= 34.711103:
            return (["Obstacle 14","Undulating Hills","2 points maximum","14.16","35"])
        else:
            return (["In course","Not near anything","0 points maximum","ALL","ALL"])
    else:
        return(["Not in course","n/a","n/a","ALL","ALL"])
