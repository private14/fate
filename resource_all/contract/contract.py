import pdfkit
import zipfile
from resource_all.resource import *
import shutil
import paramiko
from run import *

global text_path
text_path = os.path.dirname(os.path.realpath(__file__)) + "/"


# 生成txt文件
def create_text(name):
    full_path = text_path + name + '.txt'
    file = open(full_path, 'wb')
    file.close()


# 生成合同pdf
def create_contract(name):
    full_path = text_path + name + '.txt'
    create_text(name)
    pdfkit.from_string(full_path, text_path + name + '.pdf')
    # 删除多余的txt文件
    if os.path.exists(full_path):
        os.remove(full_path)


class JieBei:

    @staticmethod
    def create_contract(name, number):
        # 生成合同pdf
        create_contract(name)
        # 压缩合同pdf
        zip_file = zipfile.ZipFile(text_path + number + "A.zip", 'w', zipfile.ZIP_DEFLATED)
        zip_file.write(text_path + name + '.pdf', name + '.pdf')
        zip_file.close()
        # 创造txt文件
        file = open(text_path + number + "A.zip.txt", 'a+')
        file.write("JIEBEI,PLATFORM3," + name + "A,CREDIT_AUTHZ," + name + "A.pdf\n")
        file.close()
        # 删除pdf
        if os.path.exists(text_path + name + '.pdf'):
            os.remove(text_path + name + '.pdf')
        if env_path == 'sit1':
            # 上传到sit1
            os.system("sh " + text_path + "/scp_sit1.sh " + text_path + "*.zip")
            os.system("sh " + text_path + "/scp_sit1.sh " + text_path + "*.zip.*")
            # 清理环境
            os.system("rm -rf " + text_path + "*.zip*")
            # 上传到借呗
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.0.210", 22, "root", "51xf@password123")
            ssh.exec_command('sh /opt/app/sftp/ftp.sh ' + number)
            ssh.close()
        if env_path == 'uat':
            os.system("sh " + text_path + 'ftp_uat.sh ' + number)
            # 清理环境
            os.system("rm -rf " + text_path + "*.zip*")

    @staticmethod
    def create_photo(name, cert_no, number):
        shutil.copy(text_path + "cert_no_1.jpg", text_path + name + "_x.jpg")
        shutil.copy(text_path + "cert_no_2.jpg", text_path + name + "_y.jpg")
        # 生成文件
        os.system('cp ' + text_path + '2323 ' + text_path + number + "A.zip")
        zip_file = zipfile.ZipFile(text_path + number + "A.zip", 'w', zipfile.ZIP_DEFLATED)
        zip_file.write(text_path + name + '_x.jpg', name + '_x.jpg', )
        zip_file.write(text_path + name + '_y.jpg', name + '_y.jpg')
        zip_file.close()
        # 创造txt文件
        file = open(text_path + number + "A.zip.txt", 'a+')
        file.write("JIEBEI,PLATFORM3," + name + ",IDCARDX," + name + "_1111111111111_x.jpg\n")
        file.write("JIEBEI,PLATFORM3," + name + ",IDCARDY," + name + "_1111111111111_y.jpg\n")
        file.close()
        # 删除jpg
        if os.path.exists(text_path + name + '_x.jpg'):
            os.remove(text_path + name + '_x.jpg')
        if os.path.exists(text_path + name + '_y.jpg'):
            os.remove(text_path + name + '_y.jpg')
        if env_path == 'sit1':
            # 上传到sit1
            os.system("sh " + text_path + "/scp_sit1.sh " + text_path + "*.zip")
            os.system("sh " + text_path + "/scp_sit1.sh " + text_path + "*.zip.*")
            # 清理环境
            os.system("rm -rf " + text_path + "*.zip*")
            # 上传到借呗
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.0.210", 22, "root", "51xf@password123")
            ssh.exec_command('sh /opt/app/sftp/ftp_photo.sh ' + number)
            ssh.close()
        if env_path == 'uat':
            os.system("sh " + text_path + 'ftp_photo_uat.sh ' + number)
            # 清理环境
            os.system("rm -rf " + text_path + "*.zip*")


    @staticmethod
    def scp_to_sftp(name, cert_no, number):
        # 创造数据
        JieBei.create_contract(name, number)
        JieBei.create_photo(name, cert_no, number)
        sleep(2)
        # 修改数据库
        image_dict = select_mysql('channel', "select * from jiebei_credit_image where applyNo ='201975509536136386A';")
        for i in image_dict:
            operate_mysql('channel', 'INSERT INTO jiebei_credit_image VALUES {};'.format(insert_data(i).replace('201975509536136386A', name)))
        sleep(2)


def zip_file_contract_jiebei(name, number):
    zipf = zipfile.ZipFile(text_path + number + "A.zip", 'w', zipfile.ZIP_DEFLATED)
    zipf.write(text_path + name + '.pdf', name + '.pdf')
    zipf.close()
    # 创造txt文件
    file = open(text_path + number + "A.zip.txt", 'a+')
    file.write("JIEBEI,PLATFORM3," + name + "A,CREDIT_AUTHZ," + name + "A.pdf\n")
    file.close()
    # 删除pdf
    if os.path.exists(text_path + name + '.pdf'):
        os.remove(text_path + name + '.pdf')


def zip_file_photo_jiebei(name, number):
    shutil.copy(text_path + "cert_no_1.jpg", text_path + name + "_x.jpg")
    shutil.copy(text_path + "cert_no_2.jpg", text_path + name + "_y.jpg")
    zipf = zipfile.ZipFile(text_path + number + "A.zip", 'w', zipfile.ZIP_DEFLATED)
    zipf.write(text_path + name + '_x.jpg', name + '_x.jpg')
    zipf.write(text_path + name + '_y.jpg', name + '_y.jpg')
    zipf.close()
    # 创造txt文件
    file = open(text_path + number + "A.zip.txt", 'a+')
    file.write("JIEBEI,PLATFORM3," + name + "A,IDCARDX," + name + "_x.jpg\n")
    file.write("JIEBEI,PLATFORM3," + name + "A,IDCARDY," + name + "_y.jpg\n")
    file.close()

    zipf1 = zipfile.ZipFile(text_path + number + "A.zip.txt", 'w', zipfile.ZIP_DEFLATED)
    zipf1.write(text_path + name + '_x.jpg', name + '_x.jpg')
    zipf1.write(text_path + name + '_y.jpg', name + '_y.jpg')
    zipf1.close()
    # 删除jpg
    if os.path.exists(text_path + name + '_x.jpg'):
        os.remove(text_path + name + '_x.jpg')
    if os.path.exists(text_path + name + '_y.jpg'):
        os.remove(text_path + name + '_y.jpg')
