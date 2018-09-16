#!/usr/bin/env groovy

node('master') {
    try {
        stage('build') {
            checkout scm

            sh "python3 -m venv venv"
            sh "source venv/bin/activate"
            sh "pip install -e ."
        }

        stage('test') {
            sh "pytest"
            sh "coverage run"
            sh "coverage report"
        }

        stage('deploy') {
            // ansible-playbook -i ./ansible/hosts ./ansible/deploy.yml
            sh "echo 'WE ARE DEPLOYING'"
        }
    } catch(error) {
        throw error
    } finally {

    }

}
