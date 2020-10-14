from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User
from diagrams.generic.place import Datacenter
from diagrams.onprem.network import Internet
from diagrams.saas.chat import Slack
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import Circleci
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.general import Azurehome
from diagrams.azure.web import AppServices
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.devops import Devops
from diagrams.azure.compute import VMWindows

text = "I want: \n\nname: feature-2079\n\nOrder: feature-2079\nUser&MD: 2020Q2\nShop: 2020Q2\nQuote: 2020Q2\nInventory: 2020Q2\n...\n\nUptime: working hours\n\nowner: abc@opuscapita.com"

with Diagram("\n\nHow it is implemented", show=False):
  u = User("User interface\nOpusCapita/eproc-line-launcher")
  gh = Github("Github repository\nOpusCapita/eproc-line-deployment\nbranch 'feature-2079'")
  dc = Circleci("Automated process\ninCircleCI")
  url = KubernetesServices("URL to running\ninstallation\nin Azure Kubernetes cluster\n\nhttps://demo.eproc.dev.opuscapita.com\n/eproc-line-deployment/feature-2079/")
  slack = Slack("Notification in Slack\n#eproc-dev-installations")

  u >> Edge(label=text, color="darkgreen") >> gh >> dc >> url >> slack
