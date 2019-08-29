from jenkinsapi.jenkins import Jenkins


# 连接jenkins
def get_server_instance(jenkins_url, username, password):
    return Jenkins(jenkins_url, username=username, password=password)


# build jenkins项目
def build_jenkins(jenkins_url, username, password, params, job_name):
    server = get_server_instance(jenkins_url=jenkins_url, username=username, password=password)
    server.build_job(job_name, params)


#  server = get_server_instance(jenkins_url='http://192.168.254.160:8080/jenkins/', username='wanyilei', password='Zcdsw123`')
# params = {'machine': 'mogu', 'data': '20190322', 'time': '15:00:00'}
# ret = server.build_job('uat-core-time', params)

