# To-Do

* => I wanna incorporate TDD (Test Driven Development).
* First of all, code simple program
  * ~~Implementation progress of task (For picture generation takes a long time )~~
  * => Migrate environment using docker
  * ~~Test of Gunicorn launch~~
  * ~~Code Database related API~~
  * ~~Test of connection between MySQL and FastAPI App~~
  * ~~Code Database CRUD~~
  * Code test-code
  * Code CI/CD workflow part of Dev
  * Code frontend simply
  * Code CI/CD workflow part of Sec
* Next, Deploy to AWS
  * Do AWS related config
  * Code Configuration Management Tool File
  * Code CI/CD workflow part of Ops
  * Configure server administration and operation
* Implementation part of Machine Learning
  * Test of Tensorflow's Docker lanch
  * Code template of StyleTransfer
  * Test of StyleTransfer implementation

# Technical-Elements

* Backend
  * **FastAPI**
  * **MySQL**
  * **Tensorflow** (Machine Learning)
* Frontend
  * **Vue.js**
* Environment
  * **AWS** (Infrastructure)
  * IaC
    * **Docker** (Container)
    * **Terraform** (Configuration Management Tool for AWS Instance)
    * **Ansible** (Configuration Management Tool for Server)
  * Operate
    * **Kubernetes** (Container Orchestration)
    * **Prometheus** (System Resource Management)
    * **Elastic** (SIEM / Log Visualization)
  * Security
    * **CrowdSec** (Firewall / IPS)
* DevSecOps
  * **GithubActions** (CI/CD)
  * **Git-secret** (Secret Manager)
  * **Flake** (Linter)
  * **Pytest** (Testing)
  * **Synopsys** (Software Composition Analysis / Static Application Security Testing)
  * **OWASP ZAP** (Dynamic Application Security Testing)
  * (Interactive Application Security Testing)

# Temp

* Dev (plan -> code -> build -> test)
* Ops (release -> deploy -> operate -> monitor)
* Sec (Threat Modeling -> Pre-Commit Hooks -> Secret Management -> SCA / SAST -> DAST / IAST)
* IaC
