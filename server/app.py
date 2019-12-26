from flask import Flask, jsonify, request
import json


app = Flask(__name__)
#app.debug = True


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/getVolunteers')
def get_volunteers():
    with open(app.root_path + '/../db/volunteers.json', 'r') as data:
        volunteers = data.read()
    return jsonify(json.loads(volunteers))


@app.route('/getProjects')
def get_projects():
    with open(app.root_path + '/../db/projects.json', 'r') as data:
        projects = data.read()
    return jsonify(json.loads(projects))


@app.route('/getTimeSheets')
def get_timesheets(volunteer_id=None):
    with open(app.root_path + '/../db/timesheets.json', 'r') as data:
        timesheets = data.read()
    return jsonify(json.loads(timesheets))


@app.route(
    '/recordTime/<volunteer_id>',
    methods=[
        'POST',
        'PUT',
        'DELETE'])
def record_time(volunteer_id):
    content = request.json
    project_id = content['project_id']
    new_visits = content['visits']
    new_missed_visits = content['missed_visits']
    with open(app.root_path + '/../db/timesheets.json', 'r') as data:
        tmpdata = data.read()
    existing_timesheets = json.loads(tmpdata)['timesheets']
    existing_visits = [record['visits'] for record in existing_timesheets if (
        record['project_id'] == project_id and record['volunteer_id'] == volunteer_id)][0]
    existing_missed_visits = [record['missed_visits'] for record in existing_timesheets if (
        record['project_id'] == project_id and record['volunteer_id'] == volunteer_id)][0]
    resultant_visits = list(
        {x['date']: x for x in existing_visits + new_visits}.values())
    resultant_missed_visits = list(
        {x['date']: x for x in existing_missed_visits + new_missed_visits}.values())
    [record.update(visits=resultant_visits) for record in existing_timesheets if (
        record['project_id'] == project_id and record['volunteer_id'] == volunteer_id)][0]
    [record.update(missed_visits=resultant_missed_visits) for record in existing_timesheets if (
        record['project_id'] == project_id and record['volunteer_id'] == volunteer_id)][0]
    with open(app.root_path + '/../db/timesheets.json', 'w') as data:
        data.write(json.dumps({'timesheets': existing_timesheets}))
    return jsonify(content)


if __name__ == '__main__':
    app.run()
