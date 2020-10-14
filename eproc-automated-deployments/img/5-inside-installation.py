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
from diagrams.onprem.container import Docker
from diagrams.generic.storage import Storage

with Diagram("\n\nInside installation", show=False):
  user = User("User\nhttps://demo.eproc.\ndev.opuscapita.com\n/eproc-line-deployment\n/feature-2079")

  with Cluster("Azure"):
    dns = DNSZones("demo.eproc.\ndev.opuscapita.com")

    with Cluster("Kubernetes cluster"):
      lb = Nginx("Loadbalancer\n(public IP\n1.2.3.4)")
      oauth2 = ActiveDirectory("Microsoft\nActiveDirectory\nlets only OpusCapita\nmembers in")

      with Cluster("Namespace 'dev-eproc-line-deployment-feature-2079'"):
        with Cluster("Applications"):
          with Cluster("Shop"):
            opc = SVC("Shop")
            opcd = Docker("opuscapita/opc:2020Q2")
            opc >> opcd

          with Cluster("Order"):
            proc = SVC("Order")
            procd = Docker("opuscapita/proc:feature-2079")
            proc >> procd

          with Cluster("User&MD"):
            prov = SVC("User&MD")
            provd = Docker("opuscapita/prov:2020Q2")
            prov >> provd

          with Cluster("Quote"):
            rfq = SVC("Quote")
            rfqd = Docker("opuscapita/rfq:2020Q2")
            rfq >> rfqd

          with Cluster("..."):
            dotdot = SVC("...")
            dotdotd = Docker("...")
            dotdot >> dotdotd

          apps = [ proc, opc, prov, rfq, dotdot ]

          images = [ procd, opcd, provd, rfqd, dotdotd ]

        with Cluster("Secondary services"):
          solr = Solr("Solr search engine")
          opc >> solr

          josso = SVC("JoSSO\n(Single sign-on)")
          user >> dns >> lb >> oauth2 >> josso >> apps

          email = SimpleEmailServiceSes("email server\nfor development\n(catch-all SMTP)\nwith UI and\nREST API")

          fs = Storage("Shared filesystem:\nworkarea,\nconfiguration area,\ncustomization area")

          shell = Tablet("Web console\nwhich allows\nlower level\nadmin actions")

      with Cluster("MySQL server"):
        dbsvc = SVC("mysql")
        db = Mysql("database\nfeature-2079")
        images >> dbsvc >> db

      with Cluster("Metrics"):
        grafana = Grafana("Grafana\nvisualizes metrics")
        prometheus = Prometheus("Prometheus\ngatheres metrics")
        prometheus >> grafana
        images >> prometheus

      with Cluster("Logs"):
        els = Elasticsearch("Elasticsearch\nstores logs")
        kibana = Kibana("Kibana\nUI for logs")
        images >> els >> kibana

      with Cluster("Backup/restore data"):
        velero = SVC("Velero\nsaves backups to\nAzure storage")
        images >> velero

  admin = User("Admin")

  grafana >> admin
  kibana >> admin
  shell >> admin
