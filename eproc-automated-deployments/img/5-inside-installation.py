from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import Circleci
from diagrams.k8s.network import SVC
from diagrams.azure.compute import KubernetesServices
from diagrams.onprem.database import Mysql
from diagrams.onprem.search import Solr
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.azure.network import DNSZones
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.elasticsearch import Kibana
from diagrams.azure.identity import ActiveDirectory
from diagrams.generic.device import Tablet
from diagrams.azure.storage import StorageAccounts

with Diagram("\n\nInside installation", show=False):
  user = User("User")
  with Cluster("Azure"):
    dns = DNSZones("demo.eproc.\ndev.opuscapita.com")

    with Cluster("Kubernetes cluster"):
      lb = Nginx("Loadbalancer\n(public IP\n1.2.3.4)")
      oauth2 = ActiveDirectory("Microsoft\nActiveDirectory\nlets only OpusCapita\nmembers in")

      with Cluster("Namespace 'dev-eproc-line-deployment-feature-2079'"):
        with Cluster("Applications"):
          opc = SVC("Shop: 2020Q2")
          apps = [
            SVC("Order: feature-2079"),
            opc,
            SVC("User&MD: 2020Q2"),
            SVC("Quote: 2020Q2")
          ]
          SVC("...")
        with Cluster("Secondary services"):
          solr = Solr("Solr search engine")
          opc >> solr

          josso = SVC("JoSSO (auth)")
          user >> dns >> lb >> josso >> apps

          email = SimpleEmailServiceSes("email server\nfor development\n(catch-all SMTP)")

          shell = Tablet("Web console\nwhich allows\nlower level\nadmin actions")

      with Cluster("MySQL server"):
        dbsvc = SVC("mysql")
        db = Mysql("database\nfeature-2079")
        apps >> dbsvc >> db

      with Cluster("Metrics"):
        grafana = Grafana("Grafana\nvisualizes metrics")
        prometheus = Prometheus("Prometheus\ngatheres metrics")
        prometheus >> grafana
        apps >> prometheus

      with Cluster("Logs"):
        els = Elasticsearch("Elasticsearch\nstores logs")
        kibana = Kibana("Kibana\nUI for logs")
        apps >> els >> kibana

      with Cluster("Backup/restore data"):
        velero = SVC("Velero\nsaves backups to\nAzure storage")
        apps >> velero

  admin = User("Admin")

  grafana >> admin
  kibana >> admin
  shell >> admin
