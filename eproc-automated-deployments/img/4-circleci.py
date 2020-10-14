from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import Circleci
from diagrams.k8s.network import SVC
from diagrams.azure.compute import KubernetesServices
from diagrams.onprem.database import Mysql
from diagrams.onprem.search import Solr

text = "Create or update\n\nI want: \n\nname: feature-2079\n\nOrder: feature-2079\nUser&MD: 2020Q2\nShop: 2020Q2\nQuote: 2020Q2\nInventory: 2020Q2\n...\n\nUptime: working hours\n\nowner: abc@opuscapita.com"

with Diagram("\n\nContinuous Integration", show=False):
  gh = Github("OpusCapita/eproc-line-deployment\nbranch 'feature-2079'")
  ci = Circleci("OpusCapita/eproc-line-deployment\nbranch 'feature-2079'")
  aks = KubernetesServices("Azure\nKubernetes\nService (AKS)")

  gh >> Edge(label="automated webhook\non every push") >> ci >> aks

  with Cluster("Kubernetes Cluster in Azure"):
    with Cluster("namespace 'dev-eproc-line-deployment-master'"):
      SVC("Order: master\nand other services...")
    with Cluster("namespace 'dev-eproc-line-deployment-feature-2079'"):
      apps = [
        SVC("Order: feature-2079"),
        SVC("...")
      ]

  aks >> apps