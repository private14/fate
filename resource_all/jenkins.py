import jenkins


def jenkins(url, username, password, job_id, param_list):
    server = jenkins.Jenkins(url, username=username, password=password)
    server.build_job(job_id, param_list)



jenkins("http://jenkins.51xf.cn/jenkins/", "wanyilei", "Abc123456")
