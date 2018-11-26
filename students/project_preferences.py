import networkx as nx

from students.models import Project, Student, User

def generate_project_preferences():
    projects = Project.objects.all()
    students = Student.objects.all()
    prefs = {}
    for student in students:
        preferences = []
        if student.preference1 is not None:
            preferences.append(str(student.preference1.name))
        if student.preference2 is not None:
            preferences.append(str(student.preference2.name))
        if student.preference3 is not None:
            preferences.append(str(student.preference3.name))
        if student.preference4 is not None:
            preferences.append(str(student.preference4.name))
        prefs[str(student.user.username)] = preferences
    num_persons = len(prefs)
    G = nx.DiGraph()
    G.add_node('dest', demand=num_persons)
    for person, projectlist in prefs.items():
        G.add_node(person, demand=-1)
        for i, project in enumerate(projectlist):
            if i == 0:
                cost = -100
            elif i == 1:
                cost = -75
            elif i == 2:
                cost = -50
            else:
                cost = -25
            G.add_edge(person, project, capacity=1, weight=cost)

    for project in projects:
        G.add_edge(project.name, 'dest', capacity=3, weight=0)

    flowdict = nx.min_cost_flow(G)
    list_result = []
    for person in prefs:
        for p, flow in flowdict[person].items():
            if flow:
                print(person, 'joins', p)
                list_result.append(person+" joins " + p)
                user = User.objects.filter(username=person).first()
                per = Student.objects.filter(user=user).first()
                proj = Project.objects.filter(name=p).first()
                per.project_assigned = proj
                per.save()
    return list_result