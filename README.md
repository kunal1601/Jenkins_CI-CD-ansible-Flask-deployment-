# 🚀 CI/CD Pipeline with Jenkins, Ansible & Docker

This project demonstrates an automated CI/CD pipeline where a Flask application is built into a Docker image using Jenkins, deployed using Ansible, and launched on a remote EC2 instance.

The goal is to implement a fully automated deployment process using **Jenkins for orchestration**, **Ansible for remote automation**, and **Docker for containerization** — all without using Docker Hub or pre-built images.

---

## 📦 Features

- 🛠️ Jenkins automation for continuous integration
- 🐳 Docker used to containerize the Flask application
- 🤖 Ansible playbook to deploy container on remote EC2
- 🔐 Secure SSH key-based authentication between Jenkins & remote node
- 🚫 No external Docker Hub usage — image is saved and transferred as `.tar`

---

## ⚙️ Prerequisites

✅ Two EC2 Instances (Amazon Linux):

1. **Jenkins EC2**: Jenkins and Docker installed  
2. **Target EC2**: Docker installed (via Ansible), SSH accessible

✅ SSH access configured (key pair, Ansible inventory)

✅ Python 3, pip, and Ansible installed on Jenkins instance

✅ Jenkins plugins: Pipeline

---

## 📝 Jenkinsfile (CI/CD Pipeline)

```groovy

pipeline {
    agent any
    environment {
        JAVA_HOME = "/usr/lib/jvm/java-21-amazon-corretto.x86_64"
        PATH = "${JAVA_HOME}/bin:${env.PATH}"
        REMOTE_USER = "ec2-user"
        REMOTE_HOST = "3.110.204.242"
        IMAGE_NAME = "flask-app"
        TAR_FILE = "${env.WORKSPACE}/flask-app.tar"
    }

    stages {
        stage('SCM') {
            steps {
                git 'https://github.com/kunal1601/Jenkins_CI-CD-ansible-Flask-deployment-.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Converting into Tar format') {
            steps {
                sh 'docker save ${IMAGE_NAME}:latest -o ${TAR_FILE}'
            }
        }

        stage('Transfer Image to Target Node') {
            steps {
                sshagent(['QA_env_id']) {
                    sh """
                    scp -o StrictHostKeyChecking=no ${TAR_FILE} ${REMOTE_USER}@${REMOTE_HOST}:/home/${REMOTE_USER}/
                    """
                }
            }
        }

        stage('Deploy via Ansible') {
            steps {
                sshagent(['QA_env_id']) {
                  sh """
                   ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} \\
                   'ansible-playbook -i /etc/ansible/hosts /home/ec2-user/ansible-flask_app/deployment.yaml'
                  """
                }
             }
          }
    }
}
```

🛠️ Setup & Run
1️⃣ On Jenkins EC2
- Install Docker:
  sudo yum install docker -y && sudo systemctl start docker

- Install Ansible:
  sudo pip3 install ansible

- Install Jenkins (skip if done)

  Clone your repo inside Jenkins job

2️⃣ Jenkins Job Setup
 Create Pipeline Job → Configure using Jenkinsfile

Click Build Now

✅ Result
Your Flask app should be live on:

http://<Target-EC2-Public-IP>
